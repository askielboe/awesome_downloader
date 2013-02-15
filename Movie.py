from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    """"""
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    imdbId = Column(String)
    link = Column(String)
    last_searched = Column(Integer)
    downloaded = Column(Boolean)
    

    #----------------------------------------------------------------------
    def __init__(self, title, year):
        """"""
        self.title = title
        self.year = year

