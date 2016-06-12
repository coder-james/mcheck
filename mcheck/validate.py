#!/usr/bin/env python
# -*- coding: utf-8 -*-

from compute import Signature

class Validation():

    def handle_file(self, filename, method, target):
        sig = Signature()
        result, m = sig.produce(filename, method)
        return result == target, m

    def handle_directory(self, directory, target):
        temp = target.split(".")
        method = temp[len(temp) - 1]
        sfile = open(target)
        scontent = sfile.read().split("\n")
        result = True
        sig = Signature()
        for sline in scontent:
            ss = sline.split(" ")
            if len(ss) > 1:
                sv, m = sig.produce(ss[1], method)
                if sv != ss[0]:
                    print ss
                    result = False
        return result



