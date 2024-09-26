**Deciphering the wqm_apl.run and Writing it to NetCDF**

**Task Overview**

The task involves using three files provided by Richard Tian from CBP to
convert the binary unformatted output file, wqm_apl.run, into a
sustainable NetCDF format for future use. The files required are:

1.  col_cbay_56920.dat

2.  col_cbay_56920xy.csv

3.  wqm_apl.run

The wqm_apl.run file contains binary unformatted output data written in
Fortran. The col_cbay_56920.dat and col_cbay_56920xy.csv files provide
the mapping between Cell_ID, I, J, Layer#, UTM-X, and UTM-Y. Richard
Tian also provided a Fortran77 code to read the binary output. Our goal
is to write a Python script that deciphers the wqm_apl.run file and
converts the time series data for each variable into a NetCDF format,
ensuring it is accessible and sustainable for future use.

**Code Structure**

**Preprocessing**

**Script:** Cell2LonLat.py\
**Required Files:** col_cbay_56920.dat and col_cbay_56920xy.csv\
This script merges the information from the two input files to generate
the Cell2LonLat.csv file, which contains the longitude and latitude data
for each cell. This CSV file is essential for the next step.\
\
*You should see below in your terminal:\
*![A screenshot of a computer code Description automatically
generated](media/image1.png){width="6.5in" height="2.078472222222222in"}

**Deciphering**

-   **Configuration File:** config.json

-   **Main Script:** Decipher.py

-   **Utility Script:** utils.py

Modify the config.json file to specify parameters such as the output
directory. Then, run Decipher.py, which uses functions defined in
utils.py and the configurations set in config.json. Generally, you do
not need to modify utils.py or Decipher.py.

*You should see below in your terminal:\
*![A screenshot of a computer code Description automatically
generated](media/image2.png){width="6.5in" height="4.442361111111111in"}

*...*

![](media/image3.png){width="6.5in" height="0.4236111111111111in"}

**Checking Data Saved in NetCDF**

-   **Reader Script:** netCDFReader.py

-   **GUI Tool:** probe_GUI.py

The netCDFReader.py script allows you to read and verify the NetCDF
output, which contains time series data with one variable per file. The
probe_GUI.py provides an interface for exploring the data. It enables
users to identify the nearest six grid points to a selected location and
visualize basic time series plots based on the selected point.

*You should see below like this in your terminal:*![A screenshot of a
computer program Description automatically
generated](media/image4.png){width="4.178571741032371in"
height="6.243286307961505in"}

![A screenshot of a computer generated image Description automatically
generated](media/image5.png){width="5.857142388451444in"
height="3.0866983814523183in"}

![A graph with different colored lines Description automatically
generated with medium confidence](media/image6.png){width="6.5in"
height="2.901388888888889in"}
