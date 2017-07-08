# encoding=utf-8
import os
import shlex
import subprocess


def execute_cmd(cmd, cwd=None, env=None):
    print(cmd)
    my_env = os.environ.copy()

    if env:
        my_env.update(env)
    output = subprocess.check_output(shlex.split(cmd), shell=False, cwd=cwd, env=my_env).decode('utf-8')

    return output


def execute_cmds(items=[]):
    if not items:
        return []

    return [execute_cmd(**_) for _ in items]
