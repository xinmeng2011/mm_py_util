#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pw @ 2014-12-24 15:38:26
# Author: Cindy
# Detail:

import chalk

enable = False

def blue(str2):
    if not enable:
        return
    chalk.blue(str2)

def cyan(str):
    if not enable:
        return
    chalk.cyan(str)

#COLORS = (
#            'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
#            )


class chalker:
    def __getattr__(self, name):
        def _call(*args):
                return call(name, *args)
        return _call
    

def call(function_name, str):
    try:
        fun = getattr(chalk, function_name)
        fun(str)
    except:
        chalk.blue(str)

pen = chalker()

