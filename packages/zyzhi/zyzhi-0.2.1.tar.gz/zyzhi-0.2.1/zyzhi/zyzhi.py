#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime


def sayhi():

    cyear = str(datetime.datetime.now().year)
    print("Hello World " + cyear + "!")


if __name__ == '__main__':
    
    sayhi()
