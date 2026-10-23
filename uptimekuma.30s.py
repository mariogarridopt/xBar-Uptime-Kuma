#!/usr/bin/env python
#
# <xbar.title>UptimeKuma Monitor</xbar.title>
# <xbar.version>v1.1</xbar.version>
# <xbar.author>mariogarridopt</xbar.author>
# <xbar.author.github>mariogarridopt</xbar.author.github>
# <xbar.desc>Show UptimeKuma status</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/mariogarridopt/xBar-Uptime-Kuma</xbar.abouturl>
# <xbar.image>https://raw.githubusercontent.com/mariogarridopt/xBar-Uptime-Kuma/master/screenshot.png</xbar.image>
#

import os
from uptime_kuma_api import UptimeKumaApi

# -------------------------------------------

BASE_URL = 'http://localhost:3001' # no trailing slash
USERNAME = 'admin'
PASSWORD = 'admin'

# -------------------------------------------

try:
    api = UptimeKumaApi(BASE_URL)
    api.login(USERNAME, PASSWORD)

    monitor_list = api.get_monitors()
    monitor_total = len(monitor_list);
    monitor_online = 0;
    monitor_list_string = [];

    ## GET DATA AND USE REAL UPTIME KUMA GROUPS
    # Separate groups from child monitors
    groups = {}
    child_monitors = {}
    
    for monitor in monitor_list:
        beats = api.get_monitor_beats(monitor['id'], 24)
        text = monitor['name'] + " | href='" + BASE_URL + "/dashboard/" + str(monitor['id']) + "'"
        
        if(len(beats) > 0 and beats[-1]['status'] == True):
            monitor_online = monitor_online + 1
            status_icon = "🟢"
        else:
            status_icon = "❗️"
            text += " color='#ff0000'"
        
        # Check if this is a group or child monitor
        if monitor.get('parent') is None:
            # This is a group (parent monitor)
            groups[monitor['id']] = {
                'name': monitor['name'],
                'status_icon': status_icon,
                'text': text,
                'children': []
            }
        else:
            # This is a child monitor
            parent_id = monitor.get('parent')
            if parent_id not in child_monitors:
                child_monitors[parent_id] = []
            child_monitors[parent_id].append({
                'name': monitor['name'],
                'status_icon': status_icon,
                'text': f"--{status_icon} {text}"
            })
    
    # Build the menu structure
    for group_id, group_info in groups.items():
        if group_id in child_monitors:
            children = child_monitors[group_id]
            online_count = sum(1 for child in children if child['status_icon'] == '🟢')
            total_count = len(children)
            
            # Group status based on children
            if online_count == total_count and total_count > 0:
                group_status = "🟢"
            elif online_count > 0:
                group_status = "⚠️"
            else:
                group_status = "❗️"
            
            # Add group header
            monitor_list_string.append(f"{group_status} {group_info['name']} ({online_count}/{total_count})")
            
            # Add children
            for child in children:
                monitor_list_string.append(child['text'])
        else:
            # Group with no children, treat as standalone
            monitor_list_string.append(group_info['text'])

    ## PRINT DATA
    if monitor_online == monitor_total:
        print('🌍')
    else:
        print(monitor_online, '/', monitor_total)
    
    print('---')
    for monitors_text in monitor_list_string:
        print(monitors_text)
        
    print('---')
    print("Open UptimeKuma | href='" + BASE_URL + "/dashboard'")
except:
    print('📛')
    print('---')
    print("No monitor! | color='red'")
    print("Click here to configure | href='file://%s'" % os.path.abspath('uptimekuma.30s.py'))
finally:
    api.disconnect()
