from sqlalchemy import create_engine

class Database:
    def __init__(self, db_config):
        self.db_config = db_config
        self.engine = self.create_engine()

    def create_engine(self):
        return create_engine(
            f"postgresql+psycopg2://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['dbname']}"
        )

    def fetch_data(self, table_name):
        import pandas as pd
        return pd.read_sql_query(f"SELECT * FROM {table_name}", self.engine)
