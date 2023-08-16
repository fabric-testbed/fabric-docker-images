# Heartbeat Monitor
The Heartbeat Monitor checks for the prescense of heart beat alerts that each rack should be sending. Each rack sends heartbeat alerts to the alertmanager. When the alertmanager receives a heart beat alert it notifies this heartbeat monitor. 
When the heartbeat monitor receives the group of heart beat alerts, it compares them to the the monitored_racks file which contains a json list of the racks that should be sending out heartbeats. If any are missing, the heartbeat monitor then sends out a missing heartbeat alert to the alertmanger.

## Examples
There sample docker-compose file with a sample heartbeat_racks file (racks that are actually sending heartbeates) and monitored_racks (racks that should be sending our heartbeats) file.

## Needed env variables


### The list of racks that have recently sent heartbeats.
heartbeat_racks_filename = os.environ["heartbeat_racks_filename"]
### The list of racks that should be sending heartbeats.
monitored_racks_filename = os.environ["monitored_racks_filename"]

### The alertmanger that will recieve alerts about missing heartbeats/
alertmanager_url = os.environ["alertmanager_url"]
alertmanager_user = os.environ["alertmanager_user"]
alertmanager_pass = os.environ["alertmanager_pass"]


