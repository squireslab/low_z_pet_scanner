import numpy as np

source = np.loadtxt("Delorzo2.txt", delimiter=',')
source = source - (142.5, 120.0, 0.0)
pixel_to_cm = 0.1
parent_rad = 10.6
parent_height = 8.0
rod_height = 6.0
rod_z = 0.0
volume_offset = 1
rod_color = "red"
parent_color = "green"

derenzo_material = "\"Vacuum\""
# derenzo_material = "\"G4_WATER\""

# positron_energy_MeV = 0.3
positron_energy_MeV = 0.0

file_text  = "# A topas file containing the Derenzo phantom.\n"
file_text += "# Background e+/cm^3\n"
file_text += "i:Background_e = 0\n"
file_text += "# Rod e+/cm^3\n"
file_text += "i:Rod_e = 0\n"
file_text += "\n\n # a few useful constants:\n u:pi = 3.1415\n\n"

source_text = "# The sources making up the Derenzo phantom\n\n"

parent_nm = "Derenzo"

center_geo = "# The geometry of the Derenzo phantom\n\n"

center_geo += "s:Ge/" + parent_nm + "/Type      = \"TsCylinder\"\n"
center_geo += "s:Ge/" + parent_nm + "/Material  = " + derenzo_material + "\n"
center_geo += "d:Ge/" + parent_nm + "/Rmax      = " + str(parent_rad) + " cm\n"
center_geo += "d:Ge/" + parent_nm + "/HL        = " + str(parent_height / 2) + " cm\n"
center_geo += "s:Ge/" + parent_nm + "/Color     = \"" + parent_color + "\"\n\n"

center_src  = "s:So/" + parent_nm + "_src/Type	                   = \"Volumetric\"\n"
center_src += "s:So/" + parent_nm + "_src/Component               = \"" + parent_nm + "\"\n"
center_src += "s:So/" + parent_nm + "_src/ActiveMaterial          = " + derenzo_material + "\n"
center_src += "s:So/" + parent_nm + "_src/BeamParticle            = \"e+\"\n"
center_src += "d:So/" + parent_nm + "_src/BeamEnergy              = " + str(positron_energy_MeV) + " MeV\n"
# center_src += "u:BackgroundVol                         = " + str(np.pi * parent_rad * parent_rad * parent_height) + "\n"
# the backgound volume will need the volume of all of the rods removed
center_volume = np.pi * parent_rad * parent_rad * parent_height * volume_offset

# add the center time step function

center_step  = ""
center_step += "s:Tf/" + parent_nm + "_t/Function = \"Step\"\n"



# build the set of rods. Each rod requires a geometry definition and a source
# definition These get added to their respective portions
rod_geometry = "# rod geometries\n\n"
rod_sources = "# rod sources\n\n"
rod_steps = "# rod time steps run one rod at a time\n\n"


timing_array = np.zeros((np.shape(source)[0] + 1, 1))
times_string = ""
for i in range(np.shape(source)[0] + 1):
    times_string += " " + str(float(i) + 0.5)

for i in range(np.shape(source)[0]):
    # add the rod geometry to the file
    rod_geometry += "s:Ge/Rod_" + str(i) + "/Type = \"TsCylinder\"\n"
    rod_geometry += "s:Ge/Rod_" + str(i) + "/Material = " + derenzo_material + "\n"
    rod_geometry += "s:Ge/Rod_" + str(i) + "/Parent = \"" + parent_nm + "\"\n"
    rod_geometry += "d:Ge/Rod_" + str(i) + "/Rmax = " + str(source[i,2] * pixel_to_cm * 0.5) + " cm\n"
    rod_geometry += "d:Ge/Rod_" + str(i) + "/HL = " + str(rod_height * 0.5) + " cm\n"
    rod_geometry += "d:Ge/Rod_" + str(i) + "/TransX = " + str(source[i,0] * pixel_to_cm) + " cm\n"
    rod_geometry += "d:Ge/Rod_" + str(i) + "/TransY = " + str(source[i,1] * pixel_to_cm) + " cm\n"
    rod_geometry += "d:Ge/Rod_" + str(i) + "/TransZ = " + str(rod_z) + " cm\n"
    rod_geometry += "s:Ge/Rod_" + str(i) + "/Color = \"" + rod_color + "\"\n\n"
    rod_volume = np.pi * source[i,2] * pixel_to_cm * source[i,2] * pixel_to_cm * rod_height * 0.5 * volume_offset
    center_volume -= rod_volume

    # add the rod source to the file
    rod_sources += "s:So/Rod_" + str(i) + "_src/Type = \"Volumetric\"\n"
    rod_sources += "s:So/Rod_" + str(i) + "_src/Component = \"Rod_" + str(i) + "\"\n"
    rod_sources += "s:So/Rod_" + str(i) + "_src/ActiveMaterial = " + derenzo_material + "\n"
    rod_sources += "s:So/Rod_" + str(i) + "_src/BeamParticle = \"e+\"\n"
    rod_sources += "d:So/Rod_" + str(i) + "_src/BeamEnergy = " + str(positron_energy_MeV) + " MeV\n"
    rod_sources += "i:Rod_" + str(i) + "_src_mult = Tf/Rod_" + str(i) + "_t/Value * " + str(round(rod_volume)) + "\n"
    rod_sources += "i:So/Rod_" + str(i) + "_src/NumberOfHistoriesInRun = Rod_e * Rod_" + str(i) + "_src_mult\n\n"

    # add the rod step function to the file. This function is 1 only for the history the rod should be in
    rod_steps += "s:Tf/Rod_" + str(i) + "_t/Function = \"Step\"\n"
    rod_steps += "dv:Tf/Rod_" + str(i) + "_t/Times = " + str(np.shape(source)[0] + 1) + times_string + " s\n"
    timing_array[i] = 1
    rod_steps += "iv:Tf/Rod_" + str(i) + "_t/Values = " + str(np.shape(source)[0] + 1)
    for j in range(len(timing_array)):
        rod_steps += " " + str(int(timing_array[j,0]))
    rod_steps += "\n\n"
    timing_array[i] = 0

# add the step function for the background parent object
center_step += "dv:Tf/" + parent_nm + "_t/Times = " + str(np.shape(source)[0] + 1) + times_string + " s\n"
timing_array[len(timing_array) - 1] = 1
center_step += "iv:Tf/" + parent_nm + "_t/Values = " + str(np.shape(source)[0] + 1)
for j in range(len(timing_array)):
    center_step += " " + str(int(timing_array[j,0]))
center_step += "\n\n"
# define how many histories should run in the derenezo background.
# this requires the center volume with all of the rods volumes taken out
center_src += "i:" + parent_nm + "_src_mult = Tf/" + parent_nm + "_t/Value * " + str(round(center_volume)) + "\n"
center_src += "i:So/" + parent_nm + "_src/NumberOfHistoriesInRun = " + parent_nm + "_src_mult * Background_e\n\n"

# combine the geometry text

comb_geo = center_geo + rod_geometry

# combine the source text

source_text += center_src + rod_sources

# combine the step functions

comb_step = center_step + rod_steps

# combine all of the text together

file_text += comb_geo + source_text + comb_step

# add the timing behavior

file_text += "d:Tf/TimelineStart = 0. s\n"
file_text += "d:Tf/TimelineEnd = " + str(float(np.shape(source)[0] + 1)) + " s\n"
file_text += "i:Tf/NumberOfSequentialTimes = " + str(np.shape(source)[0] + 1) + "\n\n"

print(file_text)
