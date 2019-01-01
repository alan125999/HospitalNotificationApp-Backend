#!/bin/python3
import urllib.request
import json

from sqlalchemy import func, or_, not_

# Crawl
for id in range(1000):
    url = 'http://59.125.231.55/trews/api/GetDptRoomInfo?DptID={0:03d}'.format(id)
    fpIn = urllib.request.urlopen(url)
    data = fpIn.read().decode('utf8')
    if data != '[]':
        # Store Data
        ''' 
        fpOut = open('./cralwerData/{0:03d}'.format(id), 'w')
        fpOut.write(data)
        '''
        jsonData = json.loads(data)
        # doctorStatus = list(map(lambda x: {
        #     'RoomStatus': x.RoomStatus,
        #     'deptID': x.deptID,
        #     'deptName': x.deptName.strip(),
        #     'opdTimeID': x.opdTimeID,
        #     'roomID': x.roomID,
        #     'roomName': x.roomName,
        #     'roomLocation': x.roomLocation,
        #     'doctorID': x.doctorID,
        #     'doctorName': x.doctorName,
        #     'calledNumber': x.calledNumber, 
        # }, jsonData))
        
        for obj in jsonData:
            query = session.query(doctorStatus)
            found_rows = query.filter_by(doctorName = obj.get('doctorName')).filter_by(deptName = obj.get('deptName').strip() )
            isNewHistory = False
            if(found_rows.first() == None):
                isNewHistory = True
                # Insert
                print(obj.get('deptName').strip() + ' / ' + obj.get('doctorName') + ' not exist .....insert')
                storeDoctorStatus(obj.get('deptID'), obj.get('deptName').strip(), obj.get('doctorName'), obj.get('opdTimeID'), obj.get('RoomStatus'), obj.get('calledNumber'))
            else:
                # Update
                if(found_rows.first().calledNumber != obj.get('calledNumber')):
                    isNewHistory = True
                    print(obj.get('deptName').strip() + ' / ' + obj.get('doctorName') + ' exist .....update')
                    found_rows.update({
                        'deptID'       :  obj.get('deptID'),
                        'doctorID'     :  obj.get('doctorID'),
                        'roomID'       :  obj.get('roomID'),
                        'roomName'     :  obj.get('roomName'),
                        'roomLocation' :  obj.get('roomLocation'),
                        'opdTimeID'    :  obj.get('opdTimeID'),
                        'RoomStatus'   :  obj.get('RoomStatus'),
                        'calledNumber' :  obj.get('calledNumber')
                    })
                else: print(obj.get('deptName').strip() + ' / ' + obj.get('doctorName') + ' exist .....no update')
            if(isNewHistory):
                dsh = doctorStatusHistory(
                    deptID = obj.get('deptID'),
                    deptName = obj.get('deptName').strip(),
                    doctorID = obj.get('doctorID'),
                    doctorName = obj.get('doctorName'),
                    roomID = obj.get('roomID'),
                    roomName = obj.get('roomName'),
                    roomLocation = obj.get('roomLocation'),
                    opdTimeID = obj.get('opdTimeID'),
                    RoomStatus = obj.get('RoomStatus'),
                    calledNumber = obj.get('calledNumber')
                )
                session.add(dsh)
            session.commit()
        print('Crawling {0:03d} ......OK'.format(id))
    else:
        print('Crawling {0:03d} ......Empty'.format(id))

# print(doctorStatus)


''' data format
[{
    "deptID": 科別代號,
    "deptName": 科別名稱,
    "doctorID": 醫師編號,
    "doctorName": 醫師姓名,
    "roomID": 診間代號,
    "roomName": 診間名稱（房號）,
    "roomLocation": 診間位置（棟別、樓層）,
    "opdTimeID": (尚未猜到是什麼),
    "RoomStatus": 準備中 / 看診中,
    "calledNumber": 當前號碼
}]
'''
