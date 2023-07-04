import pymysql
import pandas as pd
from sqlalchemy import create_engine
from dbCon import DB_URI

engine=create_engine(DB_URI)
df=pd.read_csv("douban_movies.csv",encoding="gb18030")
df.to_sql('movieinfo', engine, if_exists='append',index=False,chunksize=1000)