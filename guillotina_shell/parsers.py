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


# Endpoint

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

# cd

cd_parser = GshCommandParser(
    prog="cd",
    description='Change directory by navigating thru the resource tree',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

cd_parser.add_argument('path', help='Requested path')

# ls

ls_parser = GshCommandParser(
    prog="ls",
    description='Display current resource tree node',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

ls_parser.add_argument('path', default='', nargs='?', help='Requested path')

# create

create_parser = GshCommandParser(
    prog="create",
    description='Create a new child resource by providing json as argument',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

create_parser.add_argument('data', help='JSON data')

# delete

delete_parser = GshCommandParser(
    prog="delete",
    description='Delete current resource and "cd" to parent',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# update

update_parser = GshCommandParser(
    prog="update",
    description='Update current resource by providing json as argument',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

update_parser.add_argument('data', help='JSON data')
