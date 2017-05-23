#!/bin/bash

for file in `ls *.csv`
do
	if [ -e "${file}_orig" ]
	then
		if [ "${file}" -nt "${file}_orig" ]
		then
			fieldsf=`echo $RANDOM`
			touch $fieldsf
			echo "Hull,Sailset,Sail Trim,Dagger,Canting,Trim Tab,TWS,TWA,AWS_mh,AWA_mh,TWS_ce,AWS_ce,AWA_ce,TWS_10m,AWS_10m,AWA_10m,BoatSpeed,VMG,Heel,Leeway,Rudder,WS,Trim,Sink,Mass,Xcg,Ycg,Zcg,Flat,Cl,Cd,Cup,h,Xce,Yce,Zce,Heeling Force,Righting Moment,Fx,Fy,Fz,Mx,My,Mz,Fx,Fy,Fz,Mx,My,Mz,Delta_Mx,Delta_Mx_deflection,Fx,Fy,Fz,Mx,My,Mz,AoA,Cl,Cd,SCl,SCd,h,Fx,Fy,Fz,Mx,My,Mz,Cl,Cd,SCl,SCd,h,Fx,Fy,Fz,Mx,My,Mz,AoA,Cl,Cd,SCl,SCd,h,Fx,Fy,Fz,Mx,My,Mz,AoA,Cl,Cd,SCl,SCd,h,R_Angle, Fx, Fy, Fz, Mx, My, Mz, AoA, Cl, Cd, h, WS,R_Angle,Hull Area,Hull Fx,Hull Fy,Hull Fz,Hull Mx,Hull My,Hull Mz, Cl, Cd, Cup, h, Xce, Yce, Zce,Rudder Fx,Rudder Fy,Rudder Fz,Rudder Mx,Rudder My,Rudder Mz,Rig Area,Rig Fx,Rig Fy,Rig Fz,Rig Mx,Rig My,Rig Mz,Rig Cl,Rig Cd, Cup,h, Xce, Yce, Zce,Drag,Side Force,RFx,RFy,RFz,RMx,RMy,RMz,," > ${file}_new
			lines=$(cat $file | wc -l)
			for line in `seq 1 $lines`
			do
				head -n $line $file | tail -1 | awk -F',' '{print NF}' >> $fieldsf
			done
			maxfields=$(sort -nu $fieldsf | tail -1)
			for line in `seq 1 $lines`
			do
				fields=$(head -n $line $file | tail -1 | awk -F',' '{print NF}')
				if [ "$fields" -lt "$maxfields" ]
				then
					#do nothing
					true
				else
					echo $(head -n $line $file | tail -1) >> ${file}_new
				fi
			done
			/bin/mv $file ${file}_orig
			/bin/mv ${file}_new $file
			/bin/rm $fieldsf
			touch ${file}_orig
		else
			echo "File ${file} processed previously so do nothing..."
		fi
	else
		fieldsf=`echo $RANDOM`
		touch $fieldsf
		echo "Hull,Sailset,Sail Trim,Dagger,Canting,Trim Tab,TWS,TWA,AWS_mh,AWA_mh,TWS_ce,AWS_ce,AWA_ce,TWS_10m,AWS_10m,AWA_10m,BoatSpeed,VMG,Heel,Leeway,Rudder,WS,Trim,Sink,Mass,Xcg,Ycg,Zcg,Flat,Cl,Cd,Cup,h,Xce,Yce,Zce,Heeling Force,Righting Moment,Fx,Fy,Fz,Mx,My,Mz,Fx,Fy,Fz,Mx,My,Mz,Delta_Mx,Delta_Mx_deflection,Fx,Fy,Fz,Mx,My,Mz,AoA,Cl,Cd,SCl,SCd,h,Fx,Fy,Fz,Mx,My,Mz,Cl,Cd,SCl,SCd,h,Fx,Fy,Fz,Mx,My,Mz,AoA,Cl,Cd,SCl,SCd,h,Fx,Fy,Fz,Mx,My,Mz,AoA,Cl,Cd,SCl,SCd,h,R_Angle, Fx, Fy, Fz, Mx, My, Mz, AoA, Cl, Cd, h, WS,R_Angle,Hull Area,Hull Fx,Hull Fy,Hull Fz,Hull Mx,Hull My,Hull Mz, Cl, Cd, Cup, h, Xce, Yce, Zce,Rudder Fx,Rudder Fy,Rudder Fz,Rudder Mx,Rudder My,Rudder Mz,Rig Area,Rig Fx,Rig Fy,Rig Fz,Rig Mx,Rig My,Rig Mz,Rig Cl,Rig Cd, Cup,h, Xce, Yce, Zce,Drag,Side Force,RFx,RFy,RFz,RMx,RMy,RMz,," > ${file}_new
		lines=$(cat $file | wc -l)
		for line in `seq 1 $lines`
		do
			head -n $line $file | tail -1 | awk -F',' '{print NF}' >> $fieldsf
		done
		maxfields=$(sort -nu $fieldsf | tail -1)
		for line in `seq 1 $lines`
		do
			fields=$(head -n $line $file | tail -1 | awk -F',' '{print NF}')
			if [ "$fields" -lt "$maxfields" ]
			then
				#do nothing
				true
			else
				echo $(head -n $line $file | tail -1) >> ${file}_new
			fi
		done
		/bin/mv $file ${file}_orig
		/bin/mv ${file}_new $file
		/bin/rm $fieldsf
		touch ${file}_orig 
	fi
done
