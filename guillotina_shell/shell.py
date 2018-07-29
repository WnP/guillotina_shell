import traceback
from pprint import pprint as pp

from requests.exceptions import ConnectionError
from guillotina_client.client import BasicAuthClient
from guillotina_client.exceptions import (
    AlreadyExistsException,
    NotExistsException,
    UnauthorizedException,
    RetriableAPIException,
    LoginFailedException,
    RefreshTokenFailedException,
)

from .cmd_base import CmdBase

error = '\033[0;31mError\033[0m: '


class Gsh(CmdBase):
    intro = "Welcome to guillotina shell. Type help or ? to list commands.\n"
    prompt = 'gsh> '

    def __init__(self, config, *args, **kwargs):
        self.g = BasicAuthClient(config.url, config.user, config.password)
        self.path = []
        self.config = config
        return super().__init__(*args, **kwargs)

    def do_cd(self, arg):
        '''Change directory by navigating thru the resource tree'''
        if not arg or arg == '/':
            self.prompt = 'gsh> '.format(arg)
            self.path = []
        else:
            path_ = [p for p in arg.split('/') if p]
            path = []
            for p in path_:
                if p == '..':
                    if len(self.path):
                        self.path = self.path[:-1]
                    else:
                        print(error + 'Invalid path')
                elif p != '.':
                    path.append(p)

            if arg.startswith('/'):
                self.path = path
            else:
                self.path.extend(path)

        if self.path:
            self.prompt = 'gsh@{}> '.format('/' + '/'.join(self.path))
        else:
            self.prompt = 'gsh> '

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
                self.g.server, '/'.join(current_path), '@ids'))

    def do_ls(self, arg):
        '''Display current resource tree node'''
        if arg == '@addons':
            if len(self.path) < 2:
                print(error + 'Not a container path')
            else:
                self.g.set_container(self.path[1], db=self.path[0])
                pp(self.g.container.list_addons())
        else:
            path = self.path[:]
            path.extend(arg.split('/'))
            try:
                res = self.g.get_request('{}/{}'.format(
                    self.g.server, '/'.join(path)))
            except Exception as e:
                self.handle_exception(e)
            else:
                pp(res)

    def complete_ls(self, text, line, begidx, endidx):
        res = []
        if len(self.path) >= 2:
            # FIXME:
            # adding an extra blank entry in order to display '@' entries
            res.extend(['', '@addons', '@ids', '@items', '@sharing'])
            try:
                res.extend(self.g.get_request('{}/{}/{}'.format(
                    self.g.server, '/'.join(self.path), '@ids')))
            except Exception:  # noqa
                res.remove('@ids')
                res.remove('@items')
        return res

    @property
    def current_url(self):
        path = '/'.join(self.path)
        return f'{self.g.server}/{path}'

    def do_create(self, arg):
        '''Create a new child resource by providing json as argument'''
        try:
            res = self.g.post_request(self.current_url, data=arg)
        except Exception as e:
            self.handle_exception(e)
        else:
            pp(res)

    def do_update(self, arg):
        '''Update current resource by providing json as argument'''
        try:
            res = self.g.patch_request(self.current_url, data=arg)
        except Exception as e:
            self.handle_exception(e)
        else:
            pp(res)

    def do_delete(self, arg):
        '''Delete current resource and "cd" to parent'''
        try:
            res = self.g.delete_request(self.current_url)
        except Exception as e:
            self.handle_exception(e)
        else:
            self.do_cd('..')
            pp(res)

    def handle_exception(self, exception):
        print_trace = False
        if isinstance(exception, AlreadyExistsException):
            print(error + 'Already  exists')
        elif isinstance(exception, NotExistsException):
            print(error + 'Does not exists')
        elif isinstance(exception, UnauthorizedException):
            print(error + 'Unauthorized')
        elif isinstance(exception, RetriableAPIException):
            print_trace = True
            print(error + 'Retriable API')
        elif isinstance(exception, LoginFailedException):
            print(error + 'Login failed')
        elif isinstance(exception, RefreshTokenFailedException):
            print(error + 'Refresh token failed')
        elif isinstance(exception, ConnectionError):
            print_trace = True
            print(error + 'Connection error')
        else:
            print_trace = True
        if print_trace:
            formatted_lines = traceback.format_exc().splitlines()
            if self.config.debug:
                for line in formatted_lines:
                    print(line)
            else:
                print(formatted_lines[-1])
