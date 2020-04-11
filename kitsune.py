#!/usr/local/bin/python3

# https://en.wikipedia.org/wiki/Kitsune

import os
import random
import subprocess

import importlib
import click

from objs.tmux_obj import Tmux
from utilities import get_configs


def cmd_build(item, home, tool, in_color):
    cmds = []
    verify_tool(tool)
    if tool == 'tail':
        cmds.append(f'''tail -n 0 -f {item} | sed "s/^/"{sed_build_prefix(item.split('/')[-1], in_color)}/g &''')
    elif f'{tool}.py' in os.listdir(f'{home}/tools/'):  # Allows for extensions to be added through ./tools/
        module = importlib.import_module(f'tools.{tool}', package='ext_cmd_build')
        for cmd in module.ext_cmd_build(item):
            if '/' in item:
                item = item.split('/')[-1]
            cmds.append(f'''{cmd} | sed "s/^/"{sed_build_prefix(item, in_color)}/g &''')
    else:
        print('The referenced tool is not valid within kitsune.')
    return cmds


def cmd_kill(tmux, item):
    # TODO: Do this better - bug with missing item
    # TODO: Remove session if this is the last job
    kill_cmd = f"kill %$(jobs | grep {item}" + " | awk '{print $1}' | cut -d [ -f 2 | cut -d ] -f 1)"
    subprocess.call(['tmux', 'send-keys', '-t', tmux.pane, kill_cmd, 'Enter'])


def sed_build_prefix(prefix, in_color):
    # TODO: Verify colors aren't already in use
    colors = {'blue': '[34m', 'green': '[32m', 'cyan': '[36m', 'red': '[31m', 'purple': '[35m', 'brown': '[33m',
              'gray': '[37m', 'dark_gray': '[30m', 'light_blue': '[34m', 'light_green': '[32m', 'light_cyan': '[36m',
              'light_red': '[31m', 'light_purple': '[35m', 'yellow': '[33m', 'white': '[37m'}
    color_choice = random.choice(list(colors.items()))[1] if not in_color else colors[in_color.lower()]
    # print(f'\033{color_choice}test\033[0m')  # Prints colored test in pycharm
    return f"$'\\033{color_choice}{prefix}: \\033[0m'"


@click.command()
@click.argument('name')
@click.option('--color', '-c', default=None, help='The color to use for the tail. '
                                                  '<blue|green|cyan|red|purple|brown|gray|dark_gray|light_blue|'
                                                  'light_green|light_cyan|light_red|light_purple|yellow|white>')
@click.option('--remove', '-r', is_flag=True, help='Remove a tail.')
@click.option('--tool', '-t', default='tail', help='The tool to use for the tail.')
def main(name, color, remove, tool):
    settings = get_configs()
    tmux = Tmux(settings['kitsune']['tmux']['session_name'])
    if tmux.verify_session():
        tmux.build_session()

    if remove:
        print(f'Removing {name} from {tmux.session} session')
        cmd_kill(tmux, name)
    else:
        for cmd in cmd_build(name, settings['kitsune']['home'], tool.lower(), color):
            print(f'Adding {name} to {tmux.session} session')
            tmux.cmd_call(cmd)


def verify_tool(name):
    if subprocess.getstatusoutput(f'which {name}')[0]:
        print(f'{name} tool not locally installed.')
        exit(0)


if __name__ == '__main__':
    main()
