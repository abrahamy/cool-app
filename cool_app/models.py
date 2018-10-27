from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import cool_app.settings as settings


Base = declarative_base()

engine = create_engine(settings.DATABASE_URI)
Session = sessionmaker()
Session.configure(bind=engine)


class Customer(Base):
    """Customer Entity"""

    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, index=True, unique=True)
    create_date = Column(DateTime, default=func.now())
    modified_date = Column(DateTime, onupdate=func.utc_timestamp())


Base.metadata.create_all(engine)
