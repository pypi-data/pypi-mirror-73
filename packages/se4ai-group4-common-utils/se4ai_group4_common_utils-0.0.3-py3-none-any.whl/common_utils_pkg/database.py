import os
from sqlalchemy import create_engine, Column, Text, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, user, password, host, port, database, **kwargs):
        self.engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                user, password, host, port, database
            ), **kwargs)
        Base = declarative_base(self.engine)
        self.Movie = self._create_movie_class(Base)
        self.User = self._create_user_class(Base)
        self.Rating = self._create_rating_class(Base)

    def load_session(self):
        # TODO: should we checkout scoped sessions
        Session = sessionmaker(bind=self.engine)
        return Session()
 
    def _create_movie_class(self, base):
        class Movie(base):
            __tablename__ = 'movies'
            __table_args__ = ({'autoload': True})
        return Movie
    
    def _create_user_class(self, base):
        class User(base):
            __tablename__ = 'users'
            __table_args__ = {'autoload':True}
        return User

    def _create_rating_class(self, base):
        class Rating(base):
            __tablename__ = 'ratings'

            movie_id = Column(Text, primary_key =True)
            user_id = Column(Text, primary_key =True)
            rating = Column(SmallInteger)
        return Rating
    