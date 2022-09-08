
# Author:         Stephen Hurt 
# Author Contact: stephenhurt99@tamu.edu 
# This code builds line relays for a given PowerWorld case

from esa import SAW

FILE_NAME = r"C:\Users\steph\PowerWorldCases\ACTIVSg200\ACTIVSg200.PWB"
saw = SAW(FILE_NAME)

# get branch fields
branch_fields = saw.GetParametersMultipleElement('branch', ['BusNum', 'BusNum:1', 'LineCircuit', 'BusName_NomVolt', 'BusName_NomVolt:1', 'AreaName', 'AreaName:1', 'ZMag', 'ZAng', 'BranchDeviceType', 'LineLimAmp'])
aux_file_name = FILE_NAME[:FILE_NAME.rfind("\\") + 1] + 'line_relays_{}.aux'.format(FILE_NAME[FILE_NAME.rfind("\\") + 1:-4])
# create an aux file and load the relays into it
with open(aux_file_name, 'w') as file:
    # write in distance relays
    print("Writing DISTRELAYs...")
    file.write("LineRelayModel_DISTRELAY (BusNumFrom,BusNumTo,Circuit,BusNameNomkVFrom,BusNameNomkVTo,DeviceEnd,DeviceID,AreaNameFrom,AreaNameTo,ModelType,Status,Criteria,SubIntervalsUsed,DiffModified,DefaultData,ModelClass,Zone1Reach,Zone2Reach,Zone3Reach,OtherObject:0,OtherObject:1,OtherObject:2,OtherObject:3,OtherObject:4,OtherObject:5,OtherObject:6,OtherObject:7,OtherObject:8,OtherObject:9,OtherObject:10,OtherObject:11,Notrip,Shape1,Shape2,Shape3,Shape4,TransferType,UseLoadEncroach,NumDirect,RecloseWithFault,DirectTrip,DirectReclose,TransferTrip,TransferReclose,Angle1,Wt1,Rr1,InternalAng1,Rb1,T1,IThres1,Angle2,Wt2,Rr2,InternalAng2,Rb2,T2,IThres2,Angle3,Wt3,Rr3,InternalAng3,Rb3,T3,IThres3,Angle4,Wt4,Rr4,InternalAng4,Rb4,T4,IThres4,BlindType0,BlindInt0,BlindRot0,BlindType1,BlindInt1,BlindRot1,BlindType2,BlindInt2,BlindRot2,BlindType3,BlindInt3,BlindRot3,FarRelayEnd)")
    file.write('\n{\n')
    for index in branch_fields.index:
        branch = branch_fields.iloc[index]
        # skip everything but lines; there are some transformers that need to be skipped
        if branch['BranchDeviceType'] != "Line":
            continue
        # calculate impedence from the normalized impedence
        branch_impedence = branch['ZMag'] * (float(branch['BusName_NomVolt'][-5:]) ** 2) / 100
        impedence_angle = branch['ZAng']
        relay_data = f"{branch['BusNum']}   {branch['BusNum:1']} \"{branch['LineCircuit']}\" \"{branch['BusName_NomVolt']}\" \"{branch['BusName_NomVolt:1']}\" \"From\" \"1\" \"{branch['AreaName']}\" \"{branch['AreaName:1']}\" \"DISTRELAY\" \"Active\" \"\" \"\" \"\" \"\" \"Line Relay Model\" \"\" \"\" \"\" \"Bus \'{branch['BusNum:1']}\'\" \"Branch \'{branch['BusNum']}\' \'{branch['BusNum:1']}\' \'{branch['LineCircuit']}\'\" \"Bus \'{branch['BusNum']}\'\" \"Branch \'{branch['BusNum']}\' \'{branch['BusNum:1']}\' \'{branch['LineCircuit']}\'\" \"Bus \'{branch['BusNum:1']}\'\" \"Branch \'{branch['BusNum']}\' \'{branch['BusNum:1']}\' \'{branch['LineCircuit']}\'\" \"none\" \"none\" \"none\" \"none\" \"none\" \"none\"         0         0         0         0         0         0         0         2         1 1 10 2 10 {impedence_angle} {branch_impedence * 0.9} 0 90 0 0 -1 {impedence_angle} {branch_impedence * 1.2} 0 90 0 0.1 -1 {impedence_angle} {branch_impedence * 2.2} 0 90 0 0.5 -1 0 0 0 90 0 0 0 0 \"0\" \"0\" 0 \"0\" \"0\" 0 \"0\" \"0\" 0 \"0\" \"0\" 0\n"
        file.write(relay_data)
        relay_data = f"{branch['BusNum']}   {branch['BusNum:1']} \"{branch['LineCircuit']}\" \"{branch['BusName_NomVolt']}\" \"{branch['BusName_NomVolt:1']}\" \"To\" \"1\" \"{branch['AreaName']}\" \"{branch['AreaName:1']}\" \"DISTRELAY\" \"Active\" \"\" \"\" \"\" \"\" \"Line Relay Model\" \"\" \"\" \"\" \"Bus \'{branch['BusNum:1']}\'\" \"Branch \'{branch['BusNum']}\' \'{branch['BusNum:1']}\' \'{branch['LineCircuit']}\'\" \"Bus \'{branch['BusNum']}\'\" \"Branch \'{branch['BusNum']}\' \'{branch['BusNum:1']}\' \'{branch['LineCircuit']}\'\" \"Bus \'{branch['BusNum:1']}\'\" \"Branch \'{branch['BusNum']}\' \'{branch['BusNum:1']}\' \'{branch['LineCircuit']}\'\" \"none\" \"none\" \"none\" \"none\" \"none\" \"none\"         0         0         0         0         0         0         0         2         1 1 10 2 10 {impedence_angle} {branch_impedence * 0.9} 0 90 0 0 -1 {impedence_angle} {branch_impedence * 1.2} 0 90 0 0.1 -1 {impedence_angle} {branch_impedence * 2.2} 0 90 0 0.5 -1 0 0 0 90 0 0 0 0 \"0\" \"0\" 0 \"0\" \"0\" 0 \"0\" \"0\" 0 \"0\" \"0\" 0\n"
        file.write(relay_data)
    file.write('}\n')
    print("Writing TIOCRSs...")
    # write in overcurrent relays
    file.write("LineRelayModel_TIOCRS (BusNumFrom,BusNumTo,Circuit,BusNameNomkVFrom,BusNameNomkVTo,DeviceEnd,DeviceID,AreaNameFrom,AreaNameTo,ModelType,Status,Criteria,SubIntervalsUsed,DiffModified,DefaultData,ModelClass,Zone1Reach,Zone2Reach,Zone3Reach,OtherObject:0,OtherObject:1,OtherObject:2,OtherObject:3,RelaySlot,Monitor,CurveType,ThresholdCurrent,BreakerTime,Tdm,ResetTime,p,A,B,C,D,E,t3trip,direct)")
    file.write('\n{\n')
    for index in branch_fields.index:
        branch = branch_fields.iloc[index]
        if branch['BranchDeviceType'] != "Line":
            continue
        relay_data = f"{branch['BusNum']}   {branch['BusNum:1']} \"{branch['LineCircuit']}\" \"{branch['BusName_NomVolt']}\" \"{branch['BusName_NomVolt:1']}\" \"From\" \"1\" \"{branch['AreaName']}\" \"{branch['AreaName:1']}\" \"TIOCRS\" \"Active\" \"\" \"\" \"\" \"IEEE C37.113 Moderately Inverse\" \"Line Relay Model\" \"\" \"\" \"\" \"Branch \'{branch['BusNum']}\'   \'{branch['BusNum:1']}\' \'{branch['LineCircuit']}\'\" \"none\" \"none\" \"none\"         1         1         1 {branch['LineLimAmp']*1.1} 0 \"1\" 0.1 2.0 0.0833 0.0833 0 0 0 0 0\n"
        file.write(relay_data)
        relay_data = f"{branch['BusNum']}   {branch['BusNum:1']} \"{branch['LineCircuit']}\" \"{branch['BusName_NomVolt']}\" \"{branch['BusName_NomVolt:1']}\" \"To\" \"1\" \"{branch['AreaName']}\" \"{branch['AreaName:1']}\" \"TIOCRS\" \"Active\" \"\" \"\" \"\" \"IEEE C37.113 Moderately Inverse\" \"Line Relay Model\" \"\" \"\" \"\" \"Branch \'{branch['BusNum']}\'   \'{branch['BusNum:1']}\' \'{branch['LineCircuit']}\'\" \"none\" \"none\" \"none\"         1         1         1 {branch['LineLimAmp']*1.1} 0 \"1\" 0.1 2.0 0.0833 0.0833 0 0 0 0 0\n"
        file.write(relay_data)
    file.write('}\n')
print(f"All relays written to {aux_file_name}")
