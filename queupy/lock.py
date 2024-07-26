import peewee


def acquire_advisory_lock(db : peewee.Database, resource_id : int):
    cursor = db.execute_sql('SELECT pg_advisory_lock(%s);', (resource_id,))
    cursor.close()


def release_advisory_lock(db : peewee.Database, resource_id : int):
    cursor = db.execute_sql('SELECT pg_advisory_unlock(%s);', (resource_id,))
    cursor.close()

