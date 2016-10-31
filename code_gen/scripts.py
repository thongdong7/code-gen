# encoding=utf-8
import logging
from os.path import exists

import click
from code_gen.generator import CodeGenerator
from code_gen.init import InitTemplate
from code_gen.install import DependencyInstaller

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
def cli(ctx, app_dir):
    if ctx.invoked_subcommand is None:
        # Generate
        print('Generating...')
        try:
            generator = get_generator(app_dir)
            generator.generate()
            print('Done!')
        except Exception as e:
            print(str(e))
            raise


@cli.command(help='Install dependencies')
@click.option('--app-dir', 'app_dir', default='.', help='Application directory. Default is the current directory')
def install(app_dir):
    print('Installing...')
    try:
        installer = DependencyInstaller(app_dir)
        installer.install()
        print('Done!')
    except Exception as e:
        print(str(e))
        raise


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
        print(str(e))
        raise

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
