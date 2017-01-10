# encoding=utf-8
import logging
from os.path import exists

import click
import sys

from zander.generator import CodeGenerator
from zander.init import InitTemplate
from zander.install import DependencyInstaller
from zander.utils.cli_utils import print_exception

logging.basicConfig(level=logging.DEBUG)


class InvalidAppDirError(Exception):
    def __str__(self):
        return "Application directory %s does not exists" % self.args[0]


class InvalidTemplateDirError(Exception):
    def __str__(self):
        return "Could not find template directory at %s" % self.args[0]


def get_generator(app_dir):
    if not exists(app_dir):
        raise InvalidAppDirError(app_dir)

    return CodeGenerator(app_dir, app_dir)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--app-dir', 'app_dir', default='.', help='Application directory. Default is the current directory')
@click.option('--watch', '-w', 'watch', is_flag=True, help='Run as daemon')
@click.option('--debug', 'debug', is_flag=True, help='Debug')
def cli(ctx, app_dir, watch, debug):
    if ctx.invoked_subcommand is None:
        # Generate
        try:
            generator = get_generator(app_dir)
            generator.generate(watch=watch)
            print('Done!')
        except Exception as e:
            print_exception(e, debug=debug)

            sys.exit(1)


@cli.command(help='Install dependencies')
@click.option('--app-dir', 'app_dir', default='.', help='Application directory. Default is the current directory')
@click.option('--debug', 'debug', is_flag=True, help='Debug')
def install(app_dir, debug):
    print('Installing...')
    try:
        installer = DependencyInstaller(app_dir)
        installer.install()
        print('Done!')
    except Exception as e:
        print_exception(e, debug=debug)

        sys.exit(1)


@cli.command(help='Init template')
@click.argument('template_name')
@click.option('--app-dir', 'app_dir', default='.', help='Application directory. Default is the current directory')
def init(template_name, app_dir):
    print('Init template %s...' % template_name)
    try:
        action = InitTemplate(template_name, app_dir)
        action.execute()
        print('Done!')
    except Exception as e:
        print_exception(e)

        sys.exit(1)

# @click.command(help='Generate')
# @click.option('--app-dir', 'app_dir', default='.', help='Application directory. Default is the current directory')
# @click.option('--template-dir-name', 'template_dirname', default='template',
#               help='Template directory name, default "template"')
# def code_gen_old(app_dir, template_dirname):
#     try:
#         if not exists(app_dir):
#             raise InvalidAppDirError(app_dir)
#
#         template_dir = join(app_dir, template_dirname)
#         if not exists(template_dir):
#             raise InvalidTemplateDirError(template_dir)
#
#         generate_all(template_dir, output_dir=app_dir)
#     except Exception as e:
#         print(str(e))
#         raise
