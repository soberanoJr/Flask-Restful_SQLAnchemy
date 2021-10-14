# 1, 4, 5
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# 2, 5
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
# 3
from sqlalchemy.ext.declarative import declarative_base

# 1
engine = create_engine("sqlite:///activities.db")

# 2
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

# 3
Base = declarative_base()
Base.query = db_session.query_property()


# 4
class People(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True)
    age = Column(Integer)

    def __repr__(self):
        return "Person: {}".format(self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


# 5
class Activities(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    person_id = Column(Integer, ForeignKey("people.id"))
    person = relationship("People")

    def __repr__(self):
        return "Person: {}".format(self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(20))

    def __repr__(self):
        return "User: {}".format(self.login)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
