#!/usr/bin/env python3
# Yonghang Wang
# yhang_wang@icloud.com

import os
import sys
import argparse
import re
from .ltexpect import LE

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', dest='command', help='command to spawn')
    parser.add_argument('--const', dest='consts',action='append',help='const->value')
    parser.add_argument('--rule', dest='rules',action='append',help='pattern->response')
    parser.add_argument('--timeout', dest='timeout',type=int, default=60, help='timeout')
    parser.add_argument('--debug', dest='debug',action='store_true',help='debug mode')
    args = parser.parse_args()
    if args.debug :
        print("# command = ",args.command)
        print("# consts  = ",args.consts)
        print("# rules   = ", args.rules)
    if not args.command :
        print("# no command specified.")
        parser.print_help()
        sys.exit(0)
    le = LE(command=args.command,timeout=args.timeout)
    le.set_debug(args.debug)
    for c in (args.consts or []) :
        m = re.search(r"(.+?)->(.+)",c)
        if m :
            le.add_const(m.group(1),m.group(2))
    for r in (args.rules or [])  :
        m = re.search(r"(.+?)->(.+)",r)
        if m :
            le.add_rule(m.group(1),m.group(2))
    if args.debug :
        print("# LE = ", str(le))
    le.spawn()

if __name__ == "__main__":
    main()
