#!/usr/bin/python
###########################################
#
#Title: aerotrans.py
#Author: Jaime Saelices
#Release: v4
#Date: 06/10/2014
#Bugfix: Removed AWAreal computation due to its useless nature
#Input data: sum_up.txt renamed by aero_clean_python to project.log
#Output data: Three csv files named like sum_up.txt used as input. One file per part:sails, hull and rig
#
###########################################

import argparse
import numpy as np
import math
import os
import csv
import sys

#Definitions for arguments passed to the program
parser = argparse.ArgumentParser()
parser.add_argument("projectname", action='store', help="name to use in order to parse the file")
parser.add_argument("-d", "--datum", action='store', type=float, nargs=2, dest='datum', help="xdatum and zdatum for VppCS")
parser.add_argument("-m", "--masth", action='store', type=float, nargs=1, dest='masth', help="masthead from water surface")
parser.add_argument("-c", "--csv", action='store_true', default=True, dest='csv', help="indicates that output will be in csv format")
parser.add_argument("-s", "--split", action='store_true', default=False, dest='split', help="all CFD parts will be processed")
parser.add_argument("-g", "--gonzalo",action='store_true', default=False, dest='gonz', help="output file will have only forces and moments refered to VppCS")
args = parser.parse_args()

Adens = 1.18415
vconv = 1.944
fallo = ""

for cfd_part in ['hull', 'sails', 'rig']:
	filename_suffix = "-trans-"
	part_suffix = cfd_part
	file_extension = ".csv"
	filename = os.path.join(args.projectname + filename_suffix + part_suffix + file_extension)
	csv_file = open(filename, "ab")
	csv_write = csv.writer(csv_file)
	if args.gonz:
		data = ['Sail', 'Trim' , 'Path', 'TWS Masthead (Kn)', 'TWA (NS)', 'Heel', 'Yaw', 'Boatspeed (Kn)', 'Area', 'h (Couple)', 'AWS 10m (Kn)', 'AWA 10m (NS)', 'CL', 'CD (sign changed)', 'CU', 'CEx (CP datum)', 'CEy (CP datum)', 'CEz (Cp datum)', 'TWA', 'Fx (VPP)', 'Fy (VPP)', 'Fz (VPP)', 'Mx (VPP)', 'My (VPP)', 'Mz (VPP)', 'Mx Couple (VPP)', 'My Couple (VPP)', 'Mz Couple (VPP)']
		csv_write.writerow(data)
	else:
		data = ['Sail', 'Trim' , 'Path', 'TWS Masthead (Kn)', 'TWA (NS)', 'Heel', 'Yaw', 'Boatspeed (Kn)', 'Area', 'Fx', 'Fy', 'Fz', 'Mx (Datum)', 'My (Datum)', 'Mz (Datum)', 'Mx (Couple)', 'My (Couple)', 'Mz (Couple)', 'h (Couple)', 'AWS 10m (Kn)', 'AWA 10m (NS)', 'CL', 'CD (sign changed)', 'CU', 'CEx (CP datum)', 'CEy (CP datum)', 'CEz (Cp datum)', 'TWA', 'Fx (VPP)', 'Fy (VPP)', 'Fz (VPP)', 'Mx (VPP)', 'My (VPP)', 'Mz (VPP)', 'Mx Couple (VPP)', 'My Couple (VPP)', 'Mz Couple (VPP)']
	csv_write.writerow(data)
#csv_file.close()
			
