
# Author: Stephen Hurt  |  stephenhurt99@tamu.edu
# Date: 07/18/2022
# Python 3.9.13
# pandas 1.4.2
# numpy 1.21.6
# esa 1.2.7
# matplotlib 3.3.3
# This code creates synthetic generator capability curves for gas turbine generators
# It then writes the curve data to a *.csv and a *.aux file so that it can be stored, viewed, and loaded into PowerWorld Simulator.

from select import select
import matplotlib.pyplot as plt
import numpy as np
import math
from esa import SAW
import pandas as pd
import os

FILE_PATH = r"C:\Users\steph\PowerWorldCases\ACTIVSg2000\ACTIVSg2000.pwb"

saw = SAW(FILE_PATH)

def armature_current_limit(p, R, pos=True):
    if p > R:
        return
    if pos:
        return math.sqrt(R ** 2 - p ** 2)
    else:
        return -math.sqrt(R ** 2 - p ** 2)

def end_field_current_limit(Qo, r, P, pos=True):
    if P > r:
        return
    if pos:
        return Qo + math.sqrt(r ** 2 - P ** 2)
    else:
        return Qo - math.sqrt(r ** 2 - P ** 2)

# maximum and minimum constraints from PowerWorld
def get_pw_constraints(genData):
    global Pmax, Pmin, Qmax, Qmin, baseMVA
    Pmax = genData['GenMWMax']
    Pmin = genData['GenMWMin']
    Qmax = genData['GenMVRMax']
    Qmin = genData['GenMVRMin']
    baseMVA = genData['GenMVABase']

def create_curve(genData):
    get_pw_constraints(genData)
    global p_vals, pos_q_vals, neg_q_vals, pos_field_vals, neg_field_vals, maxMVA, baseMVA
    # find the minPf where the field current limit intersects the armature current limit
    pos_min_pf = Pmax / math.sqrt(Pmax ** 2 + Qmax ** 2)
    # create a maxMVA that is less than the name plate rating based on the given Qmax and Pmax
    maxMVA = Pmax / pos_min_pf
    # create an absolute Qmax that is larger than the given Qmax. This is done by using the nameplate MVA rating which is larger
    print()
    # this is just to handle odd cases when, for some reason, the baseMVA is less than the, maxMVA
    if baseMVA <= maxMVA:
        baseMVA = maxMVA * 1.01
    absQmax = math.sqrt(baseMVA ** 2 - Pmax ** 2)

    Rmax = maxMVA
    p_vals = np.arange(0, int(maxMVA) + 1, 0.001)
    pos_q_vals = np.zeros(len(p_vals))
    neg_q_vals = np.zeros(len(p_vals))


    # find the negative power factor which is where the armature current limit intersects the given Qmin
    neg_min_pf = Pmax / math.sqrt(Pmax ** 2 + Qmin ** 2)
    # find the real power where the armature current limit intersects the given Qmin
    P_atQmin_corner = neg_min_pf * maxMVA
    # create an absQmin by using the name plate rating which is larger than the maxMVA curve
    absQmin = -math.sqrt(baseMVA ** 2 - P_atQmin_corner ** 2)
    # calculate Qofield documented here: https://molzahn.github.io/pubs/molzahn_friedman_lesieutre_demarco_ferris-naps2015.pdf
    FieldCoef = math.sqrt(1 - pos_min_pf ** 2)
    QoField = (absQmax ** 2 - maxMVA ** 2) / (2 * (absQmax - FieldCoef * maxMVA))
    Rfield = absQmax - QoField
    # calculate Qoend documented at the above link
    coef = math.sqrt(1 - neg_min_pf ** 2)
    Qoend = (absQmin ** 2 - maxMVA ** 2) / (2 * (absQmin + coef * maxMVA))
    Rend = -absQmin + Qoend


    for i in range(len(p_vals)):
        pos_q_vals[i] = armature_current_limit(p_vals[i], Rmax)
        neg_q_vals[i] = armature_current_limit(p_vals[i], Rmax, False)

    pos_field_vals = np.zeros(len(p_vals))
    neg_field_vals = np.zeros(len(p_vals))

    for i in range(len(p_vals)):
        pos_field_vals[i] = end_field_current_limit(QoField, Rfield, p_vals[i])
        neg_field_vals[i] = end_field_current_limit(Qoend, Rend, p_vals[i], False)
