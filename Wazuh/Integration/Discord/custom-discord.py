#/usr/bin/env python3

import sys
import requests
import json
from requests.auth import HTTPBasicAuth

"""
ossec.conf configuration structure
 <integration>
     <name>custom-discord</name>
     <hook_url>https://discord.com/api/webhooks/XXXXXXXXXXX</hook_url>
     <alert_format>json</alert_format>
 </integration>
"""

# read configuration
alert_file = sys.argv[1]
user = sys.argv[2].split(":")[0]
hook_url = sys.argv[3]

# read alert file
with open(alert_file) as f:
    alert_json = json.loads(f.read())

# extract alert fields
alert_level = alert_json["rule"]["level"]

# colors from https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
if(alert_level < 5):
    # green
    color = "5763719"
elif(alert_level >= 5 and alert_level <= 7):
    # yellow
    color = "16705372"
else:
    # red
    color = "15548997"

# agent details
if "agentless" in alert_json:
	  agent_ = "agentless"
else:
    agent_ = alert_json["agent"]["name"]

# check for network log and set variables in testing 

if ("dstip" in str(alert_json)):
    network_ = ((alert_json["data"]["srcip"]) + " -> " + (alert_json["data"]["dstip"]))
    netName_ = "Network: "
    if ("dstport" in str(alert_json)):
        network_ = (network_ + ":" + (alert_json["data"]["dstport"]))
    else:
        network_ = (network_ + ":N/A")
    if ("protocol" in str(alert_json)):
        network_ = (network_ + "\nProto: " + (alert_json["data"]["protocol"]))
    else:
        network_ = (network_ + "\nProto: N/A")
else:
    network_ = netName_= ""

# combine message details
content = "HML: in testing"

#Debbuger VV
#with open('/home/custom-teams-debug.log', 'w', encoding='utf-8') as my_file:
#    my_file.write(str(content) + '\n')

payload = json.dumps({
    "content": content,
    "embeds": [
        {
		    "title": f"Wazuh Alert - Rule {alert_json['rule']['id']}",
				"color": color,
				"description": alert_json["rule"]["description"],
				"fields": [
               {"name": "Agent","value": agent_,"inline": False},
               {"name": netName_,"value": network_,"inline": False}
               ]
        }
    ]
})

# send message to discord
r = requests.post(hook_url, data=payload, headers={"content-type": "application/json"})
sys.exit(0)
