from os.path import join, exists

from zander.provider.template import TemplateProvider
from zander.template_engine import TemplateEngine
from zander.utils.template_utils import generate


def dependency_render(name, params, target_dir, override=True, **kwargs):
    """
    Render a dependency

    :param name:
    :param params:
    :param target_dir:
    :return:
    """
    template = TemplateProvider().get_dependency(name)
    template.config.override = override
    engine = TemplateEngine(template, project_dir=target_dir)

    _render(engine, template, params, target_dir, **kwargs)


def _render(engine, template, params, output_dir, **kwargs):
    # Master
    for path in template.paths:
        print('  > %s' % path)
        template_dir = join(path, 'master')
        if not exists(template_dir):
            continue

        generate(template_dir=template_dir, params=params,
                 output_dir=output_dir,
                 override=template.config.override, engine=engine,
                 **kwargs)

    # Generate item
    for item_name in params:
        for path in template.paths:
            item_dir = join(path, 'items', item_name)
            if exists(item_dir):
                for item_config in params[item_name]:
                    item_params = item_config.copy()
                    item_params['params'] = params

                    generate(template_dir=item_dir,
                             params=item_params,
                             output_dir=output_dir,
                             override=template.config.override,
                             engine=engine,
                             **kwargs)
