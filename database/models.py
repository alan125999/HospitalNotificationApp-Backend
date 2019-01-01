# -*- coding: utf-8 -*-

from sqlalchemy import Column, text
from sqlalchemy.types import Integer, String, Time, TIMESTAMP, Date, Enum
from database.database import Base
import datetime

class DoctorStatus(Base):
    # Table name
    __tablename__ = 'doctorStatuses'

    # Table Structure
    department = Column(String(20), primary_key=True, nullable=False)
    doctor = Column(String(10), primary_key=True, nullable=False)
    period = Column(String(10))
    roomStatus = Column(String(10))
    calledNumber = Column(String(5))
    timeDelta = Column(Integer)
    createDate = Column(Date, default=datetime.datetime.now().date())
    updateTime = Column(TIMESTAMP(True), nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return '<DoctorStatus %r>' % (self.department + '/' + self.doctor)

    def __iter__(self):
        yield 'department', self.department
        yield 'doctor', self.doctor
        yield 'period', self.period
        yield 'roomStatus', self.roomStatus
        yield 'calledNumber', self.calledNumber
        yield 'timeDelta', self.timeDelta
        yield 'createDate', self.createDate
        yield 'updateTime', self.updateTime

class Doctor(Base):
    # Table name
    __tablename__ = 'doctors'

    # Table Structure
    name = Column(String(10), primary_key=True, nullable=False)
    id = Column(String(10))

    def __repr__(self):
        return '<Doctor %r>' % (self.name)

class Department(Base):
    # Table name
    __tablename__ = 'departments'

    # Table Structure
    name = Column(String(20), primary_key=True, nullable=False)
    id = Column(String(10))

    def __repr__(self):
        return '<Department %r>' % (self.name)

class DoctorStatistic(Base):
    # Table name
    __tablename__ = 'doctorStatistics'

    # Table Structure
    department = Column(String(20), primary_key=True, nullable=False)
    doctor = Column(String(10), primary_key=True, nullable=False)
    currentAvg = Column(Integer, default=0)
    currentCount = Column(Integer, default=0)
    lastPeriodAvg = Column(Integer, default=0)
    lastPeriodCount = Column(Integer, default=0)
    # lastMonthAvg = Column(Integer, default=0)
    # lastMonthCount = Column(Integer, default=0)
    # lastYearAvg = Column(Integer, default=0)
    # lastYearCount = Column(Integer, default=0)
    currentDate = Column(TIMESTAMP(True), nullable=False, default=datetime.datetime.now())
    currentPeriod = Column(Enum(u'上午', u'下午', u'晚上'))

    def __repr__(self):
        return '<DoctorStatistic %r>' % (self.department + '/' + self.doctor)

class DoctorSchedule(Base):
    __tablename__ = 'doctorSchedules'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement = True)
    department = Column(String(20))
    doctor = Column(String(10))
    date = Column(Date)
    period = Column(Enum(u'上午', u'下午', u'晚上'))

    def __iter__(self):
        yield 'department', self.department
        yield 'doctor', self.doctor
        yield 'date', self.date
        yield 'period', self.period