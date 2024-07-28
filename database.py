# from urllib.parse import quote_plus
# from sqlalchemy import create_engine, MetaData, text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from databases import Database
# import logging
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# password = quote_plus("$1OwukktWWC0")
# DATABASE_URL = f"mysql+pymysql://aieltsir_oprt:{password}@95.217.119.130/aieltsir_ddb"
# database = Database(DATABASE_URL)
# metadata = MetaData()
#
# engine = create_engine(DATABASE_URL, echo=True)  # Set echo=True for SQLAlchemy to log SQL queries
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# # Enable logging for SQLAlchemy
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
#
