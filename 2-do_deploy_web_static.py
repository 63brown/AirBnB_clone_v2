#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers, using the function do_deploy"""

import os
from os.path import exists
from fabric.api import env, put, run


env.hosts = ['100.26.177.16', '100.26.9.154']  # Replace with your own IP addresses


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    """
    # Check if the archive file exists
    if not exists(archive_path):
        return False

    # Get the name of the archive
    archive_name = os.path.basename(archive_path)

    # Define the remote paths
    remote_archive = '/tmp/{}'.format(archive_name)
    remote_folder = '/data/web_static/releases/{}'.format(archive_name.split('.')[0])

    # Upload the archive to the remote server
    put(archive_path, remote_archive)

    # Create the folder to store the archive
    run('sudo mkdir -p {}'.format(remote_folder))

    # Uncompress the archive into the folder
    run('sudo tar -xzf {} -C {}'
        .format(remote_archive, remote_folder))

    # Remove the archive from the remote server
    run('sudo rm {}'.format(remote_archive))

    # Move the contents of the folder to the parent folder
    run('sudo mv {}/* {}'.format(remote_folder, remote_folder+'/..'))

    # Remove the original folder
    run('sudo rm -rf {}'.format(remote_folder))

    # Remove the existing symbolic link
    run('sudo rm -rf /data/web_static/current')

    # Create a new symbolic link to the new version
    run('sudo ln -s {} /data/web_static/current'
        .format(remote_folder+'/'))

    return True