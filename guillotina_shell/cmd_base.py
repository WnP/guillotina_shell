import cmd


class CmdBase(cmd.Cmd):
    '''A more suitable shell that the default one provided by cmd module'''

    def cmdloop(self, *args, **kwargs):
        '''Don't throw an error on Ctrl-c'''
        while True:
            try:
                super().cmdloop(*args, **kwargs)
                break
            except KeyboardInterrupt:
                self.intro = ''
                print()

    def do_EOF(self, *args, **kwargs):
        '''Exit on Ctrl-d'''
        print()
        return self.do_exit()

    def get_names(self, *args, **kwargs):
        '''Don't display EOF in command help list'''
        names = super().get_names(*args, **kwargs)
        names.remove('do_EOF')
        return names

    def do_exit(self, *arg, **kwargs):
        '''Exit guillotina shell, also called on Ctrl-d'''
        print('Bye')
        return True
