# Guillotina Shell

This is a POC for a future
[guillotina](https://github.com/plone/guillotina) shell.

The project is heavily based on
[guillotina_client](https://github.com/guillotinaweb/guillotina_client)
and python [cmd](https://docs.python.org/3/library/cmd.html) module.

## Install

```
git clone https://github.com/WnP/guillotina_shell
cd guillotina_shell
pip install -r requirements.txt
pip install .
```

## Usage

```
$ gsh -h

usage: gsh [-h] [--url URL] [-u USER] [-p PASSWORD] [-d]

gsh: The Guillotina shell

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Guillotina url (default: http://localhost:8083)
  -u USER, --user USER  Basic auth user (default: root)
  -p PASSWORD, --password PASSWORD
                        Basic auth password (default: root)
  -d, --debug           Debug mode (default: False)

Set environment variables using GSH_ prefix
```

Available commands:

- `?` or `help`: to display all available commands, pass command name as argument to display command help.
- `ls`: display node content (tab completion available).
- `cd`: change resource tree location (tab completion available).
- `create`: create new resource.
- `update`: update resource.
- `delete`: delete resource.
- `endpoint`: query resource endpoints.

## Contribute

Issues and PRs are welcome!

## License

MIT
