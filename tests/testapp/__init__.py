def set_constraints_immediate(connection):
    # psql constraints are deferred until COMMIT by default
    # but standard test case will not COMMIT, so we force
    # constraint checking earlier
    if connection.vendor in ('postgresql',):
        cur = connection.cursor()
        cur.execute("SET CONSTRAINTS ALL IMMEDIATE")
        cur.close()
