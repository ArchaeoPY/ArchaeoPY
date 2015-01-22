# -*- coding: utf-8 -*-
"""
Created on Tue Dec 09 15:03:09 2014

@author: FPopecarter
"""
import numpy as np

def Rotate2D(pts,cnt,ang=np.pi/4):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    pi     = np.pi
    dot    = np.dot
    sin    = np.sin
    cos    = np.cos
    ar     = np.array
    #rand   = np.rand
    arange = np.arange
    return dot(pts-cnt,ar([[cos(ang),sin(ang)],[-sin(ang),cos(ang)]]))+cnt