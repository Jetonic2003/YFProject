from sqlalchemy import create_engine,text

# 数据库的配置变量
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'jobdb'
USERNAME = 'root'
PASSWORD = 'Jtnic027'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

# 创建数据库引擎
engine = create_engine(DB_URI)

#创建连接
with engine.connect() as con:
    rs = con.execute(text('SELECT * FROM users'))
    print(rs.fetchone())