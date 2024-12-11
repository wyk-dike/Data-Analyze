import pandas as pd

class DataProcessor:
    @staticmethod
    def parse_json_column(df, json_column_name):
        return pd.json_normalize(df[json_column_name])

    @staticmethod
    def explode_column(df, column_name):
        return df.explode(column_name)
