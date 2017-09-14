# encoding=utf-8
import os
import shlex
import subprocess
from os.path import expanduser

from functional import seq

home = expanduser("~")


def _normalize_path(path):
    items = path.split(':')
    items = seq(items).map(lambda item: expanduser(item)).list()

    return ':'.join(items)


def execute_cmd(cmd, cwd=None, env=None, path=None):
    if cmd.startswith('~/'):
        cmd = cmd.replace('~/', '%s/' % home)

    print(cmd)
    my_env = os.environ.copy()

    if env:
        my_env.update(env)

    if path:
        my_env['PATH'] = _normalize_path(path) + ":" + my_env['PATH']
        # print(my_env['PATH'])

    output = subprocess.check_output(shlex.split(cmd), shell=False, cwd=cwd, env=my_env).decode('utf-8')

    return output


def execute_cmds(items=[]):
    if not items:
        return []

    return [execute_cmd(**_) for _ in items]
