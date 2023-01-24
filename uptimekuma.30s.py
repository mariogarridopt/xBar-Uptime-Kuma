#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# <xbar.title>UptimeKuma Monitor</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>mariogarridopt</xbar.author>
# <xbar.author.github>mariogarridopt</xbar.author.github>
# <xbar.desc>Show UptimeKuma status</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/mariogarridopt/xBar-Uptime-Kuma</xbar.abouturl>
# <xbar.image>https://raw.githubusercontent.com/mariogarridopt/xBar-Uptime-Kuma/master/screenshot.png</xbar.image>

import requests
import json
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

# Set your API Key here!
# Get your API Key in https://...
api_key = 'CHANGE_HERE!!'

# soon ...
