from database.database import db_session
from database.models import DoctorStatus, Doctor, Department, DoctorSchedule, DoctorStatistic
import datetime

weight = {
    'day': 5,
    'month': 5,
    'year': 5,
}
def updateDoctorStatus(department, doctor, period, roomStatus, calledNumber):
    # Get Previous Doctor Status
    status = DoctorStatus.query \
        .filter_by(doctor = doctor) \
        .filter_by(department = department) \
        .first()

    # Get Stats
    newStats = False
    stats = DoctorStatistic.query \
            .filter_by(department = department) \
            .filter_by(doctor = doctor) \
            .first()
    if stats is None: 
        newStats = True
        stats = DoctorStatistic(
            department = department,
            doctor = doctor
        )
        stats.currentCount = calledNumber
        if period == u'上午':
            hour = 8
            minute = 0
        elif period == u'下午':
            hour = 13
            minute = 30
        elif period == u'晚上':
            hour = 17
            minute = 0
        now = datetime.datetime.now()
        stats.currentAvg = (now - now.replace(hour=hour, minute=minute)).total_seconds() / int(calledNumber) if int(calledNumber) != 0 else 0
        stats.currentDate = now.date()
        stats.currentPeriod = period

    # if exists, update
    if status is not None:
        if(status.calledNumber != calledNumber):
            if newStats is False:
                updateStatistic(stats, period, calledNumber, status.calledNumber, status.updateTime)

                status.calledNumber = calledNumber
                status.period = period
                status.timeDelta = (stats.lastPeriodAvg * stats.lastPeriodCount + stats.currentCount * stats.currentAvg) / (stats.lastPeriodCount + stats.currentCount) if (stats.lastPeriodCount + stats.currentCount) != 0 else 0

    else:
        # Create Model
        newDoctorStatus = DoctorStatus(
            department = department,
            doctor = doctor,
            period = period,
            roomStatus = roomStatus,
            calledNumber = calledNumber
        )
        if newStats :
            db_session.add(stats)
        else:
            updateStatistic(stats, period, calledNumber, status.calledNumber, status.updateTime)
        newDoctorStatus.timeDelta = stats.currentAvg
        # Add to session
        db_session.add(newDoctorStatus)
        


    # Commit to database
    db_session.commit()
def updateStatistic(stats, period, calledNumber, prevCalledNumber, prevUpTime):
    now = datetime.datetime.now()
    deltaCount = int(calledNumber) - prevCalledNumber
    deltaTime = (now - prevUpTime).total_seconds()
    avg = deltaTime / deltaCount if deltaCount != 0 else 0

    if compareTime(stats.currentDate, stats.currentPeriod, period):
        stats.lastPeriodAvg = (stats.lastPeriodAvg * stats.lastPeriodCount + stats.currentCount) / stats.lastPeriodCount + 1
        stats.lastPeriodCount = stats.lastPeriodCount + 1 if stats.lastPeriodCount < 20 else 20
        stats.currentCount = calledNumber
        stats.currentAvg = avg
        stats.currentDate = now.date()
        stats.currentPeriod = period
    else: 
        stats.currentAvg = ( deltaTime + stats.currentAvg * stats.currentCount ) / (deltaCount + stats.currentCount) if (deltaCount + stats.currentCount) != 0 else 0
        stats.currentCount = deltaCount + stats.currentCount

def createDoctor(name, id):
    # Query
    doctor = Doctor.query \
        .filter_by(name = name) \
        .first()

    # if exists, return
    if doctor is not None: 
        return

    # Create
    newDoctor = Doctor(
        name = name,
        id = id,
    )
    
    # Add to session
    db_session.add(newDoctor)

    # Commit to database
    db_session.commit()

def createDepartment(name, id):
    # Query
    dept = Department.query \
        .filter_by(name = name) \
        .first()

    # if exists, return
    if dept is not None: 
        return

    # Create
    newDept = Department(
        name = name,
        id = id,
    )
    
    # Add to session
    db_session.add(newDept)

    # Commit to database
    db_session.commit()

def createSchedule(department, doctor, date, period):
    # Query
    dept = DoctorSchedule.query \
        .filter_by(department = department) \
        .filter_by(doctor = doctor) \
        .filter_by(date = date) \
        .filter_by(period = period) \
        .first()

    # if exists, return
    if dept is not None: 
        return

    # Create
    newSchedule = DoctorSchedule(
        department = department,
        doctor = doctor,
        date = date,
        period = period,
    )
    
    # Add to session
    db_session.add(newSchedule)

    # Commit to database
    db_session.commit()

def getDoctorStatus(doctor):
    status = DoctorStatus.query \
        .filter_by(doctor = doctor) \
        .first()
    return status

def getDoctorSchedule():
    return DoctorSchedule.query.all()


def compareTime(dataDate, dataPeriod, period):
    if dataDate < datetime.datetime.now().date(): return True
    elif dataDate == datetime.datetime.now().date():
        if dataPeriod == None: return True
        if dataPeriod == u'上午' and period != u'上午': return True
        if dataPeriod == u'下午' and period == u'晚上': return True
        if dataPeriod == u'晚上' and period != u'晚上': return True
    return False

def removeAllOutdateStatus():
    statuses = DoctorStatus.query.all()

    for status in statuses:
        if status.createDate < datetime.datetime.now().date():
            print('Status: {}/{} {}'.format(status.department, status.doctor, status.calledNumber))
            db_session.delete(status)
            db_session.commit()

def removeAllOutdateSchedule():
    schedules = DoctorSchedule.query.all()
    period = getCurrentPeriod()

    for schedule in schedules:
        if compareTime(schedule.date, schedule.period, period):
            print('Delete Schedule: {} {} {}/{}'.format(schedule.date.strftime('%Y-%m-%d'), schedule.period, schedule.department, schedule.doctor))
            db_session.delete(schedule)
            db_session.commit()

def getCurrentPeriod():
    now = datetime.datetime.now()
    if now > now.replace(hour=17, minute=0):
        return u'晚上'
    if now > now.replace(hour=13, minute=30):
        return u'下午'
    if now > now.replace(hour=8, minute=0):
        return u'上午'