# encoding=utf-8
import os
import subprocess
from os.path import join, exists, abspath, dirname

from tornado.gen import sleep

from zander.monitor import FileMonitor, FileMonitorPool
from zander.provider.template import TemplateProvider
from zander.renderer import Renderer
from zander.template_engine import TemplateEngine
from zander.utils.cmd_utils import execute_cmds
from zander.utils.template_utils import generate


class CodeGenerator(object):
    def __init__(self, project_dir, output_dir):
        self.project_dir = abspath(project_dir)
        self.template = None
        self.output_dir = output_dir

        #
        self.renderer = Renderer()

    def generate(self, watch=False):
        self._generate()

        if watch:
            file_monitor = FileMonitor(self._on_change)
            print('Watch folders %s' % ' and '.join(self.template.paths))
            file_monitor.watch_multiple(self.template.paths)

            pool = FileMonitorPool()
            pool.add_file_monitor(file_monitor)
            pool.start()

            while True:
                sleep(1000)

    def _on_change(self, path):
        print('%s changed' % path)

        # Run a process to generate instead of call self._generate(reload=True) to avoid macro catch issue
        current_dir = abspath(dirname(__file__))
        script_file = join(current_dir, 'scripts.py')

        subprocess.Popen(["python", script_file], env=os.environ)
        # print('aaa')
        # self._generate(reload=True)

    def _generate(self, reload=False):
        if reload or not self.template:
            # Reload parameters
            self.template = TemplateProvider().get(self.project_dir)

        # TODO Check changed path to decide to reload parameters or not
        params = self.template.parameters

        engine = TemplateEngine(self.template, project_dir=self.project_dir)

        # Call params decor
        params = engine.decor_params(params)

        # Generate master
        self._generate_master(engine, params)

        # Generate item
        for item_name in params:
            for path in self.template.paths:
                item_dir = join(path, 'items', item_name)
                if exists(item_dir):
                    for item_config in params[item_name]:
                        item_params = {
                            'params': params,
                        }

                        if isinstance(item_config, dict):
                            item_params.update(item_config)
                        else:
                            # Item config is an object
                            for field in item_config.__dict__.keys():
                                item_params[field] = getattr(item_config, field)

                        generate(template_dir=item_dir,
                                 params=item_params,
                                 output_dir=self.output_dir,
                                 override=self.template.config.override,
                                 engine=engine)

        # Run postcmd
        execute_cmds(self.template.config.postcmd)

    def _generate_master(self, engine, params):
        for path in self.template.paths:
            # print('  > %s' % path)
            template_dir = join(path, 'master')
            if not exists(template_dir):
                continue

            generate(template_dir=template_dir, params=params, output_dir=self.output_dir,
                     override=self.template.config.override, engine=engine)
