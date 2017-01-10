import traceback

import click


def print_exception(e, debug=False):
    message = "Fatal Error: {0}".format(
        str(e)
    )

    if debug:
        message += '\n' + traceback.format_exc()

    click.secho(message, fg='red', err=True)
