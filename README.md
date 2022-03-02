# MIST

This program was the result from trying to make life as an up and comming scientist a little easier in terms of plotting and analyzing data quickly in the form of Python scripts. 


Examples of (current) script functionality: 
* Plotting stacked graphs of e.g. XRD-data with possibility to overlay PDF-lines from an internal database by press of a button 
* Plotting XRD pole figures correctly defined by a press of a button
* Plotting Nanoindentation curves by press of a button
* Calculating XRD-data from Linear scale to Log and sqrt with possibility to save the file 
* ...

A general framework handle reading and writing data from/to files, potential errors and plotting texts. Imported data-files are always kept read-only! General classes and functions were written to simplify script-writing, such as data-containers, predefined graphical entry-objects, string-containers etc. 
The software design philosophy is that it should be easy to understand and easy to modify to fit the present needs. Therefore, to get the most out of the software, each user can/should download and configure the code themselves, and/or write own scripts to match their specific needs.
The software was written object oriented, so user scripts and other modifications should follow the same pattern. 


The GUI is based on the built-in Python library "tkinter"
For graphs, "matplotlib" is used as well as "numpy". 
Small "databases" (where the user can store information more permanently) are based on "json" (e.g. powder diffraction data)
Other libraries are used to handle various tasks.


This is my first attempt at a python software... Bugs may (do...) exist in the code and the code itself is probably not written in the most "python-ish" way... 
I take no responsibility for the quality or accuracy of the calculations and graphs.
With that said, I hope this software can be useful for you!

Copyright 2021-2022 Marcus Lorentzon

