import subprocess


# TODO: Make more cross-platform - start and verify are specific to Mac

def ext_cmd_build(item):
    if not verify_running_docker():
        start_docker()
    cmds = []
    for container in get_container(item):
        cmds.append(f"docker logs --tail=0 -f {container}")
    return cmds


def get_container(name):
    cmd = f'docker ps | grep {name}' + ' | awk \'{print $1}\''
    if containers := str(subprocess.check_output(cmd, shell=True).decode('utf-8').strip()).split('\n'):
        return containers
    return None


def start_docker():
    out = subprocess.run(['open', '-a', 'Docker'])
    if out.returncode == 0:
        return True
    return False


def verify_running_docker():
    down_output = 'Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?'
    out = subprocess.getstatusoutput('docker ps')[1]
    if out == down_output:
        return False
    return True
