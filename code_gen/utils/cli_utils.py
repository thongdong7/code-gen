import click


def print_exception(e):
    message = "Fatal Error: {0}".format(
        str(e)
    )

    click.secho(message, fg='red', err=True)
