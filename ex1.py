#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2019 Matthias Busenhart


import mapplotter

if __name__ == '__main__':
    p = mapplotter.Plotter()

    p.loadFromFile("mapplotter/examples/eigernord")

    p.plot(overlay=True)