first_run = True
# write data to *.aux file
def write_aux(GenData: pd.Series):
    global first_run
    aux_file = FILE_PATH[:FILE_PATH.rfind("\\") + 1] + 'gen_capability_curves_{}.aux'.format(FILE_PATH[FILE_PATH.rfind("\\") + 1:-4])
    if first_run and os.path.exists(aux_file):
        os.remove(aux_file)
    first_run = False
    # this function opens an .aux with the name of the generator. If all generator data is desired to be in the same file. Change the name and change 'w' to 'a'
    with open(aux_file, 'a') as file: 
        file.write('Gen (BusNum,BusName,NomkV,ID,Status,VoltSet,VoltSetTol,RegBusNum,RegFactor,AGC,PartFact,MWSetPoint,MWMax,MWMin,EnforceMWLimit,AVR,MvarSetPoint,MvarMax,MvarMin,UseCapCurve,WindContMode,WindContModePF,UseLineDrop,Rcomp,Xcomp,VoltageDroopControl,MVABase,GenR,GenX,StepR,StepX,StepTap,GovRespLimit,UnitTypeCode,FuelTypeCode,AreaNumber,ZoneNumber,BANumber,OwnerNum1,OwnerPerc1,OwnerNum2,OwnerPerc2,OwnerNum3,OwnerPerc3,OwnerNum4,OwnerPerc4,OwnerNum5,OwnerPerc5,OwnerNum6,OwnerPerc6,OwnerNum7,OwnerPerc7,OwnerNum8,OwnerPerc8,EMSType,EMSID,DataMaintainerAssign,DataMaintainerInherit,AllLabels)')
        file.write('\n{\n')
        file.write(f'{GenData.name[0]} "{GenData["BusName"]}"   {GenData["BusNomVolt"]} "{GenData.name[1]}" "{GenData["GenStatus"]}"   {GenData["GenVoltSet"]} {GenData["VoltSetTol"]}   {GenData["GenRegNum"]} {GenData["GenRMPCT"]} "{GenData["GenAGCAble"]}"   {GenData["GenParFac"]}    {GenData["GenMWSetPoint"]}   {GenData["GenMWMax"]}   {GenData["GenMWMin"]} "{GenData["GenEnforceMWLimits"]}" "{GenData["GenAVRAble"]}"   {GenData["GenMvrSetPoint"]}   {GenData["GenMVRMax"]}   {GenData["GenMVRMin"]} "YES" "{GenData["GenWindControlMode"]}" {GenData["GenWindPowerFactor"]} "{GenData["GenUseLDCRCC"]}"      {GenData["GenRLDCRCC"]} {GenData["GenXLDCRCC"]} "{GenData["DCName"]}"  {GenData["GenMVABase"]} {GenData["GenZR"]} {GenData["GenZX"]} {GenData["GenStepR"]} {GenData["GenStepX"]} {GenData["GenStepTap"]} "{GenData["TSGovRespLimit"]}"    "{GenData["GenUnitType:1"]}" "{GenData["GenFuelType:1"]}"      {GenData["AreaNum"]}     {GenData["ZoneNum"]}      {GenData["BANumber"]}     {GenData["OwnerNum"]} {GenData["OwnPercent"]} {GenData["OwnerNum:1"]} {GenData["OwnPercent:1"]} {GenData["OwnerNum:2"]} {GenData["OwnPercent:2"]} {GenData["OwnerNum:3"]} {GenData["OwnPercent:3"]} {GenData["OwnerNum:4"]} {GenData["OwnPercent:4"]} {GenData["OwnerNum:5"]} {GenData["OwnPercent:5"]} {GenData["OwnerNum:6"]} {GenData["OwnPercent:6"]} {GenData["OwnerNum:7"]} {GenData["OwnPercent:7"]} "{GenData["EMSType"]}" "{GenData["EMSDeviceID"]}" "{GenData["DataMaintainerAssign"]}" "{GenData["DataMaintainerInherit"]}" "{GenData["AllLabels"]}"')

        file.write('\n}\n\n')
        file.write('ReactiveCapability (BusNum,BusName,NomkV,ID,MW,MvarMax,MvarMin)\n')
        file.write('{\n')
        len_p_vals = len(p_vals)
        num_data_points = 30
        select_distance = int(len_p_vals / num_data_points)
        for i in range(num_data_points):
            if p_vals[i*select_distance] < Pmin:
                continue
            elif p_vals[i*select_distance] > maxMVA:
                break
            file.write(f'{GenData.name[0]} "{GenData["BusName"]}" {GenData["BusNomVolt"]} "{GenData.name[1]}"   ')
            mw = p_vals[i*select_distance]
            if pos_field_vals[i*select_distance] < pos_q_vals[i*select_distance]:
                maxMvar = pos_field_vals[i*select_distance]
            else:
                maxMvar = pos_q_vals[i*select_distance]
            if neg_q_vals[i*select_distance] > neg_field_vals[i*select_distance]:
                minMvar = neg_q_vals[i*select_distance]
            else:
                minMvar = neg_field_vals[i*select_distance]
            file.write('{}   {}   {}\n'.format(round(mw, 3), round(maxMvar, 3), round(minMvar, 3)))

        file.write('}\n')
