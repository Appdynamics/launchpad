import logging

from click import Context
from colorama import init as colorama_init, Fore

from appd_api.appd_controller_service import AppDControllerService
from routines.routine import all_options
from routines.routine_runner import begin_routine
from appd_api.appd_controller import ApiError
from util.click_utils import end_section, appd_api
from util.sys_utils import exit_with_message
from util.logging_wrapper import httpclient_logging

import click


@appd_api
def main(host: str, port: int, ssl: bool, accountname: str, username: str, pwd: str):
    """
    Automate AppDynamics Application onboarding activities.
    """

    # Print splash image
    f = open("resources/splash.txt")
    click.echo(f"{f.read()}")
    end_section()

    controller_service = AppDControllerService(host, port, ssl, accountname, username, pwd)
    result = controller_service.login_to_controller()

    if result.error is not None:
        exit_with_message(f"Controller Login Failed With Code {result.error.msg}")
    else:
        logging.info(f"Successfully Connected to Controller {host}")
        click.echo(Fore.GREEN + f"Successfully Connected to Controller {host}")
    end_section()

    # Initialization successful, begin main routine.
    logging.info("Initialization successful, begin main routine.")
    begin_routine(controller_service, all_options)


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
