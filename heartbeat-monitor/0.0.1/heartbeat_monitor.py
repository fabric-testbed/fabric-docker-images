import requests
import json
from flask import Flask, request, Response

import os

import logging

# Get needed variables, or use default vaulues
heartbeat_racks_filename = 'heartbeat_racks.json'
if 'heartbeat_racks_filename' in os.environ:
    heartbeat_racks_filename = os.environ["heartbeat_racks_filename"]

monitored_racks_filename = 'monitored_racks.json'
if 'monitored_racks_filename' in os.environ:
    monitored_racks_filename = os.environ["monitored_racks_filename"]

# alertmanager user & password not needed since we are running in isolated docker network
alertmanager_user = None
if 'alertmanger_user' in os.environ:
    alertmanager_user = os.environ["alertmanager_user"]

alertmanager_pass = None
if 'alertmanger_pass' in os.environ:
    alertmanager_pass = os.environ["alertmanager_pass"]

# Always need url
alertmanager_url = os.environ["alertmanager_url"]


app = Flask(__name__)

loglevel_str = "INFO"
loglevel = logging.INFO
if "heartbeat_log_level" in os.environ:
    loglevel_str = os.environ["heartbeat_log_level"]

if loglevel_str.upper() == 'DEBUG':
    loglevel = logging.DEBUG
if loglevel_str.upper() == 'ERROR':
    loglevel = logging.ERROR
if loglevel_str.upper() == 'WARNING':
    loglevel = logging.WARNING
if loglevel_str.upper() == 'ERROR':
    loglevel = logging.ERROR
if loglevel_str.upper() == 'CRITICAL':
    loglevel = logging.CRITICAL

logging.basicConfig(level = loglevel)
logger = app.logger
logger.info("Heartbeat Monitor Server Started.")
logger.info(f"Log level is {logger.getEffectiveLevel()}")


@app.route('/config')   
def config():
    # show basic config info 
    ret_val = f"<h2>Heartbeat file</h2> {heartbeat_racks_filename} <h2>Monitored file</h2> {monitored_racks_filename} <h2>Alertmanager URL</h2> {alertmanager_url} "
    logger.info(ret_val)
    return ret_val

@app.route('/')
def welcome():
    logger.debug("Welcome activated")
    return "Hello, heartbeat_monitor server is running."

@app.post('/alert_webhook')
def alert_in():
    # recieve alerts from the alertmanager
    json_data = request.get_json()
    logger.debug(json_data)
    # save the alert data to disk
    write_rack_alerts(json_data) 
    logger.debug("webhook activated")
    process_alerts()
    return Response(status=200)

@app.get('/missing')
def missing():
    # returns the list of missing racks according to most recent reading
    missing_racks = compare_racks()
    logger.debug(str(missing_racks))
    return str(missing_racks)


@app.get('/process_alerts')
def process_alerts():
    missing_racks = compare_racks()
    logger.info(f"Processing Alerts. Missing racks are {missing_racks}.")
    sent  = send_alerts(missing_racks)      
    logger.info(f"Sent {sent} alerts.")
    return str(missing_racks)

# Example of incoming alert notification
# {
#   "version": "4",
#   "groupKey": <string>,              // key identifying the group of alerts (e.g. to deduplicate)
#   "truncatedAlerts": <int>,          // how many alerts have been truncated due to "max_alerts"
#   "status": "<resolved|firing>",
#   "receiver": <string>,
#   "groupLabels": <object>,
#   "commonLabels": <object>,
#   "commonAnnotations": <object>,
#   "externalURL": <string>,           // backlink to the Alertmanager.
#   "alerts": [
#     {
#       "status": "<resolved|firing>",
#       "labels": <object>,
#       "annotations": <object>,
#       "startsAt": "<rfc3339>",
#       "endsAt": "<rfc3339>",
#       "generatorURL": <string>,      // identifies the entity that caused the alert
#       "fingerprint": <string>        // fingerprint to identify the alert
#     },
#     ...
#   ]
# }


def write_rack_alerts(alerts):
    # Write the list of racks that are contained in the recieved alert from alertmanager    
    racks = []
   
    for alert in alerts["alerts"]:
        logger.debug(f"adding {alert["labels"]["rack"]} ")
        racks.append( alert["labels"]["rack"] )
    rack_json_str = json.dumps({ "racks":racks} )

    with open( heartbeat_racks_filename, 'w' ) as out_file:
        out_file.write(rack_json_str)

def read_rack_alerts():
    # Read the list of racks that heartbeat alerts.
    with open(heartbeat_racks_filename, 'r' ) as in_file:
        rack_alerts = json.load(in_file)
    logger.debug("Reading rack alerts")
    logger.debug(rack_alerts)
    return rack_alerts

def read_monitored_racks():
    # Read the list of racks to be monitored.
    with open(monitored_racks_filename, 'r') as in_file:
        monitored_racks = json.load(in_file)
    logger.debug("Reading monitored racks")
    logger.debug(monitored_racks)
    return monitored_racks

def compare_racks():
    received_racks = read_rack_alerts()
    monitored_racks = read_monitored_racks()
    missing_racks = []
    for rack in monitored_racks["racks"]:
        if rack not in received_racks["racks"]:
            missing_racks.append(rack)
    return missing_racks 

def send_alerts(missing_racks):
    sent = 0
    for rack in missing_racks:
        send_alert(rack)
        sent += 1
    return sent


def send_alert(rack):
    alert_info = { 'labels':{'alertname':'HeartbeatMissing', 'rack':rack } }
    logger.info(f"Sending alert as {alert_info}")
    # user & pass not needed when running in closed docker network
    #r = requests.post( alertmanager_url , json=[{ 'labels':{'alertname':'HeartbeatMissing', 'rack':rack } }], auth=(alertmanager_user, alertmanager_pass ))
    r = requests.post( alertmanager_url , json=[{ 'labels':{'alertname':'HeartbeatMissing', 'rack':rack } }])
    for x in r:
        logger.debug(x)


