import subprocess


def ext_cmd_build(item):
    cmds, in_pods = [], []
    context, oc_item = get_context(item)
    if context == 'pod':
        in_pods.append(item)
    if in_pods:
        cmds = [f'kubectl logs --tail=0 -f pod/{pod}' for pod in get_pods(in_pods)]
    return cmds


def get_context(in_arg):
    arg_list = in_arg.split('/')
    return arg_list[0].lower(), arg_list[1]


def get_pods(in_arg):
    found_pods = []
    pods = str(subprocess.check_output('kubectl get pods | grep -v NAME | awk \'{print $1}\'',
                                       shell=True).decode('utf-8').strip()).split('\n')
    for value in in_arg:
        value = value.split('/')[-1]
        for pod in pods:
            if value in pod:
                found_pods.append(pod)
    return found_pods
