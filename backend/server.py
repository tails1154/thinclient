from flask import Flask, request
from tinydb import TinyDB, Query
import os

app = Flask(__name__)
db = TinyDB('db.json')
ssid_table = db.table('ssid')

# Ensure db structure on startup
def ensure_db():
    if len(ssid_table.all()) == 0:
        ssid_table.truncate()  # Create empty table

ensure_db()

# Check if SSID is already in db
def is_ssid_in_db(ssid):
    SSID = Query()
    return ssid_table.contains(SSID.ssid == ssid)

# Add a new SSID to the db
def add_ssid(ssid):
    if not is_ssid_in_db(ssid):
        ssid_table.insert({'ssid': ssid})

# /api/getuuid endpoint
@app.route('/api/getuuid')
def get_uuid():
    ssid = request.args.get('ssid', '')
    if is_ssid_in_db(ssid):
        return "/api/proxy"
    else:
        return "/api/prereg"

# /api/prereg endpoint
@app.route('/api/prereg')
def prereg():
    ssid = request.args.get('ssid', '')
    if is_ssid_in_db(ssid):
        return "/api/getuuid"
    else:
        add_ssid(ssid)
        return "/api/getuuid"
@app.route('/api/proxy')
def proxy():
    ssid = request.args.get('ssid', '')
    if is_ssid_in_db(ssid):
       return "http://192.168.0.107:8080"
    else:
        return "/api/prereg"


if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0")
