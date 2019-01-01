from database.database import db_session
from database.models import DoctorStatus, Doctor, Department, DoctorSchedule

def updateDoctorStatus(department, doctor, period, roomStatus, calledNumber):
    # Get Previous Doctor Status
    status = DoctorStatus.query \
        .filter_by(doctor = doctor) \
        .filter_by(department = department) \
        .first()

    # if exists, update
    if status is not None:
        if(status.calledNumber != calledNumber):
            print(department + ' / ' + doctor + ' exist .....update')
            status.calledNumber = calledNumber
            status.period = period
    else:
        # Create Model
        newDoctorStatus = DoctorStatus(
            department = department,
            doctor = doctor,
            period = period,
            roomStatus = roomStatus,
            calledNumber = calledNumber
        )

        # Add to session
        db_session.add(newDoctorStatus)

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