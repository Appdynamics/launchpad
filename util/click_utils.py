import click


def composed(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f

    return deco


cli = click.Group()


def appd_api(func):
    return composed(
        cli.command(),
        click.option('--host',
                     prompt=True,
                     help='acme.saas.appdynamics.com'),
        click.option('--port',
                     prompt=True,
                     cls=DynamicOptionPrompt,
                     default_option='host',
                     default=lambda x: parse_port_number_from_host(x),
                     help="""
                  \b
                  SaaS: 443
                  On Prem: 8090"""),
        click.option('--ssl/--no-ssl',
                     prompt=True,
                     cls=DynamicOptionPrompt,
                     is_flag=True,
                     default_option='host',
                     default=lambda x: parse_is_ssl_from_host(x)),
        click.option('--accountname',
                     prompt=True,
                     cls=DynamicOptionPrompt,
                     default_option='host',
                     default=lambda x: parse_account_name_from_host(x),
                     help="""
                  \b
                  SaaS: first segment of controller host
                  On Prem: customer1"""),
        click.option('--username',
                     prompt=True,
                     help='must use local account'),
        click.option('--pwd',
                     prompt=True,
                     hide_input=True)
    )(func)


# modifies click.option behavior to allow for dynamic defaults based on previous user entered option
# default_option -> previous option we are using to dynamically generate current option default
# default -> lambda expression which evaluates default_option to generate current option default
# see launchpad.py for usage
class DynamicOptionPrompt(click.Option):
    _value_key = '_default_val'

    def __init__(self, *args, **kwargs):
        self.default_option = kwargs.pop('default_option', None)
        super(DynamicOptionPrompt, self).__init__(*args, **kwargs)

    def get_default(self, ctx):
        arg = ctx.params[self.default_option]
        default = self.type_cast_value(ctx, self.default(arg))
        setattr(self, self._value_key, default)
        return getattr(self, self._value_key)

    def prompt_for_value(self, ctx):
        return super(DynamicOptionPrompt, self).prompt_for_value(ctx)


# set prompt default for port number
def parse_port_number_from_host(port_number: int) -> int:
    return 443 if 'saas' in port_number else 8090


# set prompt default for account-name
def parse_account_name_from_host(host_name: str) -> str:
    return host_name.split('.')[0] if 'saas' in host_name else 'customer1'


# set prompt default for ssl
def parse_is_ssl_from_host(host_name: str) -> bool:
    """Only controllers without SSL should be on cloud machine"""
    return host_name.endswith('appd-cx.com') is not True


# to visualize end of sections
def end_section():
    click.echo('-------------------------------------------------------------------------------------------')
