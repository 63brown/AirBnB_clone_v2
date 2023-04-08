from fabric.api import env, local
from os.path import exists
from datetime import datetime

# Define the environment
env.user = 'ubuntu'
env.hosts = ['100.26.177.16', '100.26.9.154']  # Replace with your own IP addresses

def do_pack():
    """
    Creates an archive of the web_static folder.
    """
    now = datetime.now()
    local('mkdir -p versions')
    file_path = 'versions/web_static_{}{}{}{}{}{}.tgz'.format(now.year,
                                                              now.month,
                                                              now.day,
                                                              now.hour,
                                                              now.minute,
                                                              now.second)
    local('tar -cvzf {} web_static'.format(file_path))

    if exists(file_path):
        return file_path
    else:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    """
    # Check if the archive file exists
    if not exists(archive_path):
        return False

    # Get the name of the archive
    archive_name = archive_path.split('/')[-1]

    # Define the remote paths
    remote_archive = '/tmp/{}'.format(archive_name)
    remote_folder = '/data/web_static/releases/{}'.format(
        archive_name.replace('.tgz', ''))

    # Upload the archive to the remote server
    put(archive_path, remote_archive)

    # Create the folder to store the archive
    run('sudo mkdir -p {}'.format(remote_folder))

    # Uncompress the archive into the folder
    run('sudo tar -xzf {} -C {}'
        .format(remote_archive, remote_folder))

    run('sudo rm {}'.format(remote_archive))

    run('sudo mv {}/* {}'.format(remote_folder, remote_folder+'/..'))
    run('sudo rm -rf {}'.format(remote_folder))
    run('sudo rm -rf /data/web_static/current')
    run('sudo ln -s {} /data/web_static/current'
        .format(remote_folder+'/'))

    return True

def deploy():
    """
    Creates and distributes an archive to your web servers.
    """
    # Create the archive
    archive_path = do_pack()
    if archive_path is None:
        return False

    # Deploy the archive
    return do_deploy(archive_path)
