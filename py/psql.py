from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus as urlquote
from sqlalchemy.types import String, Date, DateTime
import pandas as pd
from .util import *

class PSQL():
    def __init__(self, host: str = "192.168.1.86", port: str = "5432", db: str = 'ws_generator', user: str = 'postgres', password: str = 'MrPho1219@'):
        self.engine = create_engine(f'postgresql+psycopg2://{user}:%s@{host}:{port}/{db}' %urlquote(password))
        self.session = sessionmaker(bind = self.engine)()
        
    def addColtoTable(self, table: str, col_name: str, dtype:str = "VARCHAR(2000)"):
        self.engine.execute(statement = f'ALTER TABLE "{table}" ADD "{col_name}" {dtype};')

    def getTableCols(self, table: str):
        return pd.read_sql(f'SELECT * FROM "{table}" LIMIT 0;', self.engine).columns

    def addDFToVarTable(self, df: pd.DataFrame, table: str, dtype = String, use_index: bool = False):
        try:
            df.to_sql(name=table, con=self.engine, if_exists = 'append', dtype = dtype, index = use_index)
        except:
            sql_unique = buildDictBoolbyArr(self.getTableCols(table = table))
            df_unique = buildDictBoolbyArr(df.columns)
            df_unique[df.index.name] = True
            diff_arr = getDictDiffArr(dict_1 = sql_unique, dict_2 = df_unique)
            for diff in diff_arr:
                self.addColtoTable(table = table, col_name = diff)
            try:
                df.to_sql(name=table, con=self.engine, if_exists = 'append', dtype = dtype, index = use_index)
            except:
                pass
            
    def addSerialPKIntCol(self, table: str, col_name: str):
        self.engine.execute(f'ALTER TABLE "{table}" ADD COLUMN "{col_name}" SERIAL PRIMARY KEY;')


