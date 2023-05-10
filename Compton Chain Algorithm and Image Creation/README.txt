All of the Compton chain ordering code, along with the image creation code is contained in the “Compton Chain Algorithm and Image Creation” directory. To make the Compton chain reconstruction code make sure you have gcc and make, then run “make compton_reconstruction”. This will create an executable called compton_reconstruction. This can then be run using the following syntax: 

./compton_reconstruction [source tuple data] [location and name of output] [FOM/scatter] [FLAGS]

The source tuple data is expected to come from the custom extension scorer. If the source data is in the binary output format from TOPAS a –b flag should be added in the flags location. 

If you wish to change the energy resolution from the baseline at run time add the following flag and then your value: –E [energy/count in keV]. This sets a new energy per count value for application of energy randomness. 

If you wish to change the spatial resolution from the baseline at run time add the following flag and then your value: -s [distance in cm]. This changes the distribution of spatial error applied to scatters. 

To change the time resolution from the baseline at run time add the –t [time in cm]. This value is in units of distance, and is the 1 sigma size for the distribution. To give a worked example, the 500 ps FWHM value used for the baseline leads to a 1 sigma time of 212 ps. Converted to distance this is then divided by the speed of light to give the timing error in distance of 6.36 cm. 

Information on using flags can also be found by adding a –h flag after the three main arguments. 

The output will be three files: a .lor containing all of the found lines of response, a .eng containing the first five energies of the scatters that were reconstructed for each history, and a .debug file containing a large number of diagnostic values for determining detector and reconstruction behavior. The latter two files are purely for diagnostic use and can be discarded otherwise.

To make a .lor file into an image the renderer code is used. To make the executable run "make renderer", creating the renderer executable. The code arguments are as follows:

./renderer [source .lor file] [addition method] [output file name] [FLAGS]

This code is run using the "addition_440_thin.def" file as the addition method. Generally the output file is marked as .data, however this is entirely up to user choice.

For the Derenzo phantom attenuation correction is used. This is done using the -g flag followed by the phantom geometry definition file "geo_derenzo.geo". To find the full list of available flags use a -h flag.

After creation of the .data file containing the numerical data of what each voxel value is you can make this into an easier to process .npy file using the "image_conversion_cleanup.py" file. To use this set the source file inside of the code.

This will produce a .npy file of the same name, which can then be easily processed, an example of which is given in the run_filter file.