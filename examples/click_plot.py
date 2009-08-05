#!/usr/bin/env python
# encoding: utf-8
"""
show_artist.py

Created by Paul Lamere on 2009-08-04.
Copyright (c) 2009 The Echo Nest Corporation. All rights reserved.
"""

import sys
import os

from pyechonest import track as track_api
from pyechonest import config
import matplotlib.pyplot as plt

# How to set your ECHO_NEST_API_KEY:
#   1) Set the environment variable 'ECHO_NEST_API_KEY' to be your key, or
#   2) Uncomment the next line and add your key between the quotes
#config.ECHO_NEST_API_KEY="YOUR API KEY HERE" 

usage = "Usage: click_plot.py filename"

def plot_click_track(filename):
    track = track_api.Track(filename)
    tempo = float(track.tempo['value'])
    beats = track.beats
    times = [ dict['start'] for dict in beats ]
    bpms = get_bpms(times)
    plt.ylabel('Beats Per Minute')
    plt.xlabel('Time')
    plt.title('Click Plot for ' + os.path.basename(filename))
    plt.plot(times, get_filtered_bpms(bpms), label='Filtered')
    plt.plot(times, bpms, color=('0.8'), label='raw')
    plt.ylim(tempo * .9, tempo * 1.1)
    plt.axhline(tempo, color=('0.7'), label="Tempo")
    plt.show()

def get_bpms(times):
    bpms = []
    for i in xrange(len(times) - 1):
        delta = times[i + 1] - times[i]
        bpms.append(60. / delta)
    bpms.append(60. / delta)
    return bpms

def get_filtered_bpms(bpms):
    filtered = []
    for i in xrange(len(bpms)):
        filtered.append(filter(bpms, i))
    return filtered

def filter(bpms, which, size=5):
    sum = 0
    count = 0
    for i in xrange(which - size, which + size):
        if i >=0 and i < len(bpms) - 1:
            sum += bpms[i]
            count += 1
    return sum / count

if __name__ == "__main__":
    if len(sys.argv) <> 2:
        print usage
        sys.exit(1)
    else:
        plot_click_track(sys.argv[1])

