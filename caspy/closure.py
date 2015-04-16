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
        db_table = self.model._path_model._meta.db_table
        query = """
            INSERT INTO {0} (upper_id, lower_id, length)
            SELECT u.upper_id, l.lower_id, u.length + l.length + 1
            FROM {0} u, {0} l
            WHERE u.lower_id = %s AND l.upper_id = %s
            """.format(db_table)
        cursor = connection.cursor()
        cursor.execute(query, [upper.pk, lower.pk])
        result = cursor.rowcount
        cursor.close()
        return result

    def detach(self, lower):
        db_table = self.model._path_model._meta.db_table
        query = """
            DELETE FROM {0}
            WHERE {0}.id in (
                SELECT path.id FROM {0} path, {0} u, {0} l
                WHERE u.lower_id = %s AND u.length > 0
                AND l.upper_id = %s
                AND path.upper_id = u.upper_id
                AND path.lower_id = l.lower_id
            )
            """.format(db_table)
        cursor = connection.cursor()
        cursor.execute(query, [lower.pk, lower.pk])
        result = cursor.rowcount
        cursor.close()
        return result

    def paths(self, qset=None):
        nodes = list((qset or self)
                     .annotate(depth=models.Max('upper_set__length'))
                     .order_by('depth'))
        bypk = {n.pk: [n] for n in nodes}
        path_qset = self.model._path_model.objects.filter(length=1)
        if qset:
            path_qset = path_qset.filter(lower__in=qset)
        for a in path_qset:
            bypk[a.lower_id][0].parent = a.upper_id
        for n in nodes:
            if n.depth == 0:
                continue
            bypk[n.pk] = bypk.get(n.parent, []) + bypk[n.pk]
        return [bypk[n.pk] for n in nodes]