#We open the file passed as argument previously
with open(args.projectname, "r") as file:
	while True:
		output = file.readline().split()
		if not output: 
			break
		#Definition and initialization of several variables (values taken from sum_up.txt
		try:
			sail = (output[1])
			sail_trim = (output[3])
			sail_forces = np.array([float(output[6]), float(output[7]), float(output[8])])
			sail_moments = np.array([float(output[9]), float(output[10]), float(output[11])])
			hull_forces = np.array([float(output[13]), float(output[14]), float(output[15])])
			hull_moments = np.array([float(output[16]), float(output[17]), float(output[18])])
			mast_forces = np.array([float(output[20]), float(output[21]), float(output[22])])
			mast_moments = np.array([float(output[23]), float(output[24]), float(output[25])])
			jib_forces = np.array([float(output[27]), float(output[28]), float(output[29])])
			jib_moments = np.array([float(output[30]), float(output[31]), float(output[32])])
			main_forces = np.array([float(output[34]), float(output[35]), float(output[36])])
			main_moments = np.array([float(output[37]), float(output[38]), float(output[39])])
			stay_forces = np.array([float(output[41]), float(output[42]), float(output[43])])
			stay_moments = np.array([float(output[44]), float(output[45]), float(output[46])])
			boom_forces = np.array([float(output[48]), float(output[49]), float(output[50])])
			boom_moments = np.array([float(output[51]), float(output[52]), float(output[53])])
			totalA = np.empty((10))
			totalA[0] = float(output[54])+float(output[55])+float(output[56])
			totalA[1] = float(output[57])/2
			totalA[2] = (float(output[58])+float(output[59]))/2
			totalA[3] = totalA[0]
			totalA[4] = totalA[1]
			totalA[5] = float(output[59])/2
			totalA[6] = float(output[54])
			totalA[7] = float(output[55])/2
			totalA[8] = float(output[56])
			totalA[9] = float(output[58])/2
			masth = args.masth[0]
			proj_dir = (output[70])
			heel = math.radians(float(output[65]))
			trim = math.radians(float(output[66]))
			yaw = math.radians(float(output[67]))
			TWA = math.radians(float(output[60]))
			BS = float(output[64])
			TWS = float(output[61])
			refH = float(output[63])
			WPI = float(output[62])
			
			TWSrefS = TWS*math.pow(10.0/refH,WPI)
			AWSS = math.sqrt(math.pow(TWSrefS*math.cos(TWA)+BS*math.cos(yaw),2)+math.pow(TWSrefS*math.sin(TWA)-BS*math.sin(yaw),2))
			AWA = math.acos((TWSrefS*math.cos(TWA)+BS*math.cos(yaw))/AWSS)
			#AWAreal = math.acos((TWSrefS*math.cos(TWA+yaw))/AWSS)
			TWSMH = TWS*math.pow((masth*math.cos(heel))/refH,WPI)

			#Transform the forces and moments to the VPP frame, generic forces/moments are the same forces/moments acting on sails,hull and rig. In C++ it is coded in this way and works so let it be.  
			Mforces = np.empty((10,3))
			Mmoments = np.empty((10,3))
			MmomentsD = np.empty((10,3))
			Mforcesy = np.empty((10,3))
			MmomentsDy = np.empty((10,3))
			coupleFy = np.empty((10,3))
			coeff = np.empty((10,3))
			CEH = np.empty((10,3))
			CE = np.empty((10,3))
			coupleF = np.empty((10,3))
			hnumber = np.empty((10))

			Mforces[0,:] = np.array([-(sail_forces[0]+mast_forces[0]+boom_forces[0]), sail_forces[2]+mast_forces[2]+boom_forces[2], sail_forces[1]+mast_forces[1]+boom_forces[1]])
			Mmoments[0,:] = np.array([-(sail_moments[0]+mast_moments[0]+boom_moments[0]), sail_moments[2]+mast_moments[2]+boom_moments[2], sail_moments[1]+mast_moments[1]+boom_moments[1]])
			Mforces[1,:] = np.array([-(hull_forces[0]), hull_forces[2], hull_forces[1]])
			Mmoments[1,:] = np.array([-(hull_moments[0]), hull_moments[2], hull_moments[1]])
			Mforces[2,:] = np.array([-(mast_forces[0]+boom_forces[0]), mast_forces[2]+boom_forces[2], mast_forces[1]+boom_forces[1]])
			Mmoments[2,:] = np.array([-(mast_moments[0]+boom_moments[0]), mast_moments[2]+boom_moments[2], mast_moments[1]+boom_moments[1]])
			Mforces[3,:] = np.array([-(sail_forces[0]), sail_forces[2], sail_forces[1]])
			Mmoments[3,:] = np.array([-(sail_moments[0]), sail_moments[2], sail_moments[1]])
			Mforces[4,:] = np.array([-(hull_forces[0]), hull_forces[2], hull_forces[1]])
			Mmoments[4,:] = np.array([-(hull_moments[0]), hull_moments[2], hull_moments[1]])
			Mforces[5,:] = np.array([-(mast_forces[0]), mast_forces[2], mast_forces[1]])
			Mmoments[5,:] = np.array([-(mast_moments[0]), mast_moments[2], mast_moments[1]])
			Mforces[6,:] = np.array([-(jib_forces[0]), jib_forces[2], jib_forces[1]])
			Mmoments[6,:] = np.array([-(jib_moments[0]), jib_moments[2], jib_moments[1]])
			Mforces[7,:] = np.array([-(main_forces[0]), main_forces[2], main_forces[1]])
			Mmoments[7,:] = np.array([-(main_moments[0]), main_moments[2], main_moments[1]])
			Mforces[8,:] = np.array([-(stay_forces[0]), stay_forces[2], stay_forces[1]])
			Mmoments[8,:] = np.array([-(stay_moments[0]), stay_moments[2], stay_moments[1]])
			Mforces[9,:] = np.array([-(boom_forces[0]), boom_forces[2], boom_forces[1]])
			Mmoments[9,:] = np.array([-(boom_moments[0]), boom_moments[2], boom_moments[1]])

			#CE, couples and coefficients computation
			for number in range(10):
				vdot = math.pow(Mforces[number,0],2)+math.pow(Mforces[number,1],2)+math.pow(Mforces[number,2],2)
				if vdot == 0:
					CE[number,:] = ([0,0,0])
					h = 0
				else:
					CE[number,0] = (Mforces[number,1]*Mmoments[number,2]-Mforces[number,2]*Mmoments[number,1])/vdot
					CE[number,1] = (Mforces[number,2]*Mmoments[number,0]-Mforces[number,0]*Mmoments[number,2])/vdot
					CE[number,2] = (Mforces[number,0]*Mmoments[number,1]-Mforces[number,1]*Mmoments[number,0])/vdot

					h = (Mforces[number,0]*Mmoments[number,0]+Mforces[number,1]*Mmoments[number,1]+Mforces[number,2]*Mmoments[number,2])/vdot
					hnumber[number] = h
				for n in range(3):
					coupleF[number,n] = Mforces[number,n]*h

					CEH[number,0] = CE[number,0]-args.datum[0]
					CEH[number,1] = CE[number,1]*math.cos(heel)-CE[number,2]*math.sin(heel)
					CEH[number,2] = CE[number,2]*math.cos(heel)+CE[number,1]*math.sin(heel)-args.datum[1]

					CE[number,0] = CE[number,0]-args.datum[0]
					CE[number,1] = CE[number,1]-args.datum[1]*math.sin(heel)
					CE[number,2] = CE[number,2]-args.datum[1]*math.cos(heel)

					MmomentsD[number,0] = Mforces[number,2]*CE[number,1]-Mforces[number,1]*CE[number,2]
					MmomentsD[number,1] = Mforces[number,0]*CE[number,2]-Mforces[number,2]*CE[number,0]
					MmomentsD[number,2] = Mforces[number,1]*CE[number,0]-Mforces[number,0]*CE[number,1]

					Mforcesy[number,0] = Mforces[number,0]* math.cos(yaw)+Mforces[number,1]*math.sin(yaw)
					Mforcesy[number,1] = Mforces[number,1]*math.cos(yaw)-Mforces[number,0]*math.sin(yaw)
					Mforcesy[number,2] = Mforces[number,2]

					MmomentsDy[number,0] = MmomentsD[number,0]*math.cos(yaw)+MmomentsD[number,1]*math.sin(yaw)
					MmomentsDy[number,1] = MmomentsD[number,1]*math.cos(yaw)-MmomentsD[number,0]*math.sin(yaw)
					MmomentsDy[number,2] = MmomentsD[number,2]

					coupleFy[number,0] = coupleF[number,0]*math.cos(yaw)+coupleF[number,1]*math.sin(yaw)
					coupleFy[number,1] = coupleF[number,1]*math.cos(yaw)-coupleF[number,0]*math.sin(yaw)
					coupleFy[number,2] = coupleF[number,2]
			    
				if totalA[number] == 0:
					Cx = 0
					Cz = 0
					cup = 0
				else:
					Cx = Mforces[number,0]/(0.5*Adens*totalA[number]*AWSS*AWSS)
					Cz = Mforces[number,1]/(0.5*Adens*totalA[number]*AWSS*AWSS)
					cup = Mforces[number,2]/(0.5*Adens*totalA[number]*AWSS*AWSS)
				clift = Cz*math.cos(-AWA)-Cx*math.sin(-AWA)
				coeff[number,0] = Cx*math.cos(-AWA)+Cz*math.sin(-AWA)
				coeff[number,1] = math.cos(heel)*clift-math.sin(heel)*cup
				coeff[number,2] = math.cos(heel)*cup+math.sin(heel)*clift
		except IndexError:
			fallo = ['Fallo en la recogida de datos']
			pass
		except ValueError:
			fallo = ['Fallo en el calculo de ciertos datos']
			pass
		finally:
			#All data gathered, time to write the csv files
			for cfd_part in ['hull', 'sails', 'rig']:
				filename_suffix = "-trans-"
				part_suffix = cfd_part
				file_extension = ".csv"
				filename = os.path.join(args.projectname + filename_suffix + part_suffix + file_extension)
				csv_file = open(filename, "ab")
				csv_write = csv.writer(csv_file)
				if args.gonz:
					if cfd_part == "hull":
						if len(fallo) == 0:
							data2csv = [sail, sail_trim, proj_dir, TWSMH*vconv, math.degrees(TWA), math.degrees(heel), math.degrees(yaw), BS*vconv]
							data2csv.extend([totalA[1]])
							data2csv.extend([hnumber[1], coeff[1,1], -coeff[1,0], coeff[1,2], CEH[1,0], CEH[1,1], CEH[1,2], Mforcesy[1,0], Mforcesy[1,1], Mforcesy[1,2], MmomentsDy[1,0]+coupleF[1,0], MmomentsDy[1,1]+coupleF[1,1], MmomentsDy[1,2]+coupleF[1,2], coupleFy[1,0], coupleFy[1,1], coupleFy[1,2]])
							data2csv.insert(10, AWSS*vconv)
							data2csv.insert(11, math.degrees(AWA))
							data2csv.insert(18, math.degrees(TWA+yaw))
							csv_write.writerow(data2csv)
						else:
							#data2csv.insert(0, fallo)
							csv_write.writerow(fallo)
					elif cfd_part == "sails":
						if len(fallo) == 0:
							data2csv = [sail, sail_trim, proj_dir, TWSMH*vconv, math.degrees(TWA), math.degrees(heel), math.degrees(yaw), BS*vconv]
							data2csv.extend([totalA[0]])
							data2csv.extend([hnumber[0], coeff[0,1], -coeff[0,0], coeff[0,2], CEH[0,0], CEH[0,1], CEH[0,2], Mforcesy[0,0], Mforcesy[0,1], Mforcesy[0,2], MmomentsDy[0,0]+coupleF[0,0], MmomentsDy[0,1]+coupleF[0,1], MmomentsDy[0,2]+coupleF[0,2], coupleFy[0,0], coupleFy[0,1], coupleFy[0,2]])
							data2csv.insert(10, AWSS*vconv)
							data2csv.insert(11, math.degrees(AWA))
							data2csv.insert(18, math.degrees(TWA+yaw))
							csv_write.writerow(data2csv)        
						else:
							#data2csv.insert(0, fallo)
							csv_write.writerow(fallo)
					else:
						if len(fallo) == 0:
							data2csv = [sail, sail_trim, proj_dir, TWSMH*vconv, math.degrees(TWA), math.degrees(heel), math.degrees(yaw), BS*vconv]
							data2csv.extend([totalA[2]])
							data2csv.extend([hnumber[2], coeff[2,1], -coeff[2,0], coeff[2,2], CEH[2,0], CEH[2,1], CEH[2,2], Mforcesy[2,0], Mforcesy[2,1], Mforcesy[2,2], MmomentsDy[2,0]+coupleF[2,0], MmomentsDy[2,1]+coupleF[2,1], MmomentsDy[2,2]+coupleF[2,2], coupleFy[2,0], coupleFy[2,1], coupleFy[2,2]])
							data2csv.insert(10, AWSS*vconv)
							data2csv.insert(11, math.degrees(AWA))
							data2csv.insert(18, math.degrees(TWA+yaw))
							csv_write.writerow(data2csv)
						else:
							#data2csv.insert(0, fallo)
							csv_write.writerow(fallo)
							fallo = []
				else:
					if cfd_part == "hull":
						if len(fallo) == 0:
							data2csv = [sail, sail_trim, proj_dir, TWSMH*vconv, math.degrees(TWA), math.degrees(heel), math.degrees(yaw), BS*vconv]
							data2csv.extend([totalA[1]])
							data2csv.extend([Mforces[1,0], Mforces[1,1], Mforces[1,2], (MmomentsD[1,0]+coupleF[1,0]), (MmomentsD[1,1]+coupleF[1,1]), (MmomentsD[1,2]+coupleF[1,2]), coupleF[1,0], coupleF[1,1], coupleF[1,2], hnumber[1], coeff[1,1], -coeff[1,0], coeff[1,2], CEH[1,0], CEH[1,1], CEH[1,2], Mforcesy[1,0], Mforcesy[1,1], Mforcesy[1,2], MmomentsDy[1,0]+coupleF[1,0], MmomentsDy[1,1]+coupleF[1,1], MmomentsDy[1,2]+coupleF[1,2], coupleFy[1,0], coupleFy[1,1], coupleFy[1,2]])
							data2csv.insert(19, AWSS*vconv)
							data2csv.insert(20, math.degrees(AWA))
							data2csv.insert(27, math.degrees(TWA+yaw))
							csv_write.writerow(data2csv)
						else:
							#data2csv.insert(0, fallo)
							csv_write.writerow(fallo)
					elif cfd_part == "sails":
						if len(fallo) == 0:
							data2csv = [sail, sail_trim, proj_dir, TWSMH*vconv, math.degrees(TWA), math.degrees(heel), math.degrees(yaw), BS*vconv]
							data2csv.extend([totalA[0]])
							data2csv.extend([Mforces[0,0], Mforces[0,1], Mforces[0,2], (MmomentsD[0,0]+coupleF[0,0]), (MmomentsD[0,1]+coupleF[0,1]), (MmomentsD[0,2]+coupleF[0,2]), coupleF[0,0], coupleF[0,1], coupleF[0,2], hnumber[0], coeff[0,1], -coeff[0,0], coeff[0,2], CEH[0,0], CEH[0,1], CEH[0,2], Mforcesy[0,0], Mforcesy[0,1], Mforcesy[0,2], MmomentsDy[0,0]+coupleF[0,0], MmomentsDy[0,1]+coupleF[0,1], MmomentsDy[0,2]+coupleF[0,2], coupleFy[0,0], coupleFy[0,1], coupleFy[0,2]])
							data2csv.insert(19, AWSS*vconv)
							data2csv.insert(20, math.degrees(AWA))
							data2csv.insert(27, math.degrees(TWA+yaw))
							csv_write.writerow(data2csv)
						else:
							#data2csv.insert(0, fallo)
							csv_write.writerow(fallo)
					else:
						if len(fallo) == 0:
							data2csv = [sail, sail_trim, proj_dir, TWSMH*vconv, math.degrees(TWA), math.degrees(heel), math.degrees(yaw), BS*vconv]
							data2csv.extend([totalA[2]])
							data2csv.extend([Mforces[2,0], Mforces[2,1], Mforces[2,2], (MmomentsD[2,0]+coupleF[2,0]), (MmomentsD[2,1]+coupleF[2,1]), (MmomentsD[2,2]+coupleF[2,2]), coupleF[2,0], coupleF[2,1], coupleF[2,2], hnumber[2], coeff[2,1], -coeff[2,0], coeff[2,2], CEH[2,0], CEH[2,1], CEH[2,2], Mforcesy[2,0], Mforcesy[2,1], Mforcesy[2,2], MmomentsDy[2,0]+coupleF[2,0], MmomentsDy[2,1]+coupleF[2,1], MmomentsDy[2,2]+coupleF[2,2], coupleFy[2,0], coupleFy[2,1], coupleFy[2,2]])
							data2csv.insert(19, AWSS*vconv)
							data2csv.insert(20, math.degrees(AWA))
							data2csv.insert(27, math.degrees(TWA+yaw))
							csv_write.writerow(data2csv)
						else:
							#data2csv.insert(0, fallo)
							csv_write.writerow(fallo)
							fallo = []
