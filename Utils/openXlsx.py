# -*- coding: utf-8 -*-
from tkFileDialog import askopenfilename
import xlrd
import numpy as np
import brewer2mpl


"""
Excel Import
============

Opens excel file, ready for reading.
"""

def openXlsx():
    filename = askopenfilename() #GUI file open dialogue
    workbook = xlrd.open_workbook(filename) #accesses excel file
    return workbook
    
"""
Generate colours!
=================

"""    
def prettyColours():
    set2 = brewer2mpl.get_map('Set2', 'qualitative', 8).mpl_colors  
    return set2
    
"""
MIT Stress Path Plot
====================

Plots triaxial data on a MIT stress path plot, and calculates effective stress parameters.

Requires excel input of this form and a sheet name 'Triaxial':
    
|   | A      | B      | C            | D      |
|---+--------+--------+--------------+--------|
| 1 | Sigma3 | sigma1 | Scheme Title | *name* |
| 2 | *Data* | *Data* | *Data*       |        |
| 3 | *Data* | *Data* | *Data*       |        |
| 4 | *Data* | *Data* | *Data*       |        |



"""
def mitStressPath():
    workbook = openXlsx()
    sheet = workbook.sheet_by_name('Triaxial')
    sigma1 = sheet.col_values(1) #Column B
    sigma3 = sheet.col_values(0) #Column A
    scheme = sheet.cell(0,3).value
    #scheme = ucd.normalize('NFKD', scheme).encode('ascii', 'ignore')
    print scheme
    #Removing the headers from the spreadsheet
    sigma1.pop(0)
    sigma3.pop(0)
    #Converting lists to numpy arrays
    sigma1 = np.array(sigma1)
    sigma3 = np.array(sigma3)
    
    
    #Setting up colors for use in plots
    almost_black = '#262626'
    set2 = prettyColours()
    
    #Manipulating data for input into chart
    x = (sigma1 + sigma3)/2 #Centre of Mohr's Circles for each data set
    y = (sigma1 - sigma3)/2 #Radius of Mohr's Circles for each data set
    x2 = np.arange(0, max(x)*1.2, 0.1)
    
    #Line of best fit
    m,b = np.polyfit(x,y,1)
    #Manipulating data to get Effective Stress Parameters
    phi = np.arcsin(m)
    phi = round(phi, 2)
    c = b/(np.cos(phi))
    c= round(c, 2)
    phiOut = 'phi - ' + str(phi) + ' degrees'
    cOut = 'c\' - ' + str(c) + ' kPa'
    print phiOut 
    print cOut
    
    
    #Plotting Stress Path Plot
    fig = plt.figure()
    plt.scatter(x,y, s=40, edgecolor=almost_black, facecolor=set2[0], linewidth=0.15)
    plt.plot(x2, m*x2+b, color=set2[1])
    
    
    #Using a For loop to plot all the Mohr's Circle Data
    a = sigma1.shape[0]
    for i in range(0, a):
        l =sigma3[i]
        m = sigma1[i]
        x = np.arange(l,m, 0.1)
        y = np.sqrt((((m-l)/2)**2 - (x - (m+l)/2)**2)) #equation of circle for Mohr's Circle
        plt.plot(x,y, color=set2[i+2])
    
    #Setting plot formatting
    plt.grid()
    plt.axis([0, np.amax(sigma1), 0, max(y)*1.1])
    plt.axes().set_aspect('equal')
    
    #Plot Title and Axis Titles
    plt.title(scheme + ' - MIT Stress Path Plot')
    plt.xlabel('p\' (kpa)')
    plt.ylabel('q (kPa)')
    plt.show()
    
