import click


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
def parse_port_number_from_host(val):
    return 443 if 'saas' in val else 8090


# set prompt default for account-name
def parse_account_name_from_host(val):
    return val.split('.')[0] if 'saas' in val else 'customer1'


# to visualize end of sections
def end_section():
    click.echo('--------------------------------------------------------------------------------')
