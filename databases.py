import sqlalchemy as db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy_serializer import SerializerMixin
engine = db.create_engine('sqlite:///Base.db')

conn = engine.connect()


class Base(DeclarativeBase):
    pass


class Thread(Base, SerializerMixin):
    __tablename__ = "Threads"

    id = Column(Integer, primary_key=True, index=True)

    id_user = Column(Integer)

    id_thread = Column(String)


Base.metadata.create_all(bind=engine)


def data():
    response = None
    with Session(autoflush=False, bind=engine) as db:
        res = {}
        response = db.query(Thread).all()
        for row in response:
            res[row.id_user] = row.id_thread
    return res


def create_thread_db(thread_id: str, user_id: int):
    response = None
    with Session(autoflush=False, bind=engine) as db:
        user = Thread(id_user = user_id, id_thread  = thread_id)
        db.add(user)
        db.commit()

