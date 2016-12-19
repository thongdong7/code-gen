# encoding=utf-8
from copy import copy
from os.path import join, exists, abspath

from tornado.gen import sleep

from code_gen.monitor import FileMonitor, FileMonitorPool
from code_gen.provider.template import TemplateProvider
from code_gen.renderer import Renderer
from code_gen.template_engine import TemplateEngine
from code_gen.utils.template_utils import generate


class CodeGenerator(object):
    def __init__(self, path, output_dir):
        self.path = abspath(path)
        self.template = TemplateProvider().get(path)
        self.output_dir = output_dir

        #
        self.renderer = Renderer()

    def generate(self, watch=False):
        self._generate()

        if watch:
            file_monitor = FileMonitor(self._on_change)
            print('Watch folders', self.template.paths)
            file_monitor.watch_multiple(self.template.paths)

            pool = FileMonitorPool()
            pool.add_file_monitor(file_monitor)
            pool.start()

            while True:
                sleep(1000)

    def _on_change(self, path):
        print('%s changed' % path)
        self._generate()

    def _generate(self):
        print('Generating...')
        # Reload parameters
        self.template = TemplateProvider().get(self.path)

        # TODO Check changed path to decide to reload parameters or not
        params = self.template.parameters

        engine = TemplateEngine(self.template)

        # Generate master
        self._generate_master(engine, params)

        # Generate item
        for item_name in params:
            for path in self.template.paths:
                item_dir = join(path, 'items', item_name)
                if exists(item_dir):
                    for item_config in params[item_name]:
                        item_params = copy(item_config)
                        item_params['params'] = params

                        generate(template_dir=item_dir,
                                 params=item_params,
                                 output_dir=self.output_dir,
                                 override=self.template.config.override,
                                 engine=engine)

        # TODO Generate items
        print('Done!')

    def _generate_master(self, engine, params):

        for path in self.template.paths:
            print('  > %s' % path)
            template_dir = join(path, 'master')
            if not exists(template_dir):
                continue

            generate(template_dir=template_dir, params=params, output_dir=self.output_dir,
                     override=self.template.config.override, engine=engine)