# write data to *.csv file
def write_csv(GenData: pd.Series):
    # this function opens a .csv with the name of the generator. If all generator data is desired to be in the same file. Change the name and change 'w' to 'a'
    with open('gen{}.csv'.format(GenData.name[0]), 'w') as file:
        file.write('ReactiveCapability,\n')
        file.write('Number of Bus,Name of Bus,Nom kV of Bus,ID of Gen,Gen MW of Gen,Min Mvar of Gen,Max Mvar of Gen,\n')
        len_p_vals = len(p_vals)
        num_data_points = 30
        select_distance = int(len_p_vals / num_data_points)
        for i in range(num_data_points):
            if p_vals[i*select_distance] < Pmin:
                continue
            elif p_vals[i*select_distance] > maxMVA:
                break
            file.write(f'{GenData.name[0]}, {GenData["BusName"]}, {GenData["BusNomVolt"]}, {GenData.name[1]},')
            mw = p_vals[i*select_distance]
            if pos_field_vals[i*select_distance] < pos_q_vals[i*select_distance]:
                maxMvar = pos_field_vals[i*select_distance]
            else:
                maxMvar = pos_q_vals[i*select_distance]
            if neg_q_vals[i*select_distance] > neg_field_vals[i*select_distance]:
                minMvar = neg_q_vals[i*select_distance]
            else:
                minMvar = neg_field_vals[i*select_distance]
            file.write('{},{},{},\n'.format(round(mw, 3), round(minMvar, 3), round(maxMvar, 3)))

        file.write('}\n')
# graph the generator capability curve
def graph_curve(gen):
    global p_vals
    for i in range(len(p_vals)):
        if p_vals[i] > maxMVA:
            pos_field_vals[i] = 'nan'
            neg_q_vals[i] = 'nan'
            neg_field_vals[i] = 'nan'
            pos_q_vals[i] = 'nan'
        if pos_field_vals[i] > pos_q_vals[i]:
            pos_field_vals[i] = 'nan'
        if pos_field_vals[i] <= pos_q_vals[i]:
            pos_q_vals[i] = 'nan'
        if neg_field_vals[i] <= neg_q_vals[i]:
            neg_field_vals[i] = 'nan'
        if neg_field_vals[i] > neg_q_vals[i]:
            neg_q_vals[i] = 'nan'
    plt.figure()
    plt.title('Generator {} {}'.format(gen[0], gen[1]))
    
    plt.xlabel('Generator Real Power Output (MW)')
    plt.ylabel('Generator Reactive Power Output (MVAR)')
    all_pos_q_vals = np.zeros(len(p_vals))
    
    for i, f, q in zip(range(len(p_vals)), pos_field_vals, pos_q_vals):
        if not math.isnan(f):
            all_pos_q_vals[i] = f
        elif not math.isnan(q):
            all_pos_q_vals[i] = q
        else:
            all_pos_q_vals[i] = 'nan'
    all_neg_q_vals = np.zeros(len(p_vals))
    
    for i, f, q in zip(range(len(p_vals)), neg_field_vals, neg_q_vals):
        if not math.isnan(f):
            all_neg_q_vals[i] = f
        elif not math.isnan(q):
            all_neg_q_vals[i] = q
        else:
            all_neg_q_vals[i] = 'nan'
    count = 0
    all_pos_q_vals2 = []
    all_neg_q_vals2 = []
    while not math.isnan(all_pos_q_vals[count]) and not math.isnan(all_neg_q_vals[count]):
        
        all_pos_q_vals2.append(all_pos_q_vals[count])
        all_neg_q_vals2.append(all_neg_q_vals[count])
        count +=1
    all_pos_q_vals = all_pos_q_vals2
    all_neg_q_vals = all_neg_q_vals2
    p_vals2 = []
    for i in range(len(all_pos_q_vals)):
        p_vals2.append(p_vals[i])
    p_vals = p_vals2
    list_of_points = []
    for i, p in enumerate(p_vals):
        list_of_points.append([p, all_pos_q_vals[i]])
    for i in range(len(p_vals)):
        i = -i - 1
        list_of_points.append([p_vals[i], all_neg_q_vals[i]])
    x = [point[0] for point in list_of_points]
    y = [point[1] for point in list_of_points]
    plt.plot(x, y, label='Synthetic Generator Capability Curve')
    plt.plot([0, Pmax, Pmax, 0], [Qmax, Qmax, Qmin, Qmin], label='Known Generator Capbility Parameters')
    
    plt.grid()
    plt.show()

