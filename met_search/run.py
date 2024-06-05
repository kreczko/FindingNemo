#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 6 Oct 2013

@author: kreczko
'''
import os, os.path, datetime, re, sys, copy, traceback, shutil, hashlib, tempfile

from ROOT import gROOT

from utils.theta_auto import config
from utils.theta_auto.Report import html_report
from utils.theta_auto.utils import info

def clean_workdir():
    shutil.rmtree(config.workdir, ignore_errors = True)
    setup_workdir()
    
def setup_workdir():
    if not os.path.exists(config.workdir): os.mkdir(config.workdir)
    if not os.path.exists(os.path.join(config.workdir, 'plots')): os.mkdir(os.path.join(config.workdir, 'plots'))

if __name__ == '__main__':
    gROOT.SetBatch(True)
    scriptname = 'analysis.py'
    tmpdir, profile = False, False
    wd = None
    for iarg, arg in enumerate(sys.argv[1:]):
        if '.py' in arg: scriptname = arg
        if arg=='--tmpdir': tmpdir = True
        if arg=='--profile': profile = True
        if arg=='--workdir': wd = sys.argv[iarg+2]
    if tmpdir:
        config.workdir = tempfile.mkdtemp()
    else:
        config.workdir = os.path.join(os.getcwd(), scriptname[:-3])
        config.workdir = os.path.realpath(config.workdir)
        if wd is not None:
            config.workdir = os.path.realpath(wd)
    setup_workdir()
    config.theta_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    config.theta_dir = '/software/theta'
    config.report = html_report(os.path.join(config.workdir, 'index.html'))
    variables = globals()
    variables['report'] = config.report
    info("executing script %s" % scriptname)
    try:
        if profile:
            import cProfile
            cProfile.runctx("execfile(scriptname, variables)", globals(), locals())
        else:
            execfile(scriptname, variables)
    except Exception as e:
        print "error while trying to execute analysis script %s:" % scriptname
        traceback.print_exc()
        sys.exit(1)
    info("workdir is %s" % config.workdir)