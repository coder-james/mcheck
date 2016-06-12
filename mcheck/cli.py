#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MCheck

Usage:
  mcheck ( compute | c ) [-f <file>] [-s <DSA>]
  mcheck ( generate | g ) [-d <directory>] [-s <DSA>]
  mcheck ( validate | v ) [-f <file>] [-t <target>] [-s <DSA>]
  mcheck ( validate | v ) [-d <directory>] [-t <target>]
  mcheck -H | --help
  mcheck -V | --version

Subcommands:
  compute | c            Compute the signature value
  generate | g           Generate a signature file
  validate | v           Validate a file or directory's signature

Options:
  -H, --help          Help information
  -V, --version       Show version
  -s <DSA>            Specify the DSA [md5/sha1/sha224/sha256/sha384/sha512] default[md5]
  -f <file>           Specify the filename
  -d <directory>      Specify the directory
  -t <target>         Specify the target's signature
"""

import os
from docopt import docopt
from mcheck import __version__
from compute import Signature
from generate import SignatureFile
from validate import Validation
import algorithm

def main(args=None):
    if not args:
        args = docopt(__doc__, version="mcheck {0}".format(__version__))
    if args["compute"] or args["c"]:
        if args["-f"] != None:
            if os.path.isfile(args["-f"]):
                sig = Signature()
                if algorithm.isSignatureExist(args["-s"]):
                    value = sig.handle(args["-f"], args["-s"])
                    print value
                else:
                    print "%s signature algorithm is not existed" %(args["-s"])
            else:
                print "%s is a illegal filename" % (args["-f"])
        else:
            print "you need designated a file"
    elif args["generate"] or args["g"]:
        if args["-d"] != None:
            if os.path.isdir(args["-d"]):
                sigf = SignatureFile()
                if algorithm.isSignatureExist(args["-s"]):
                    result = sigf.handle(args["-d"], args["-s"])
                    print "the signature file is saved as %s" %(result)
                else:
                    print "%s signature algorithm is not existed" % (args["-s"])
            else:
                print "%s is a illegal directory" % (args["-f"])
        else:
            print "you need designated a directory"
    elif args["validate"] or args["v"]:
        if args["-f"] != None:
            if args["-d"] != None:
                print "you can't specify a file and a directory at the same time"
            else:
                if args["-t"] != None:
                    valid = Validation()
                    if algorithm.isSignatureExist(args["-s"]):
                        passed,m = valid.handle_file(args["-f"],args["-s"],args["-t"])
                        if passed:
                            print "%s Check passed" %(m)
                        else:
                            print "%s Check not passed" %(m)
                    else:
                        print "%s signature algorithm is not existed" % (args["-s"])
                else:
                    print "you need provide a target's signature"
        elif args["-d"] != None:
            if args["-t"] != None:
                valid = Validation()
                fa = args["-t"].split(".")
                if algorithm.isSignatureExist(fa[len(fa)-1]):
                    m = fa[len(fa) - 1]
                    passed = valid.handle_directory(args["-d"],args["-t"])
                    if passed:
                        print "%s Check passed" % (m)
                    else:
                        print "%s Check not passed" % (m)
                else:
                    print "you need provide a signature file available"
            else:
                print "you need provide a target's signature (file)"
        else:
            print "you need specify a file or a directory"
    else:
        pass

if __name__ == '__main__':
    main()