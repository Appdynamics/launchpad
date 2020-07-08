import logging

from colorama import init as colorama_init

from routines.routine import begin_routine
from util.appd_api.appd_api import AppdApi, ApiError
from util.click_utils import DynamicOptionPrompt, parse_account_name_from_host, parse_port_number_from_host, end_section
from util.yaspin_utils import as_spinner
from util.logging_wrapper import httpclient_logging

import click


@click.command()
@click.option('--host',
              prompt=True,
              help='acme.saas.appdynamics.com')
@click.option('--port',
              prompt=True,
              cls=DynamicOptionPrompt,
              default_option='host',
              default=lambda x: parse_port_number_from_host(x),
              help="""
              \b
              SaaS: 443
              On Prem: 8090""")
@click.option('--ssl/--no-ssl',
              prompt=True,
              is_flag=True,
              default=True)
@click.option('--accountname',
              prompt=True,
              cls=DynamicOptionPrompt,
              default_option='host',
              default=lambda x: parse_account_name_from_host(x),
              help="""
              \b
              SaaS: first segment of controller host
              On Prem: customer1""")
@click.option('--username',
              prompt=True,
              help='must use local account')
@click.option('--password',
              prompt=True,
              hide_input=True)
def main(host: str, port: int, ssl: bool, accountname: str, username: str, password: str):
    """
    This program automates many common AppDynamics Application onboarding activities.
    """

    # Print splash image
    f = open("resources/splash.txt")
    click.echo(f"{f.read()}")
    end_section()

    logging.info("Attempt controller connection.")
    connection_url = f'{"https" if ssl else "http"}://{host}:{port}'
    auth = (f'{username}@{accountname}', password)
    controller = AppdApi(base_url=connection_url, auth=auth)
    response = as_spinner(fn=controller.login, text=f"Attempting Login for Controller {host}")
    if response.status_code is not 200:
        click.echo(f"Controller Login Failed With Code {response.status_code}")
        logging.error(f"Controller Login Failed With Code {response.status_code}")
        click.echo("Exiting")
        logging.error("Exiting")
        return
    else:
        logging.info(f"Successfully Logged into controller {host}")
        click.echo(f"Successfully Logged into controller {host}")
    end_section()

    # Initialization successful, begin main routine.
    logging.info("Initialization successful, begin main routine.")
    begin_routine(controller)


if __name__ == '__main__':
    logging.basicConfig(filename='logs/launchpad.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')
    colorama_init(autoreset=True)
    httpclient_logging()

    try:
        main()
    except ApiError as err:
        click.echo(err)
        click.echo("Exiting.")
