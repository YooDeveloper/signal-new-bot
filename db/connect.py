from orator import DatabaseManager, Schema, Model

DATABASES = {
    'sqlite3': {
        'foreign_keys': True,
        'driver': 'sqlite',
        'database': './database.sqlite'
    }
}

db = DatabaseManager(DATABASES)
schema = Schema(db)
Model.set_connection_resolver(db)
