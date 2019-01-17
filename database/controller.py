from database.database import db_session
from database.models import DoctorStatus, Doctor, Department, DoctorSchedule, DoctorStatistic, periodDict
import datetime

def getDoctorStats(department, doctor):
    stats = DoctorStatistic.query \
        .filter_by(department = department) \
        .filter_by(doctor = doctor) \
        .first()
    return stats

def getStatus(department, doctor):
    status = DoctorStatus.query \
        .filter_by(department = department) \
        .filter_by(doctor = doctor) \
        .first()
    return status

def createDoctorStats(department, doctor, period, calledNumber):
    stats = DoctorStatistic(
        department = department,
        doctor = doctor,
        currentDate = datetime.datetime.now().date(),
        currentPeriod = period
    )
    return stats

def createDoctorStatus(department, doctor, period, roomStatus, calledNumber):
    newDoctorStatus = DoctorStatus(
        department = department,
        doctor = doctor,
        period = period,
        roomStatus = roomStatus,
        calledNumber = calledNumber
    )
    return newDoctorStatus
    
def updateDoctorStatus(department, doctor, period, roomStatus, calledNumber):
    calledNumber = int(calledNumber)
    now = datetime.datetime.now()

    # Get Stats
    stats = getDoctorStats(department, doctor)

    # Get Doctor Status
    status = getStatus(department, doctor)

    if status is None:
        if stats is None:
            # No status and stats -> First time 
            stats = createDoctorStats(department, doctor, period, calledNumber)
            status = createDoctorStatus(department, doctor, period, roomStatus, calledNumber)
            db_session.add(stats)
            db_session.add(status)
        else:
            # No Status but stats -> No First time overall, but is today's first time
            status = createDoctorStatus(department, doctor, period, roomStatus, calledNumber)
            status.timeDelta = stats.currentAvg
            if stats.currentAvg != None:
                stats.lastPeriodAvg = (stats.lastPeriodAvg * stats.lastPeriodCount + stats.currentAvg) / (stats.lastPeriodCount + 1)
                stats.lastPeriodCount += 1
            stats.currentAvg = None
            stats.currentCount = calledNumber
            stats.currentDate = now.date(),
            stats.currentPeriod = period
            db_session.add(status)
    else:
        if status.calledNumber != calledNumber:
            if status.period == stats.currentPeriod and stats.currentDate == datetime.datetime.now().date():
                deltaNum = calledNumber - stats.currentCount
                deltaTime = (status.updateTime - now).total_seconds()
                if stats.currentAvg == None:
                    stats.currentAvg = deltaTime / deltaNum
                else:
                    stats.currentAvg = (stats.currentAvg * stats.currentCount + deltaTime) / calledNumber
                stats.currentCount = calledNumber
                status.calledNumber = calledNumber
                if stats.lastPeriodAvg == None:
                    status.timeDelta = stats.currentAvg
                else:
                    status.timeDelta = stats.currentAvg * 0.6 + stats.lastPeriodAvg * 0.4
                status.roomStatus = roomStatus
            else:
                status.period = period
                status.roomStatus = roomStatus
                status.calledNumber = calledNumber
                if stats.currentAvg != None:
                    stats.lastPeriodAvg = (stats.lastPeriodAvg * stats.lastPeriodCount + stats.currentAvg) / (stats.lastPeriodCount + 1)
                    stats.lastPeriodCount += 1
                stats.currentAvg = None
                stats.currentCount = calledNumber
                stats.currentDate = now.date(),
                stats.currentPeriod = period

    # Commit to database
    db_session.commit()


def createDoctor(name, id):
    # Ignore if empty
    if id == None: return

    # Query
    doctor = Doctor.query \
        .filter_by(name = name) \
        .first()

    # if exists, return
    if doctor is not None: return

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
        return periodDict['night']
    if now > now.replace(hour=13, minute=30):
        return periodDict['afternoon']
    if now > now.replace(hour=8, minute=0):
        return periodDict['morning']