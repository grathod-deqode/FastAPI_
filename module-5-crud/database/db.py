from sqlalchemy import create_engine ,URL
from sqlalchemy.orm import sessionmaker , declarative_base


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="deq@123",
    host="localhost",
    port=5432,
    database="crud_practice"
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush= False,bind = engine,autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try :
        yield db 
    finally : 
        db.close()