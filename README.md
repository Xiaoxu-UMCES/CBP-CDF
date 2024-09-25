###############Decipher the wqm_apl.run and write it in netCDF########################
Please Run Decipher.py, code is linked to the utils.py and the config.json. Please modify the config.json based on your demand, like change the output directory. No need to change the utils.py and Decipher.py. Utils.py includes all the functions which are used in the Decipher.py. 
NetCDFReader.py provides you the ability to read the deciphered netCDF output. This netCDF is saving as time teries data for one variable per file. Also provide a ProbeGUI.py tool for probing the data in an interaction interface.

The col_cbay_56920.dat and col_cbay_56920xy.csv files are provided by Richard Tian, which contains the CellID, I,J,Layer#, UTM-X,UTM-Y mapping. Runthe Cell2LonLat.py will combine the informations of the two files together, and also saved Longitute and Latitude in the file Cell2LonLat.csv file. This file is neccessary for the Decipher.py code.

The netCDF's structure is showing below. Run this code, you can probe the data by proving the Cell_ID, Layer#, the day number. 
Run the NetCDFReader.py will get the output look like this:

Decipher.py is reading and writing netCDF the wqm_apl.run(a binary unformatted output file provided by Richard Tian)
 1) need the "wqm_qpl.run" file
 2) need the "nwcbox_ij_UTM.csv" file, this file provided the nwcbox#, Cell#, I, J, and UTMX, UTMY. This file is a combination of "col_cbay_56920xy.csv"(provided by Richard Tian) and "col_cbay_56920.dat"(provided by Richard Tian), please ask Xiaoxu if you need the python code 

Data from data_Header:
title: b'\x88\x02\x00\x00Apply St Johns parallel code to Chesapeake Bay                          Code provided by MN in GOLD_STANDARD Jan 17, 2006                       Terrys vertical code installed by CFC in terrys_code_FGS Jan 23, 2006   This code brought up from aquarius /disk2/new_ches_bay/Jan_27_06        Run from ches_bay_50000/st_johns/Jan_27_06                              Feb 27, 2006                                                            '
nac: 28
ac: [ 1  2  3  4  5  6  9 11 12 13 14 16 18 19 20 21 23 24 25 26 27 30 31 32
 33 34 35 36  0  0  0  0  0  0  0  0]
nb: 56920
nspecies: 5
quality_diag: True
sediment_diag: True
sav: True
space: b'\xff'
anc1: 0.17499999701976776
anc2: 0.13500000536441803
anc3: 0.1550000011920929
apc1: 0.012500000186264515
apc2: 0.016699999570846558
apc3: 0.016699999570846558
kadpo4: 0.0
adwcepi: 18.0
ndomsp: 3
alac: [1.33000e-01 2.50000e-01 2.50000e-01 9.08041e-43 3.81075e-40]
nsb: 11064
v1: [3465398.5  2208817.   3299762.   ... 1005585.75 1041460.3  1092889.1 ]
sfa: [1536903.1   991086.75 1491936.1  ...  729589.    645997.4   719412.  ]
scover: [1. 1. 1. ... 0. 0. 0.]

Provided nwcbox: 56920
Processing Date: 1990-12-31-00
Processed # of nwcbox: 1000, please wait...
...

Processed # of nwcbox: 56000, please wait...
Time taken for Date 1991-01-01-00: 434.74 seconds
All files created successfully!




