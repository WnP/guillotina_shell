#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .shell import Gsh


def main():
    from .config import config

    Gsh(config).cmdloop()


if __name__ == "__main__":
    main()
