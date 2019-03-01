#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mapplotter

if __name__ == '__main__':
    p = mapplotter.Plotter()

    p.setCoordsFromString("694'897.01, 177'036.54")
    p.setZoomLevel(8)

    p.setPoints(5,5)

    p.getAllPoints()

    p.saveDataToFile()

    p.plot()
