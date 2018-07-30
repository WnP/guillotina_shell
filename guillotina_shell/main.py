#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdb
import sys

from .shell import Gsh


def main():
    from .config import config

    try:
        Gsh(config).cmdloop()
    except Exception:
        _, _, tb = sys.exc_info()
        pdb.post_mortem(tb)


if __name__ == "__main__":
    main()
