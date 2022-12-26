from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False , autoflush= False , bind = engine)

Base = declarative_base() 

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


















# while True:
#     try:
#         conn  = psycopg2.connect(host ="localhost" , database = "appdata" ,\
#                                 cursor_factory = RealDictCursor,user ="postgres" , password = "Ashish@2022")
#         cursor = conn.cursor()
#         print("The connection has been succesfully established")
#         break
#     except Exception as error:
#         print("Connection Failed" , error)
#         time.sleep(2)