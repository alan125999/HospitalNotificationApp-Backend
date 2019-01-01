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

    # if exists, update
    if status is not None:
        if(status.calledNumber != calledNumber):
            # Get Stats
            stats = getDoctorStatistic(department, doctor)

            deltaCount = int(calledNumber) - status.calledNumber
            deltaTime = (datetime.datetime.now() - status.updateTime).total_seconds()
            avg = deltaTime / deltaCount if deltaCount != 0 else 0

            if compareTime(stats, period):
                stats.lastPeriodAvg = (stats.lastPeriodAvg * stats.lastPeriodCount + stats.currentCount) / stats.lastPeriodCount + 1
                stats.lastPeriodCount = stats.lastPeriodCount + 1 if stats.lastPeriodCount < 20 else 20
                stats.currentCount = calledNumber
                stats.currentAvg = avg
                stats.currentDate = datetime.datetime.now().date()
                stats.currentPeriod = period
            else: 
                stats.currentAvg = ( deltaTime + stats.currentAvg * stats.currentCount ) / (deltaCount + stats.currentCount)
                stats.currentCount = deltaCount + stats.currentCount

            status.calledNumber = calledNumber
            status.period = period
            status.timeDelta = (stats.lastPeriodAvg * stats.lastPeriodCount + stats.currentCount * stats.currentAvg) / (stats.lastPeriodCount + stats.currentCount)

    else:
        # Create Model
        newDoctorStatus = DoctorStatus(
            department = department,
            doctor = doctor,
            period = period,
            roomStatus = roomStatus,
            calledNumber = calledNumber
        )

        newDoctorStatistic = DoctorStatistic(
            department = department,
            doctor = doctor
        )
        newDoctorStatistic.currentCount = calledNumber
        if period == u'上午':
            hour = 8
            minute = 0
        elif period == u'下午':
            hour = 13
            minute = 30
        elif period == u'晚上':
            hour = 17
            minute = 0
        newDoctorStatistic.currentAvg = (datetime.datetime.now() - datetime.datetime.now().replace(hour=hour, minute=minute)).total_seconds() / int(calledNumber) if int(calledNumber) != 0 else 0
        newDoctorStatistic.currentDate = datetime.datetime.now().date()
        newDoctorStatistic.currentPeriod = period
        newDoctorStatus.timeDelta = newDoctorStatistic.currentAvg
        # Add to session
        db_session.add(newDoctorStatus)
        db_session.add(newDoctorStatistic)

    # Commit to database
    db_session.commit()

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

def getDoctorStatistic(department, doctor):
    return DoctorStatus.query \
        .filter_by(department = department) \
        .filter_by(doctor = doctor) \
        .first()

def compareTime(stats, period):
    if stats.currentDate.date() < datetime.datetime.now().date(): return True
    if stats.currentPeriod == None: return True
    if stats.currentPeriod == u'上午' and period != u'上午': return True
    if stats.currentPeriod == u'下午' and period == u'晚上': return True
    if stats.currentPeriod == u'晚上' and period != u'晚上': return True
    return False

