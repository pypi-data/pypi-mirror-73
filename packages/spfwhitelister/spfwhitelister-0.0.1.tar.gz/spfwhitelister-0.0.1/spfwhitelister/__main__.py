#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Query DNS looking for spf records for a given domain
# and add the addresses to the greylistd's whitelist
#
import argparse
import sys
from . import get_spf_list

__version__ = "0.1"

MARKER = "####whitelister"*5

def main():
    parser = argparse.ArgumentParser(description="Whitelist domains.")
    parser.add_argument("-f", "--file", default="/etc/greylistd/whitelist-hosts",
                        help="The file to add the addresses to. (Default /etc/greylistd/whitelist-hosts)")
    parser.add_argument("-d", "--domains", default=[], nargs="*",
                        help="The list of domains to add. (No default)")
    parser.add_argument("-o", "--output", action="store_true", default=False,
                        help="Do not modify the file, print the list out.")

    try:
        opts = parser.parse_args()
    except Exception as e:
        parser.error("Error: " + str(e))
        sys.exit(-1)

    lohosts = get_spf_list(opts.domains)
    if opts.output:
        print("\n".join(lohosts))
    else:
        newfile=[]
        skip = False
        try:
            with open(opts.file,"r") as confile:
                oldfile=confile.read().split("\n")
                for line in oldfile:
                    if line.startswith(MARKER):
                        skip = not skip
                    elif not skip:
                        newfile.append(line)
        except Exception as e:
            print("Warning: File {} could not be read. Error was: {}".format(opts.file,e))
        if newfile[-1]=="":
            newfile = newfile[:-1]
        if lohosts:
            newfile += [MARKER] + lohosts + [MARKER]
        newfile += [""]

        try:
            with open(opts.file,"w") as confile:
                confile.write("\n".join(newfile))
        except:
            print("Warning: File {} could not be written. Error was: {}".format(opts.file,e))


if __name__ == "__main__":
    main()
