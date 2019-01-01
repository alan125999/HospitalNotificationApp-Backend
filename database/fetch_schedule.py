#!/bin/python3
from bs4 import BeautifulSoup
import requests
import urllib.request
import json
from sqlalchemy import create_engine, Column, PrimaryKeyConstraint, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import CHAR, Integer, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
class docTime(enum.Enum):
  morning = 1
  afternoon = 2
  night = 3

# define
maxDay = 12
DB_HOST = '127.0.0.1:3306'
DB_USER = 'root'
DB_PASSWD = ''
DB_NAME = 'hospital_notification'
DB_CONNECT_STRING = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(DB_USER, DB_PASSWD, DB_HOST, DB_NAME)
DB_DEBUG = False
DB_RESET = False

# Connect Databases
engine = create_engine(DB_CONNECT_STRING, echo=DB_DEBUG)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

# Create ORM Table
BaseModel = declarative_base()

class doctorSchedule(BaseModel):
    __tablename__ = 'doctorSchedule'
    __table_args__ = (
        PrimaryKeyConstraint('deptName', 'doctorName'),
    )
    deptID       =  Column( CHAR(10)     )
    deptName     =  Column( CHAR(20)     )
    doctorName   =  Column( CHAR(10)     )
    date         =  Column( Date         ) 
    time         =  Column( Enum(docTime))

# Create Table
# BaseModel.metadata.tables['doctorSchedule'].create(engine)

# list to store data
date      = [ None ] * maxDay
morning   = [ None ] * maxDay
afternoon = [ None ] * maxDay
night     = [ None ] * maxDay

# Download Page
r = requests.get('http://www2.cych.org.tw/WebToNewRegister/webSerchDrSch.aspx?No=020')
# Check if success
if r.status_code == requests.codes.ok:
  # Parse
  soup = BeautifulSoup(r.text, 'html.parser')
  # fetch parameter for next page
  payload = dict(
    __VIEWSTATE       = soup.find(id='__VIEWSTATE').get('value'),
    __EVENTVALIDATION = soup.find(id='__EVENTVALIDATION').get('value'),
    rb2               = soup.find(id='rb2').get('value'),
    __EVENTTARGET     = 'rb2',
  )
  print(payload)
  
  # fetch schedule with id
  for i in range(maxDay):
    date[i] = soup.find(id='Label' + str(i+1))
    morning[i] = soup.find(id='lblMRest' + str(i+1))
    afternoon[i] = soup.find(id='lblARest' + str(i+1))
    night[i] = soup.find(id='lblNRest' + str(i+1))

# store to DB
for i in range(maxDay):
  print(date[i].string[:-3])
  if date[i] != None:
    if morning[i] != None:
      ds = doctorSchedule(
        deptID     = ID,
        deptName   = DEPT,
        doctorName = morning[i].string[:-4],
        date       = ,
        time       = 'morning',
      )
  

# Download Page2
r = requests.post('http://www2.cych.org.tw/WebToNewRegister/webSerchDrSch.aspx?No=020', data=payload)

# Check if success
if r.status_code == requests.codes.ok:
  # Parse
  soup = BeautifulSoup(r.text, 'html.parser')
  
  # fetch schedule with id
  for i in range(maxDay):
    date[i] = soup.find(id='Label' + str(i+1))
    morning[i] = soup.find(id='lblMRest' + str(i+1))
    afternoon[i] = soup.find(id='lblARest' + str(i+1))
    night[i] = soup.find(id='lblNRest' + str(i+1))

# store to DB
for i in range(maxDay):
  print(date[i])