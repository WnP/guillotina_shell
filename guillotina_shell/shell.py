import traceback
import shlex
import pdb
import sys
from pprint import pprint

from requests.exceptions import ConnectionError
from guillotina_client.client import BasicAuthClient
from guillotina_client.api import Resource
from guillotina_client.exceptions import (
    AlreadyExistsException,
    NotExistsException,
    UnauthorizedException,
    RetriableAPIException,
    LoginFailedException,
    RefreshTokenFailedException,
)

from .cmd_base import CmdBase
from .node import Node
from .parsers import (
    cd_parser,
    ls_parser,
    endpoint_parser,
    create_parser,
    update_parser,
    delete_parser,
)


def join(*args):
    return '/'.join(args)


class Gsh(CmdBase):
    intro = "Welcome to guillotina shell. Type help or ? to list commands.\n"
    prompt = 'gsh> '

    def __init__(self, config, *args, **kwargs):
        self.g = BasicAuthClient(config.url, config.user, config.password)
        self.path = []
        self.config = config
        self.current = None
        self.ids = []
        self.get_current()
        return super().__init__(*args, **kwargs)

    @property
    def current_path(self):
        return join(*self.path)

    def current_url(self, path=''):
        if not path:
            path = self.current_path
        elif not path.startswith('/'):
            path = join(self.current_path, path)
        return f'{self.g.server}/{path}'

    def get_current(self):
        if len(self.path) <= 2:
            try:
                self.current = Node(self.current_url(), self.g)
            except NotExistsException:
                self.print_error(
                    'Please install guillotina-swagger onto your '
                    'application in order to improve your user experience')
            except Exception as e:
                self.handle_exception(e)
        if len(self.path) > 2:
            try:
                self.current = Resource(self.current_url(), self.g)
            except NotExistsException:
                self.print_error(
                    'Please install guillotina-swagger onto your '
                    'application in order to improve your user experience')
            except Exception as e:
                self.handle_exception(e)

    def get_ids(self):
        if self.current and '@ids' in self.current.endpoints:
            try:
                ids = self.g.get_request('{}/{}/{}'.format(
                    self.g.server, self.current_path, '@ids'))
            except Exception:  # noqa
                self.ids = []
            else:
                self.ids = ids

    def do_cd(self, arg):
        '''Change directory by navigating thru the resource tree'''
        args = cd_parser.parse_args(shlex.split(arg))
        if args is None:
            return
        if not args.path or args.path == '/':
            self.prompt = 'gsh> '.format(args.path)
            self.path = []
        else:
            path_ = [p for p in args.path.split('/') if p]
            path = []
            for p in path_:
                if p == '..':
                    if len(self.path):
                        self.path = self.path[:-1]
                    else:
                        self.print_error('Invalid path')
                elif p != '.':
                    path.append(p)

            if args.path.startswith('/'):
                self.path = path
            else:
                self.path.extend(path)

        if self.path:
            self.get_current()
            self.get_ids()
            self.prompt = 'gsh@{}> '.format('/' + self.current_path)
        else:
            self.current = None
            self.prompt = 'gsh> '

    def help_cd(self):
        cd_parser.print_help()

    def complete_cd(self, text, line, begidx, endidx):
        sl = line.split()
        path = sl[1].split('/') if len(sl) > 1 else []
        path = [p for p in path if p]

        if not self.path and not path:
            return ['/{}/'.format(db) for db in self.g.list_databases()]

        if max([len(self.path), len(path)]) == 1 \
                and len(self.path) != len(path):
            db = path[0] if path else self.path[0]

            return [
                '{}/'.format(container)
                if self.path else
                container
                for container in
                self.g.list_containers(db)]

        current_path = []
        if self.path:
            current_path = self.path[:]
        if path:
            current_path.extend(path)

        return self.g.get_request('{}/{}/{}'.format(
                self.g.server, join(*current_path), '@ids'))

    def do_ls(self, arg):
        '''Display current resource tree node'''
        args = ls_parser.parse_args(shlex.split(arg))
        if args is None:
            return
        if args.path == '@addons':
            if len(self.path) < 2:
                self.print_error('Not a container path')
            else:
                self.g.set_container(self.path[1], db=self.path[0])
                pprint(self.g.container.list_addons())
        else:
            path = self.path[:]
            path.extend(args.path.split('/'))
            try:
                res = self.g.get_request('{}/{}'.format(
                    self.g.server, join(*path)))
            except Exception as e:
                self.handle_exception(e)
            else:
                pprint(res)

    def help_ls(self):
        ls_parser.print_help()

    def complete_ls(self, text, line, begidx, endidx):
        # FIXME:
        # adding an extra blank entry in order to display '@' entries
        res = ['']
        if self.current:
            res.extend([
                e
                for e in getattr(self.current, 'endpoints', {}).keys()
                if e.startswith('@')])
        if self.ids:
            res.extend(self.ids)
        return res

    def do_create(self, arg):
        '''Create a new child resource by providing json as argument'''
        args = create_parser.parse_args(shlex.split(arg))
        if args is None:
            return
        try:
            res = self.g.post_request(
                self.current_url(args.path), data=args.data)
        except Exception as e:
            self.handle_exception(e)
        else:
            pprint(res)

    def help_create(self):
        create_parser.print_help()

    def do_update(self, arg):
        '''Update current resource by providing json as argument'''
        args = update_parser.parse_args(shlex.split(arg))
        if args is None:
            return
        try:
            res = self.g.patch_request(
                self.current_url(args.path), data=args.data)
        except Exception as e:
            self.handle_exception(e)
        else:
            pprint(res)

    def help_update(self):
        update_parser.print_help()

    def do_delete(self, arg):
        '''Delete current resource and "cd" to parent'''
        args = update_parser.parse_args(shlex.split(arg))
        if args is None:
            return
        try:
            res = self.g.delete_request(self.current_url(args.path))
        except Exception as e:
            self.handle_exception(e)
        else:
            self.do_cd('..')
            pprint(res)

    def help_delete(self):
        delete_parser.print_help()

    def do_endpoint(self, arg):
        args = endpoint_parser.parse_args(shlex.split(arg))
        if args is None:
            return
        if not args.name:
            for name, methods in self.current.endpoints.items():
                print(f'- {name}:')
                for verb, description in methods.summary.items():
                    print(f'    - {verb}: {description}')
            return
        if args.http_method == 'get':
            self.do_ls(args.name)
        elif args.http_method == 'post':
            self.do_create(f'{args.name} {args.data}')
        elif args.http_method == 'patch':
            self.do_update(f'{args.name} {args.data}')
        elif args.http_method == 'delete':
            self.do_delete(args.name)
        elif args.help:
            self.help_endpoint()

    def do_ep(self, arg):
        '''Alias for endpoint command'''
        return self.do_endpoint(arg)

    def help_endpoint(self):
        endpoint_parser.print_help()

    def print_error(self, error):
        print('\033[0;31mError\033[0m: ' + error)

    def handle_exception(self, exception):
        print_trace = False
        if isinstance(exception, AlreadyExistsException):
            self.print_error('Already  exists')
        elif isinstance(exception, NotExistsException):
            self.print_error('Does not exists')
        elif isinstance(exception, UnauthorizedException):
            self.print_error('Unauthorized')
        elif isinstance(exception, RetriableAPIException):
            print_trace = True
            self.print_error('Retriable API')
        elif isinstance(exception, LoginFailedException):
            self.print_error('Login failed')
        elif isinstance(exception, RefreshTokenFailedException):
            self.print_error('Refresh token failed')
        elif isinstance(exception, ConnectionError):
            print_trace = True
            self.print_error('Connection error')
        else:
            print_trace = True
        if print_trace or self.config.debug:
            formatted_lines = traceback.format_exc().splitlines()
            if self.config.debug:
                for line in formatted_lines:
                    print(line)
                _, _, tb = sys.exc_info()
                pdb.post_mortem(tb)
            else:
                print(formatted_lines[-1])
