from sqlalchemy import create_engine

dbURI = 'sqlite+pysqlite:///3444.db'
engine = create_engine(dbURI)
