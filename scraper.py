# -*- coding: utf-8 -*-

import urllib
import urllib.request
import json
from database.controller import updateDoctorStatus, createDepartment, createDoctor, createSchedule, removeAllOutdateSchedule, removeAllOutdateStatus
from bs4 import BeautifulSoup
import datetime
import string
import re
from constants import maxDay, deptDict, scrapUrlPrefix, schedulePeriodList, periodDict

def scrapStatus():
    ## Iterate Departments ##
    for key, value in deptDict.items():
        # Combine Url
        url = scrapUrlPrefix['status'] + key

        # Download Page
        data = downloadPage(url)

        # Store
        parseStatus(data, value)

def scrapSchedule():
    ## Iterate Departments ##
    for key, value in deptDict.items():
        # Combine Url
        url = scrapUrlPrefix['schedule'] + key

        # Download Page
        data = downloadPage(url)

        # Parse
        payload = parseSchedule(data, value)

        # Download Page2
        data = downloadPage(url, **payload)

        # Parse
        parseSchedule(data, value)

def opdTimeToPeriod(opd):
    mapOpt = {
        'A': periodDict['morning'],
        'P': periodDict['afternoon'],
        'Z': periodDict['night'],
    }
    if opd not in mapOpt.keys(): return None
    else: return mapOpt[opd]

def downloadPage(url, **payload):
    # Requset
    if payload: 
        # POST
        response = urllib.request.urlopen(url, data=urllib.parse.urlencode(payload).encode("utf-8"))
    else: 
        # GET
        response = urllib.request.urlopen(url)
        
    # Read
    return response.read().decode('utf8')


def parseStatus(data, deptName):
    # Ignore if empty
    if data == '[]':
        return

    # Parse
    doctors = json.loads(data)

    # Create Status
    for doctor in doctors:
        # Convert doctor dict
        doctorID, doctorName, period, roomStatus, calledNumber = spreadDoctorDict(doctor)
        
        # Update Status
        print('Status: {}/{} {}'.format(deptName, doctorName, calledNumber))
        updateDoctorStatus(deptName, doctorName, period, roomStatus, calledNumber)

        # Create Doctor
        createDoctor(doctorName, doctorID)


def spreadDoctorDict(doctor):
    # Spread Data
    doctorID = doctor['doctorID'].strip()
    doctorName = doctor['doctorName'].strip()
    period = opdTimeToPeriod( doctor['opdTimeID'].strip() )
    roomStatus = doctor['RoomStatus'].strip()
    calledNumber = doctor['calledNumber'].strip()
    return (doctorID, doctorName, period, roomStatus, calledNumber)


def getParamForNextSchedulePage(soup):
    # fetch parameter for next page
    payload = dict(
        __VIEWSTATE = soup.find(id='__VIEWSTATE').get('value'),
        __EVENTVALIDATION = soup.find(id='__EVENTVALIDATION').get('value'),
        rb2 = soup.find(id='rb2').get('value'),
        __EVENTTARGET = 'rb2',
    )
    return payload


def parseSchedule(data, deptName):
    # Get Parser
    soup = BeautifulSoup(data, 'html.parser')

    # Get Payload for next page
    payload = getParamForNextSchedulePage(soup)

    # fetch schedule with id
    for i in range(1, maxDay + 1):
        date = soup.find(id='Label' + str(i))

        # Check Date
        if date is None: continue

        # Parse Date
        dateObj = parseScheduleDate(date)

        for period in schedulePeriodList:
            doctorNames = soup.find(id=period['payload'] + str(i))
            createScheduleDoctors(doctorNames, deptName, dateObj, period['period'])

    return payload


regex = re.compile(r"[SG\d◎\(\)\ ]|休診|代診", re.IGNORECASE)
def createScheduleDoctors(doctors, department, date, period):
    if doctors is None: return

    # Convert to string list
    doctors = doctors.strings

    for doctor in doctors:
        name = regex.sub('', doctor)
        if name == '': continue
        
        print('Schedule: {} {} {}/{}'.format(date.strftime('%Y-%m-%d'), period, department, name))
        createSchedule(department, name, date, period)


def parseScheduleDate(date):
    dateParam = date.string[:-3].split('/')
    return datetime.datetime(int(dateParam[0]) + 1911, int(dateParam[1]), int(dateParam[2]))


def storeAllDepartment():
    for key, value in deptDict.items():
        createDepartment(value, key)


def clean():
    removeAllOutdateStatus()
    removeAllOutdateSchedule()
