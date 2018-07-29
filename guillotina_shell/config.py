import argparse

from .env_default import env_default


parser = argparse.ArgumentParser(
    description='gsh: The Guillotina shell',
    epilog='Set environment variables using GSH_ prefix',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    '--url', type=str, default='http://localhost:8080',
    action=env_default('URL'),
    help='Guillotina url')

parser.add_argument(
    '-u', '--user', type=str, default='root',
    action=env_default('USER'),
    help='Basic auth user')

parser.add_argument(
    '-p', '--password', type=str, default='root',
    action=env_default('PASSWORD'),
    help='Basic auth password')

parser.add_argument(
    '-d', '--debug', help='Debug mode', action='store_true')
parser.set_defaults(debug=False)

config = parser.parse_args()
