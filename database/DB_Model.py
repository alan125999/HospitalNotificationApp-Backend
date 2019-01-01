# Import
from sqlalchemy import create_engine, Column, PrimaryKeyConstraint, text
#!/bin/python3
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import CHAR, Integer, String, TIMESTAMP, Interval
from sqlalchemy.ext.declarative import declarative_base

# Environment
DB_HOST = '127.0.0.1:3306'
DB_USER = 'root'
DB_PASSWD = ''
DB_NAME = 'hospital_notification'
DB_DEBUG = True

# Create Model Base Class
BaseModel = declarative_base()

# Define Model
class doctorStatus(BaseModel):
    # Table name
    __tablename__ = 'doctorStatus'

    __table_args__ = (
        PrimaryKeyConstraint('deptName', 'doctorName'),
    )
    # Table Structure
    deptName     =  Column(CHAR(20))
    doctorName   =  Column(CHAR(10))
    period       =  Column(CHAR(5))
    roomStatus   =  Column(CHAR(10))
    calledNumber =  Column(CHAR(5))
    averageTime  =  Column(Interval)
    updatetime   =  Column(TIMESTAMP(True), nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class doctorStatusHistory(BaseModel):
    __tablename__ = 'doctorStatusHistory'
    __table_args__ = (
        PrimaryKeyConstraint('deptName', 'doctorName', 'createtime'),
    )
    deptID       =  Column( CHAR(10) )
    deptName     =  Column( CHAR(20) )
    doctorID     =  Column( CHAR(10) )
    doctorName   =  Column( CHAR(10) )
    roomID       =  Column( CHAR(10) )
    roomName     =  Column( CHAR(20) )
    roomLocation =  Column( CHAR(20) )
    opdTimeID    =  Column( CHAR(5)  )
    RoomStatus   =  Column( CHAR(10) )
    calledNumber =  Column( CHAR(5)  )
    createtime   =  Column(TIMESTAMP(True), nullable=False, server_default=text('NOW()')) 

# Create Lazy Connection
DB_CONNECT_STRING = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(DB_USER, DB_PASSWD, DB_HOST, DB_NAME)
engine = create_engine(DB_CONNECT_STRING, echo=DB_DEBUG)

# Create Session Class
DBSession = sessionmaker(bind=engine)