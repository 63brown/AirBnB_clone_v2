#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""

import os
from datetime import datetime
from fabric.api import local

def do_pack():
    if not os.path.exists("versions"):
        os.makedirs("versions")

    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    filepath = os.path.join('versions', archive_name)
    try:
        local("tar -cvzf versions/{} web_static".format(filepath))
        return "versions/{}".format(filepath)
    except:
        return None