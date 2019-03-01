#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mapplotter

if __name__ == '__main__':
    p = mapplotter.Plotter()

    p.loadFromFile("mapplotter/examples/eigernord")

    p.plot()
