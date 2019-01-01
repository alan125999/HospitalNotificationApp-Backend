# -*- coding: utf-8 -*-

import urllib
import urllib.request
import json
from database.controller import updateDoctorStatus, createDepartment, createDoctor, createSchedule, removeAllOutdateSchedule, removeAllOutdateStatus
from bs4 import BeautifulSoup
import datetime
import string
import re

maxDay = 12

deptDict = {
    # 內科部
    '020': u'一般內科',
    '021': u'胸腔內科暨重症科',
    '022': u'胃腸肝膽科',
    '023': u'心臟血管科',
    '024': u'腎臟內科',
    '025': u'過敏免疫風濕科',
    '027': u'感染科',
    '028': u'血液腫瘤科',
    '029': u'代謝科',
    '029A': u'糖尿病特診',
    '120': u'神經內科',

    # 外科部
    '030': u'一般外科',
    '030A': u'減重外科',
    '030C': u'甲狀腺特診',
    '031': u'心臟血管外科',
    '031A': u'靜脈曲張特診',
    '032': u'整形外科',
    '034': u'胸腔外科',
    '035': u'大腸直腸外科',
    '037': u'乳房外科',
    '038': u'外傷科',
    '070': u'神經外科',
    '080': u'泌尿外科',

    # 兒童醫學部
    '040': u'兒童醫學部',
    '040A': u'健兒門診',
    '042': u'兒童胃腸科',
    '043': u'兒童心臟科',
    '044': u'兒童過敏免疫科',
    '045': u'兒童內分泌',
    '045A': u'兒童遺傳代謝科',
    '046': u'兒童腦神經科',
    '047': u'兒童感染科',
    '048': u'兒童腎臟科',
    '049': u'小兒血液腫瘤科',
    '033': u'小兒外科',

    # 骨科部
    '060': u'骨科',
    '062': u'骨科手外科',
    '063': u'踝及足外科',
    '065': u'脊椎外科',
    '066': u'運動醫學及肩肘外科',
    '067': u'關節重建科',
    '068': u'骨折外傷科',
    '069': u'小兒骨科',

    # 婦產部
    '050': u'婦產科',

    # 中醫部
    '620': u'中醫科',

    # 精神科
    '130': u'精神科',
    '133': u'兒童心理衛生門診',

    # 臨床心理中心
    '135A': u'身心壓力諮詢',
    '135B': u'兒青心智門診',

    # 獨立科
    '010': u'家庭醫學科',
    '010B': u'老人醫學科',
    '010C': u'緩和醫療門診',
    '0131': u'子宮頸抹片特別門診',
    '039': u'醫學美容(自費)',
    '090': u'耳鼻喉科',
    '100': u'眼科',
    '110': u'皮膚科',
    '140': u'復健科',
    '230': u'職業醫學科',
    '400': u'牙科',
    '401': u'口腔外科',
    '40A': u'特殊需求牙科',
    '811': u'疼痛科',
    '821': u'放射腫瘤科',
    '840': u'核醫科',
    'HSJ': u'戒菸門診',
}

periodDict = {
    'P': u'上午',
    'A': u'下午',
    'Z': u'晚上',
    '': '',
}

def scrapStatus():
    # urlPrefix = 'http://59.125.231.55/trews/api/GetDptRoomInfo?DptID='
    urlPrefix = 'http://www2.cs.ccu.edu.tw/~wth105u/cralwerData/server.php?id='
    for key, value in deptDict.items():
        # Combine Url
        url = urlPrefix + key

        # Requset
        response = urllib.request.urlopen(url)

        # Read
        data = response.read().decode('utf8')

        # Store
        if data != '[]':
            doctors = json.loads(data)

            # # Create Department
            # deptName = doctors[0]['deptName'].strip()
            # createDepartment(deptName, key)

            # Create Status
            for doctor in doctors:

                # Spread Data
                deptName = value
                doctorID = doctor['doctorID'].strip()
                doctorName = doctor['doctorName'].strip()
                opdTimeID = doctor['opdTimeID'].strip()
                RoomStatus = doctor['RoomStatus'].strip()
                calledNumber = doctor['calledNumber'].strip()

                period = periodDict[opdTimeID]

                # Update Status
                print('Status: {}/{} {}'.format(deptName, doctorName, calledNumber))
                updateDoctorStatus(deptName, doctorName, period, RoomStatus, calledNumber)

                # Create Doctor
                if doctorID != None:
                    createDoctor(doctorName, doctorID)

def scrapSchedule():
    # Download Page
    urlPrefix = 'http://www2.cych.org.tw/WebToNewRegister/webSerchDrSch.aspx?No='
    for key, value in deptDict.items():
        # Combine Url
        url = urlPrefix + key

        # Requset
        response = urllib.request.urlopen(url)

        # Read
        data = response.read().decode('utf8')

        # Parse
        soup = BeautifulSoup(data, 'html.parser')

        # fetch parameter for next page
        payload = dict(
            __VIEWSTATE       = soup.find(id='__VIEWSTATE').get('value'),
            __EVENTVALIDATION = soup.find(id='__EVENTVALIDATION').get('value'),
            rb2               = soup.find(id='rb2').get('value'),
            __EVENTTARGET     = 'rb2',
        )

        parseSchedule(soup, value)

        # Download Page2
        response = urllib.request.urlopen(url, data=urllib.parse.urlencode(payload).encode("utf-8") )

         # Read
        data = response.read().decode('utf8')

        # Parse
        soup = BeautifulSoup(data, 'html.parser')
        parseSchedule(soup, value)

def parseSchedule(soup, department):
    # fetch schedule with id
    for i in range(1, maxDay + 1):
        date = soup.find(id='Label' + str(i))

        if date is not None:
            dateObj = parseScheduleDate(date)

            morning = soup.find(id='lblMRest' + str(i))
            afternoon = soup.find(id='lblARest' + str(i))
            night = soup.find(id='lblNRest' + str(i))

            createScheduleDoctors(morning, 'P', dateObj, department)
            createScheduleDoctors(afternoon, 'A', dateObj, department)
            createScheduleDoctors(night, 'Z', dateObj, department)

regex = re.compile(r"[S\d◎\(\)\ ]|休診|代診", re.IGNORECASE)
def createScheduleDoctors(doctors, period, date, department):
    if doctors is None: return

    doctors = doctors.strings
    for doctor in doctors:
        name = regex.sub('', doctor)
        if name == '': continue
        print('Schedule: {} {} {}/{}'.format(date.strftime('%Y-%m-%d'), periodDict[period], department, name))
        createSchedule(department, name, date, periodDict[period])
def parseScheduleDate(date):
    dateParam = date.string[:-3].split('/')
    return datetime.datetime(int(dateParam[0]) + 1911, int(dateParam[1]), int(dateParam[2]))

def storeAllDepartment():
    for key, value in deptDict.items():
        createDepartment(value, key)

def clean():
    removeAllOutdateStatus()
    removeAllOutdateSchedule()