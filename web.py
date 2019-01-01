from flask import Flask, request, jsonify
from database.controller import getDoctorStatus, getDoctorSchedule
import json

app = Flask(__name__)

@app.route('/status/<doctor>')
def status(doctor):
    # doctor = doctor.encode('raw_unicode_escape').decode('utf-8')
    docObj = getDoctorStatus(doctor)
    if docObj is None: docObj = []
    return jsonify(dict(docObj))

@app.route('/schedule')
def schedule():
    schedules = getDoctorSchedule()
    return jsonify([ dict(schedule) for schedule in schedules ])

def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port='3000', debug=True) 

if __name__ == '__main__':
    run()