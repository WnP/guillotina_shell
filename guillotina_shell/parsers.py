import argparse


class GshCommandParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        self.errored = False
        return super().__init__(*args, **kwargs)

    def exit(self, *args, **kwargs):
        self.errored = True

    def parse_args(self, *args, **kwargs):
        res = super().parse_args(*args, **kwargs)
        if self.errored:
            self.errored = False
            return None
        return res


endpoint_parser = GshCommandParser(
    prog="endpoint",
    description='Query current node endpoints.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

endpoint_parser.add_argument(
    'name', default='', nargs='?',
    help='Endpoint name, if not provided will display all available endpoints'
    'with descriptions')

endpoint_parser.add_argument(
    '-m', '--http-method', choices=['get', 'post', 'patch', 'delete'],
    default='get', help='HTTP method used to query endpoint')

endpoint_parser.add_argument(
    'data', type=str, default='', nargs='?',
    help='Data sent to endpoints')
