import json
import click
import sys
import yaml
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from cli.utils import exception_handler, wowza_auth
from cli.database import Database
from wowpy.resources import get_resource_info
from wowpy.resources import validate_resource
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def resource():
    """
    Resource commands.
    """
    pass


@resource.command(name='validator')
@click.option('--spec-file', required=True, type=click.File(lazy=False),
              help='File that contains your streaming resource specification')
@exception_handler
def validator(spec_file):
    """Validate streaming resource specification"""
    specification = yaml.load(spec_file, Loader=yaml.SafeLoader)
    valid = validate_resource(specification)
    if not valid:
        click.echo('The specification template is invalid')
    else:
        click.echo('The specification template is valid')


@resource.command(name='query')
@optgroup.group('Resource identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for resource')
@optgroup.option('--id', help='Resource stream id')
@optgroup.option('--name', help='Resource stream name')
@exception_handler
def query(id, name):
    """Get data for a resource"""
    wowza_auth()
    if name:
        database = Database()
        if not database.live_streams_table_exist():
            click.echo('In order to use --name parameter please run: wowtool mapper live_streams, first')
            sys.exit()

        id = database.get_live_stream_id_from_name(name)
        if not id:
            click.echo('Live stream not found in current mapping table')
            sys.exit()
    response = get_resource_info(id)
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json, JsonLexer(), TerminalTrueColorFormatter(style='solarized-dark'))
    click.echo(colorful_json)