import pickle
from alembic import op
import sqlalchemy as sa
from typing import Generator
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, PickleType, Integer, String, create_engine, select, update

Base = declarative_base()


class Face(Base):
    __tablename__ = "faces"
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    caption = Column(String)
    face_attrs = Column(PickleType)
    group = Column(String)
    age = Column(Integer)
    gender = Column(Integer)

    def attrs(self):
        return pickle.loads(self.face_attrs)


engine = create_engine("sqlite:///db.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
#connection = engine.connect()
#query = f'ALTER TABLE faces ADD age INT;'
#connection.execute(query)


class Db:
    @staticmethod
    def store_face(file_name: str, caption: str, face_attrs):
        face = Face(file_name=file_name, caption=caption, face_attrs=pickle.dumps(face_attrs))
        with Session() as session:
            session.add(face)
            session.commit()

    @staticmethod
    def get_face(id: int):
        with Session() as session:
            return session.execute(select(Face).where(Face.id == id)).fetchall()[0][0]

    @staticmethod
    def get_all_faces() -> list[Face]:
        with Session() as session:
            return [row for row in session.query(Face) if row.age != 0]

    @staticmethod
    def get_contain_faces(str) -> list[Face]:
        return [row for row in Session().query(Face) if str in row.file_name]


    @staticmethod
    def view_base():
        for face in Db.get_all_faces():
            print(str(face.id) + ' ' + face.caption + ' ' + face.file_name, face.group, face.age, face.gender)

    @staticmethod
    def update(file_name, age):
        session = Session()
        session.query(Face).filter(Face.file_name == file_name).update({'age': age})
        session.commit()


#print(Db.get_contain_faces('azamat')[0].id)
#with Session() as session:
#    session.query(Face).filter(Face.id > 30).update({'file_name': 'actors/' + Face.caption + '.jpg'})
#    session.commit()
Db.view_base()


