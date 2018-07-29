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

Run the newly installed `gsh` command:

```
gsh -h

usage: gsh [-h] [--url URL] [-u USER] [-p PASSWORD]

gsh: The Guillotina shell

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Guillotina url (default: http://localhost:8080)
  -u USER, --user USER  Basic auth user (default: root)
  -p PASSWORD, --password PASSWORD
                        Basic auth password (default: root)

Set environment variables using GSH_ prefix
```

Once logged use `cd` and `ls` commands, both provide tab completion.

## Contribute

Issues and PRs are welcome!

## License

MIT
