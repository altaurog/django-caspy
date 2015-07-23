from django import db
from django.test.utils import CaptureQueriesContext


class AssertMaxQueries(CaptureQueriesContext):
    def __init__(self, max_query_count, show_queries=True, connection=None):
        if connection is None:
            connection = db.connection
        super(AssertMaxQueries, self).__init__(connection)
        self.max_query_count = max_query_count
        self.show_queries = show_queries

    def __exit__(self, exc_type, exc_value, traceback):
        super(AssertMaxQueries, self).__exit__(exc_type, exc_value, traceback)
        if exc_type is not None:
            return
        executed = len(self)
        if executed > self.max_query_count:
            msg_template = "%d queries executed, %d expected"
            msg = msg_template % (executed, self.max_query_count)
            if self.show_queries:
                queries = (query['sql'] for query in self.captured_queries)
                msg += "\nCaptured queries were:\n%s" % '\n'.join(queries)

            raise AssertionError(msg)


# Better looking alias
assert_max_queries = AssertMaxQueries
