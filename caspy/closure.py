from django.db import models, connection


def pathstr(self):
    return ' '.join(map(str, (self.upper_id, self.lower_id, self.length)))


def path_model(model):
    name = model.__name__ + 'Path'
    uniqueness = {'unique_together': [('upper', 'lower')]}
    attrs = {
        'upper': models.ForeignKey(model, related_name='lower_set'),
        'lower': models.ForeignKey(model, related_name='upper_set'),
        'length': models.IntegerField(),
        'Meta': type('Meta', (object,), uniqueness),
        '__module__': model.__module__,
        '__str__': pathstr,
    }
    path_model = type(name, (models.Model,), attrs)
    model._path_model = path_model
    register_signal_listeners(model, path_model)
    return path_model


def register_signal_listeners(model, path_model):
    def on_save(sender, **kwargs):
        if kwargs.get('raw') or not kwargs.get('created'):
            return
        obj = kwargs.get('instance')
        path_model.objects.create(upper=obj, lower=obj, length=0)
    uuid = 'closure_create_' + model.__name__
    models.signals.post_save.connect(on_save, model, False, uuid)

    def on_delete(sender, **kwargs):
        obj = kwargs.get('instance')
        model.tree.detach(lower=obj)
    uuid = 'closure_delete_' + model.__name__
    models.signals.pre_delete.connect(on_delete, model, False, uuid)


class TreeManager(models.Manager):
    def attach(self, lower, upper):
        query = self._query_format("""
            INSERT INTO {path_table} (upper_id, lower_id, length)
            SELECT upper.upper_id,
                lower.lower_id,
                upper.length + lower.length + 1
            FROM {path_table} upper, {path_table} lower
            WHERE upper.lower_id = %s AND lower.upper_id = %s
            """)
        cursor = connection.cursor()
        cursor.execute(query, [upper.pk, lower.pk])
        result = cursor.rowcount
        cursor.close()
        return result

    def detach(self, lower):
        query = self._query_format("""
            DELETE FROM {path_table}
            WHERE {path_table}.id in (
                SELECT path.id
                FROM {path_table} path,
                    {path_table} upper,
                    {path_table} lower
                WHERE upper.lower_id = %s AND upper.length > 0
                AND lower.upper_id = %s
                AND path.upper_id = upper.upper_id
                AND path.lower_id = lower.lower_id
            )
            """)
        cursor = connection.cursor()
        cursor.execute(query, [lower.pk, lower.pk])
        result = cursor.rowcount
        cursor.close()
        return result

    def paths(self, *args, **kwargs):
        return make_paths(self.path_annotated(*args, **kwargs))

    def path_annotated(self, where='WHERE 1 = 1', params=None):
        query = self._query_format("""
            SELECT {select}
                , max(dpath.length) AS depth
                , ppath.upper_id as parent_id
            FROM {table}
            LEFT OUTER JOIN {path_table} dpath
                ON ({table}.{pk} = dpath.lower_id)
            LEFT OUTER JOIN {path_table} ppath
                ON ({table}.{pk} = ppath.lower_id
                    AND ppath.length = 1)
            {where}
            GROUP BY {select}, ppath.upper_id
            """, where=where)
        return self.raw(query, params)

    def _query_format(self, query, **kwargs):
        kwargs = kwargs.copy()
        kwargs.update(self._query_format_kwargs())
        return query.format(**kwargs)

    def _query_format_kwargs(self):
        table = self._table()
        columns = self._columns()
        return {
            'table': table,
            'columns': columns,
            'pk': self._pk(),
            'path_table': self._path_table(),
            'select': ', '.join('%s.%s' % (table, c) for c in columns),
        }

    def _path_table(self):
        return self.model._path_model._meta.db_table

    def _table(self):
        return self.model._meta.db_table

    def _columns(self):
        return list(map(db_column, self._fields()))

    def _pk(self):
        for f in self._fields():
            if f.primary_key:
                return db_column(f)

    def _fields(self):
        return self.model._meta.local_fields


def db_column(field):
    return field.column or field.name


def make_paths(objects):
    nodes = sorted(objects, key=lambda o: o.depth)
    bypk = {n.pk: [n] for n in nodes}
    for n in nodes:
        if n.depth == 0:
            continue
        bypk[n.pk] = bypk.get(n.parent_id, []) + bypk[n.pk]
    return [bypk[n.pk] for n in nodes]