# get all of the data needed to build the .aux file from PowerWorld
gen_list = saw.GetParametersMultipleElement('gen', ['BusNum', 'BusName', 'BusNomVolt', 'GenID', 'GenStatus', 'GenVoltSet', 'VoltSetTol', 'GenRegNum', 'GenRMPCT', 'GenAGCAble', 'GenParFac', 'GenMWSetPoint', 'GenMWMax','GenMWMin', 'GenEnforceMWLimits', 'GenAVRAble', 'GenMvrSetPoint', 'GenMVRMax', 'GenMVRMin', 'GenWindControlMode', 'GenWindPowerFactor', 'GenUseLDCRCC', 'GenRLDCRCC', 'GenXLDCRCC', 'DCName', 'GenMVABase', 'GenZR', 'GenZX', 'GenStepR', 'GenStepX', 'GenStepTap', 'TSGovRespLimit', 'GenUnitType:1', 'GenFuelType:1', 'AreaNum', 'ZoneNum', 'BANumber', 'OwnerNum', 'OwnPercent','OwnerNum:1', 'OwnPercent:1','OwnerNum:2', 'OwnPercent:2','OwnerNum:3', 'OwnPercent:3','OwnerNum:4', 'OwnPercent:4','OwnerNum:5', 'OwnPercent:5','OwnerNum:6', 'OwnPercent:6','OwnerNum:7', 'OwnPercent:7', 'EMSType', 'EMSDeviceID', 'DataMaintainerAssign', 'DataMaintainerInherit', 'AllLabels'])
gen_list.set_index(['BusNum', 'GenID'], inplace=True)

# This is a list of generators for which a user wants capability curves
wanted_gen_list = [(1053, '1'), (3044, '1'), (1081, '1'), (2085, '1'), (8087, '1'), (3133, '1')]


# loop through all of the generators in the case and build a curve for them
for generator in gen_list.iterrows():
    generator = generator[1]
    # skip wind and solar because this capability curve does not accurately model their capability
    if str(generator['GenFuelType:1']) == 'WND' or str(generator['GenFuelType:1']) == 'SUN':
        continue
    print(generator)
    create_curve(generator)
    write_aux(generator)
    # write_csv() creates a .csv file with the gen data it is commented out because the .aux file is the most useful
    # write_csv(generator)
    # graph curve graphs the capability curve that has been produced so that the user can verify that it is reasonable
    # graph_curve() should be commented out if the user wants to speed up the code
    #graph_curve(generator.name)

"""this for loop will optionally generate curves for selected generators"""
# for gen in wanted_gen_list:
#     series = gen_list.loc[[gen]].iloc[0,:]
#     print(series.name[0])
#     print(series.name[1])
#     print(series["BusName"])
#     create_curve(series)
#     write_aux(series)
#     write_csv(series)
#     graph_curve(series.name)