from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import time

#Set device
USE_CUDA = torch.cuda.is_available()
if USE_CUDA:
    device = torch.device("cuda")
    cuda = True
else:
    device = torch.device("cpu")
    cuda = False

print("Device =", device)
gpus = [0]

files = ['Simulation1.sumocfg', 'Simulation2.sumocfg', 'Simulation3.sumocfg', 'Simulation4.sumocfg', 'Simulation5.sumocfg', 'Simulation6.sumocfg', 'Simulation7.sumocfg', 'Simulation8.sumocfg', 'Simulation9.sumocfg', 'Simulation10.sumocfg', 'Simulation11.sumocfg', 'Simulation12.sumocfg', 'Simulation13.sumocfg', 'Simulation14.sumocfg']
simNum=1;
# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa
import traci.constants as tc
from random import random



#traci.trafficlight.setRedYellowGreenState("0", "GrGr")
def run():
    """execute the TraCI control loop"""
    timeSinceLastLightChange = 0
    timeStep = 0
    timeLight = -10
    inductionLoopTimesMeq = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    laneNumCarsLastCyclePerMinMeq = [0,0,0,0,0,0,0,0]
    laneNumCarsLastCyclePerMinMeqNext = [0,0,0,0,0,0,0,0]
    laneNumCarsAllowedAddMeq = [True,True,True,True,True,True,True,True]

    inductionLoopTimesBunt = [0,0,0,0,0,0,0,0]
    laneNumCarsLastCyclePerMinBunt = [0,0,0,0]
    laneNumCarsLastCyclePerMinBuntNext = [0,0,0,0]
    laneNumCarsAllowedAddBunt = [True,True,True,True]

    firstCarMeq = [0,0,0,0,0,0,0,0]
    secondCarMeq = [0,0,0,0,0,0,0,0]
    firstCarBunt = [0,0,0,0]
    secondCarBunt = [0,0,0,0]

    timeSinceFirstCarMeq = [0,0,0,0,0,0,0,0]
    timeSinceSecondCarMeq = [0,0,0,0,0,0,0,0]
    timeSinceFirstCarBunt = [0,0,0,0]
    timeSinceSecondCarBunt = [0,0,0,0]

    trainingDataCarPredictMeq = [0,0,0,0,0,0,0,0]
    trainingDataCarPredictBunt = [0,0,0,0]

    trainingDataTrafficSwitch = []
    trainingDataTrafficStay = []
    hiddenStatesTrafficSwitch = []
    hiddenStatesTrafficStay = []
    storedInputsSwitch = []
    storedInputsStay = []
    trainingTrafficTimeAssociatedSwitch = []
    trainingTrafficTimeAssociatedStay = []

    hiddenStatesTrafficSwitchLast = modelTrafficSwitch.init_states(num_layersTrafficSwitch, hidden_sizeTrafficSwitch)
    hiddenStatesTrafficStayLast = modelTrafficStay.init_states(num_layersTrafficStay, hidden_sizeTrafficStay)

    timeStartStop = 0

    '''
    trainingDataTrafficSwitch.append([0,0])
    trainingDataTrafficStay.append([0,0])
    usedTrafficSwitch.append(False)
    usedTrafficStay.append(False)
    hiddenStatesTrafficSwitch.append(modelTrafficSwitch.init_states(num_layersTrafficSwitch, hidden_sizeTrafficSwitch))
    hiddenStatesTrafficStay.append(modelTrafficStay.init_states(num_layersTrafficStay, hidden_sizeTrafficStay))
    storedInputsSwitch.append(torch.Tensor([]))
    storedInputsStay.append(torch.Tensor([]))
    '''
    outputCarPredictBuntOld = torch.zeros(4)
    outputCarPredictMeqOld = torch.zeros(8)
    carsData = []#land id, time stop, distance start stop

    hiddenCarPredictMeq = modelCarPredictMeq.init_states(num_layersCarPredictMeq, hidden_sizeCarPredictMeq)
    hiddenCarPredictBunt = modelCarPredictBunt.init_states(num_layersCarPredictBunt, hidden_sizeCarPredictBunt)
    # we start with phase 2 where EW has green
    start_time = time.time()
    lossHolderMeq=0
    lossHolderBunt=0
    lossHolderTrafficSwitch=0
    lossHolderTrafficStay=0
    traci.trafficlight.setPhase("gneJ5", 0)
    lightConfigOld = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        lossCarPredictMeq = 0
        lossCarPredictBunt = 0
        lossTrafficSwitch = 0
        lossTrafficStay = 0

        traci.simulationStep()

        timeSinceLastLightChange+=1
        timeStartStop+=1
        #calculate time since last induction presence/40 for each lane
        i = 0
        while i < 16:
            if traci.inductionloop.getLastStepVehicleNumber(str(i)) > 0:
                inductionLoopTimesMeq[i] = 0
            else:
                #divide by 40 to normalize around 0-1
                inductionLoopTimesMeq[i] += 1/40
            i+=1

        #calculate time since last induction presence/40 for each lane
        i = 16
        while i < 24:
            if traci.inductionloop.getLastStepVehicleNumber(str(i)) > 0:
                inductionLoopTimesBunt[i-16] = 0
            else:
                #divide by 40 to normalize around 0-1
                inductionLoopTimesBunt[i-16] += 1/40
            i+=1



        #CAR LAST CYCLE
        if traci.trafficlight.getPhase("gneJ5") == 0:
            #calculate # cars in last minute for each lane
            i = 0
            while i < 8:
                if timeSinceLastLightChange != 1:
                    laneNumCarsLastCyclePerMinMeqNext[i]*=(timeSinceLastLightChange-1)/60
                #new car since last step
                if traci.inductionloop.getLastStepVehicleNumber(str(i))>0 and laneNumCarsAllowedAddMeq[i]:
                    #nomalized with 15 to get around 0-1
                    if firstCarMeq[i] == 1 and secondCarMeq[i] == 1:
                        trainingDataCarPredictMeq[i]+=1
                    laneNumCarsLastCyclePerMinMeqNext[i] += 1
                    laneNumCarsAllowedAddMeq[i] = False
                if not(traci.inductionloop.getLastStepVehicleNumber(str(i))>0) and not(laneNumCarsAllowedAddMeq[i]):
                    laneNumCarsAllowedAddMeq[i] = True
                if timeSinceLastLightChange != 1:
                    laneNumCarsLastCyclePerMinMeqNext[i]/=timeSinceLastLightChange/60
                i+=1
        if traci.trafficlight.getPhase("gneJ5") == 1:
            if traci.trafficlight.getPhase("gneJ5") != lightConfigOld:
                laneNumCarsLastCyclePerMinBuntNext = [0,0,0,0]
            trainingDataCarPredictMeq=[0,0,0,0,0,0,0,0]
        if traci.trafficlight.getPhase("gneJ5") == 2:
            #calculate # cars in last minute for each lane
            i = 16
            while i < 20:
                if timeSinceLastLightChange != 1:
                    laneNumCarsLastCyclePerMinBuntNext[i-16]*=(timeSinceLastLightChange-1)/60
                #new car since last step
                if traci.inductionloop.getLastStepVehicleNumber(str(i))>0 and laneNumCarsAllowedAddBunt[i-16]:
                    #nomalized with 15 to get around 0-1
                    if firstCarBunt[i-16] == 1 and secondCarBunt[i-16] == 1:
                        trainingDataCarPredictBunt[i-16]+=1
                    laneNumCarsLastCyclePerMinBuntNext[i-16] += 1
                    laneNumCarsAllowedAddBunt[i-16] = False
                if not(traci.inductionloop.getLastStepVehicleNumber(str(i))>0) and not(laneNumCarsAllowedAddBunt[i-16]):
                    laneNumCarsAllowedAddBunt[i-16] = True
                if timeSinceLastLightChange != 1:
                    laneNumCarsLastCyclePerMinBuntNext[i-16]/=timeSinceLastLightChange/60
                i+=1
        if traci.trafficlight.getPhase("gneJ5") == 3:
            if traci.trafficlight.getPhase("gneJ5") != lightConfigOld:
                laneNumCarsLastCyclePerMinMeqNext = [0,0,0,0,0,0,0,0]
            trainingDataCarPredictBunt=[0,0,0,0]

        if traci.trafficlight.getPhase("gneJ5") == 1:
            if traci.trafficlight.getPhase("gneJ5") != lightConfigOld:
                laneNumCarsLastCyclePerMinMeq = laneNumCarsLastCyclePerMinMeqNext
        if traci.trafficlight.getPhase("gneJ5") == 3:
            if traci.trafficlight.getPhase("gneJ5") != lightConfigOld:
                laneNumCarsLastCyclePerMinBunt = laneNumCarsLastCyclePerMinBuntNext

        i = 0
        while i < 8:
            if firstCarMeq[i] == 1:
                timeSinceFirstCarMeq[i]+=1
            if secondCarMeq[i] == 1:
                timeSinceSecondCarMeq[i]+=1
            i+=1
        i = 0
        while i < 4:
            if firstCarBunt[i] == 1:
                timeSinceFirstCarBunt[i]+=1
            if secondCarBunt[i] == 1:
                timeSinceSecondCarBunt[i]+=1
            i+=1

        i = 8
        while i < 16:
            if traci.inductionloop.getLastStepVehicleNumber(str(i))>0 and firstCarMeq[i-8]==1 and secondCarMeq[i-8] == 0:
                secondCarMeq[i-8] = 1
                if traci.trafficlight.getPhase("gneJ5") == 0:
                    trainingDataCarPredictMeq[i-8]+=1
            i+=1
        i = 20
        while i < 24:
            if traci.inductionloop.getLastStepVehicleNumber(str(i))>0 and firstCarBunt[i-20]==1 and secondCarBunt[i-20] == 0:
                secondCarBunt[i-20] = 1
                if traci.trafficlight.getPhase("gneJ5") == 2:
                    trainingDataCarPredictBunt[i-20]+=1
            i+=1

        i = 0
        while i < 8:
            if traci.inductionloop.getLastStepVehicleNumber(str(i))>0 and firstCarMeq[i] == 0:
                firstCarMeq[i] = 1
                if traci.trafficlight.getPhase("gneJ5") == 0:
                    trainingDataCarPredictMeq[i]+=1
            i+=1
        i = 16
        while i < 20:
            if traci.inductionloop.getLastStepVehicleNumber(str(i))>0 and firstCarBunt[i-16] == 0:
                firstCarBunt[i-16] = 1
                if traci.trafficlight.getPhase("gneJ5") == 2:
                    trainingDataCarPredictBunt[i-16]+=1
            i+=1




        #TIME SINCE LAST LIGHT CHANGE
        if traci.trafficlight.getPhase("gneJ5") != lightConfigOld:
            if traci.trafficlight.getPhase("gneJ5") == 0:
                firstCarMeq = [0,0,0,0,0,0,0,0]
                secondCarMeq = [0,0,0,0,0,0,0,0]
                timeSinceFirstCarMeq = [0,0,0,0,0,0,0,0]
                timeSinceSecondCarMeq = [0,0,0,0,0,0,0,0]
            if traci.trafficlight.getPhase("gneJ5") == 2:
                firstCarBunt = [0,0,0,0]
                secondCarBunt = [0,0,0,0]
                timeSinceFirstCarBunt = [0,0,0,0]
                timeSinceSecondCarBunt = [0,0,0,0]
            if traci.trafficlight.getPhase("gneJ5") == 1 or traci.trafficlight.getPhase("gneJ5") == 3:
                outputCarPredictBuntOld = torch.zeros(4)
                outputCarPredictMeqOld = torch.zeros(8)
                firstCarMeq = [0,0,0,0,0,0,0,0]
                secondCarMeq = [0,0,0,0,0,0,0,0]
                firstCarBunt = [0,0,0,0]
                secondCarBunt = [0,0,0,0]
                timeSinceFirstCarMeq = [0,0,0,0,0,0,0,0]
                timeSinceSecondCarMeq = [0,0,0,0,0,0,0,0]
                timeSinceFirstCarBunt = [0,0,0,0]
                timeSinceSecondCarBunt = [0,0,0,0]
            trainingDataCarPredictBunt=[0,0,0,0]
            trainingDataCarPredictMeq=[0,0,0,0,0,0,0,0]
            timeSinceLastLightChange = 0
            if traci.trafficlight.getPhase("gneJ5") == 1 or traci.trafficlight.getPhase("gneJ5") == 3:
                timeStartStop = 1
        lightConfigOld = traci.trafficlight.getPhase("gneJ5")

        if traci.trafficlight.getPhase("gneJ5") == 1:
            timeSinceFirstCarMeq = [0,0,0,0,0,0,0,0]
            timeSinceSecondCarMeq = [0,0,0,0,0,0,0,0]
            timeSinceFirstCarBunt = [0,0,0,0]
            timeSinceSecondCarBunt = [0,0,0,0]
        if traci.trafficlight.getPhase("gneJ5") == 3:
            timeSinceFirstCarMeq = [0,0,0,0,0,0,0,0]
            timeSinceSecondCarMeq = [0,0,0,0,0,0,0,0]
            timeSinceFirstCarBunt = [0,0,0,0]
            timeSinceSecondCarBunt = [0,0,0,0]
        #calculate time of day (split up by 10 min and rounded down)
        #data was collected from 5 to 6 pm, so the time would be 108-113
        #once again, normalized between 0 to 1 to assist with training, so result is divided by 144
        min = timeStep//600*10
        tenMinTimeStep = 108 #should be set to 0 for actual full day, but simulation starts at 5 pm, so that is 108 10 minute segments into the day
        while min>=10:
            min-=10
            tenMinTimeStep+=1
        tenMinTimeStep/=144
        #get day of week (0=Thursday, 1=Wednesday)
        inputDay = (simNum%7)/7

        input_dataMeq = []
        input_dataMeq.append(inputDay)
        input_dataMeq.append(tenMinTimeStep)
        input_dataMeq.append(timeSinceLastLightChange)
        input_dataMeq+=laneNumCarsLastCyclePerMinMeq
        input_dataMeq+=firstCarMeq
        input_dataMeq+=secondCarMeq
        input_dataMeq+=timeSinceFirstCarMeq
        input_dataMeq+=timeSinceSecondCarMeq

        input_dataBunt = []
        input_dataBunt.append(inputDay)
        input_dataBunt.append(tenMinTimeStep)
        input_dataBunt.append(timeSinceLastLightChange)
        input_dataBunt+=laneNumCarsLastCyclePerMinBunt
        input_dataBunt+=firstCarBunt
        input_dataBunt+=secondCarBunt
        input_dataBunt+=timeSinceFirstCarBunt
        input_dataBunt+=timeSinceSecondCarBunt

        #CAR PREDICT
        if traci.trafficlight.getPhase("gneJ5") == 0:
            input_dataTensorMeq = torch.Tensor(input_dataMeq)
            target_dataCarPredictMeq = torch.Tensor(trainingDataCarPredictMeq)
            outputCarPredictMeq, hiddenCarPredictMeq = modelCarPredictMeq(input_dataTensorMeq.unsqueeze(0).unsqueeze(0), hiddenCarPredictMeq)

            lossCarPredictMeq += criterionCarPredictMeq(outputCarPredictMeq.squeeze().unsqueeze(0).unsqueeze(0), target_dataCarPredictMeq.unsqueeze(0).unsqueeze(0))
            lossesCarPredictMeq.append(lossCarPredictMeq.data.item())
            lossHolderMeq+=lossCarPredictMeq
            lossCarPredictMeq.backward()#retain_graph=True
            optimizerCarPredictMeq.step()
            '''
            if timeStep%100==0:
                print(timeStep)
                print("Time Change: " + str(time.time()-start_time))
                start_time = time.time()
                print("Time Since Last Change: " + str(timeSinceLastLightChange))
                print("target data Meq: ")
                print(target_dataCarPredictMeq)
                print("Output Data Meq: ")
                print(outputCarPredictMeq)
                print("Loss Meq: {:0.6f}".format(lossCarPredictMeq.data.item()))
                print("Loss Total Meq: " + str(lossHolderMeq/timeSinceLastLightChange))
                lossHolderMeq=0
                print("")
                print("")
            '''

        if traci.trafficlight.getPhase("gneJ5") == 2:
            input_dataTensorBunt = torch.Tensor(input_dataBunt)
            target_dataCarPredictBunt = torch.Tensor(trainingDataCarPredictBunt)
            outputCarPredictBunt, hiddenCarPredictBunt = modelCarPredictBunt(input_dataTensorBunt.unsqueeze(0).unsqueeze(0), hiddenCarPredictBunt)

            lossCarPredictBunt += criterionCarPredictBunt(outputCarPredictBunt.squeeze().unsqueeze(0).unsqueeze(0), target_dataCarPredictBunt.unsqueeze(0).unsqueeze(0))
            lossesCarPredictBunt.append(lossCarPredictBunt.data.item())
            lossHolderBunt+=lossCarPredictBunt
            lossCarPredictBunt.backward()#retain_graph=True
            optimizerCarPredictBunt.step()
            '''
            if timeStep%100==0:
                print(timeStep)
                print("Time Change: " + str(time.time()-start_time))
                start_time = time.time()
                print("Time Since Last Change: " + str(timeSinceLastLightChange))
                print("target data Bunt: ")
                print(target_dataCarPredictBunt)
                print("Output Data Bunt: ")
                print(outputCarPredictBunt)
                print("Loss Bunt: {:0.6f}".format(lossCarPredictBunt.data.item()))
                print("Loss Total Bunt: " + str(lossHolderBunt/timeSinceLastLightChange))
                lossHolderBunt=0
                print("")
                print("")


        #JUST MAKES TESTING EASIER
        if traci.trafficlight.getPhase("gneJ5") == 1 or traci.trafficlight.getPhase("gneJ5") == 3:
            if timeStep%100==0:
                print("missed")
                print("")
                print("")
        '''



        #HANDLES CAR ENTERANCES MEQUON GREEN (BUNTROCK RED)
        if traci.trafficlight.getPhase("gneJ5") == 0 or traci.trafficlight.getPhase("gneJ5") == 3:
            input_dataTensorBunt = torch.Tensor(input_dataBunt)
            target_dataCarPredictBunt = torch.Tensor(trainingDataCarPredictBunt)
            outputCarPredictBunt, hiddenCarPredictBunt = modelCarPredictBunt(input_dataTensorBunt.unsqueeze(0).unsqueeze(0), hiddenCarPredictBunt)

            i = 0
            while i < 4:
                if firstCarBunt[i] == 1 and outputCarPredictBunt[0][0][i]<1:
                    outputCarPredictBunt[0][0][i] = 1
                if secondCarBunt[i] == 1 and outputCarPredictBunt[0][0][i]<2:
                    outputCarPredictBunt[0][0][i] = 2
                if firstCarBunt[i] == 1 and secondCarBunt[i] == 0 and outputCarPredictBunt[0][0][i]>1:
                    outputCarPredictBunt[0][0][i] = 1
                if firstCarBunt[i] == 0 and not outputCarPredictBunt[0][0][i] == 0:
                    outputCarPredictBunt[0][0][i] = 0
                i+=1

            outputCarPredictBunt = outputCarPredictBunt.round()
            changeOutputCarPredictBunt = outputCarPredictBunt-outputCarPredictBuntOld
            i=0
            while i < 4:
                x = changeOutputCarPredictBunt[0][0][i]
                if x > 0:
                    d = -36.666/timeStartStop
                    xstart = d/2*(timeStartStop)**2+36.666*timeStartStop
                    if xstart > 85:
                        xstart = 85
                        temptime = timeStartStop-4.636 #time to stop in 85 meters
                        carsData.append([i+8,temptime,xstart])
                    else:
                        carsData.append([i+8,0,xstart])
                    x-=1
                i+=1
            outputCarPredictBuntOld = outputCarPredictBunt



        #Handles Car Enterances (BUNTROCK GREEN MEQUON RED)
        if traci.trafficlight.getPhase("gneJ5") == 1 or traci.trafficlight.getPhase("gneJ5") == 2:
            input_dataTensorMeq = torch.Tensor(input_dataMeq)
            target_dataCarPredictMeq = torch.Tensor(trainingDataCarPredictMeq)
            outputCarPredictMeq, hiddenCarPredictMeq = modelCarPredictMeq(input_dataTensorMeq.unsqueeze(0).unsqueeze(0), hiddenCarPredictMeq)

            i = 0
            while i < 8:
                if firstCarMeq[i] == 1 and outputCarPredictMeq[0][0][i]<1:
                    outputCarPredictMeq[0][0][i] = 1
                if secondCarMeq[i] == 1 and outputCarPredictMeq[0][0][i]<2:
                    outputCarPredictMeq[0][0][i] = 2
                if firstCarMeq[i] == 1 and secondCarMeq[i] == 0 and outputCarPredictMeq[0][0][i]>1:
                    outputCarPredictMeq[0][0][i] = 1
                if firstCarMeq[i] == 0 and not outputCarPredictMeq[0][0][i]==0:
                    outputCarPredictMeq[0][0][i] = 0
                i+=1
            outputCarPredictMeq = outputCarPredictMeq.round()
            changeOutputCarPredictMeq = outputCarPredictMeq-outputCarPredictMeqOld

            i=0
            while i < 8:
                x = changeOutputCarPredictMeq[0][0][i]
                if x > 0:
                    d = -58.666/timeStartStop
                    xstart = d/2*(timeStartStop)**2+58.666*timeStartStop
                    if xstart > 164:
                        xstart = 164
                        temptime = timeStartStop - 5.591 #time to stop in 164 meters
                        carsData.append([i,temptime,xstart])
                    else:
                        carsData.append([i,0,xstart])
                    x-=1
                i+=1
            outputCarPredictMeqOld = outputCarPredictMeq


        #Updates Time Losses Switch
        j = 0
        while j<len(trainingDataTrafficSwitch):
            i = 0
            tempTimeLoss = 0
            while i < len(carsData):
                tempCar = carsData[i]
                if trainingTrafficTimeAssociatedSwitch[j]<=tempCar[1]:
                    if tempCar[0] == 0 or tempCar[0] == 4 or tempCar[0] == 3 or tempCar[0] == 7 or tempCar[0] == 9 or tempCar[0] == 11:
                        accel = 3.805774 #feet per second for turning
                    if tempCar[0] == 1 or tempCar[0] == 2 or tempCar[0] == 5 or tempCar[0] == 6:
                        accel = 4.10105 #feet per second for straight
                    if tempCar[0] == 8 or tempCar[0] == 10:
                        accel = 3.9534121 #average for lane where they can turn or go straight
                    if tempCar[0] < 8:
                        speedlim = 58.666
                    else:
                        speedlim = 36.666
                    xexpected = speedlim*(timeStartStop - tempCar[1]) - tempCar[2]
                    if xexpected < (speedlim**2/(2*accel)):
                        timeLossCar = (2*xexpected/accel)**(.5)
                    else:
                        timeLossCar = (xexpected-(speedlim**2/(2*accel)))/speedlim + speedlim/accel
                    tempTimeLoss += timeLossCar
                i+=1
            if len(carsData) != 0:
                tempTimeLoss/=len(carsData)
            if (timeStep-trainingTrafficTimeAssociatedSwitch[j]+1) != 0:
                tempTimeLoss/=(timeStep-trainingTrafficTimeAssociatedSwitch[j]+1)
            trainingDataTrafficSwitch[j] = tempTimeLoss
            j+=1
        #Updates Time Losses Stay
        j = 0
        while j<len(trainingDataTrafficStay):
            i = 0
            tempTimeLoss = 0
            while i < len(carsData):
                tempCar = carsData[i]
                if trainingTrafficTimeAssociatedStay[j]<=tempCar[1]:
                    if tempCar[0] == 0 or tempCar[0] == 4 or tempCar[0] == 3 or tempCar[0] == 7 or tempCar[0] == 9 or tempCar[0] == 11:
                        accel = 3.805774 #feet per second for turning
                    if tempCar[0] == 1 or tempCar[0] == 2 or tempCar[0] == 5 or tempCar[0] == 6:
                        accel = 4.10105 #feet per second for straight
                    if tempCar[0] == 8 or tempCar[0] == 10:
                        accel = 3.9534121 #average for lane where they can turn or go straight
                    if tempCar[0] < 8:
                        speedlim = 58.666
                    else:
                        speedlim = 36.666
                    xexpected = speedlim*(timeStartStop - tempCar[1]) - tempCar[2]
                    if xexpected < (speedlim**2/(2*accel)):
                        timeLossCar = (2*xexpected/accel)**(.5)
                    else:
                        timeLossCar = (xexpected-(speedlim**2/(2*accel)))/speedlim + speedlim/accel
                    tempTimeLoss += timeLossCar
                i+=1
            if len(carsData) != 0:
                tempTimeLoss/=len(carsData)
            if (timeStep-trainingTrafficTimeAssociatedStay[j]+1) != 0:
                tempTimeLoss/=(timeStep-trainingTrafficTimeAssociatedStay[j]+1)
            trainingDataTrafficStay[j] = tempTimeLoss
            j+=1


        if (timeSinceLastLightChange+1)%60 == 0:
            #Train the network with whatever it has
            i = 0
            while i < len(trainingDataTrafficSwitch):
                outputTrafficSwitch, hiddenTrafficSwitchTemp = modelTrafficStay(storedInputsSwitch[i].unsqueeze(0).unsqueeze(0), hiddenStatesTrafficSwitch[i])

                target_dataTrafficSwitch = (torch.Tensor([trainingDataTrafficSwitch[i]]))
                lossTrafficSwitch = criterionTrafficStay(outputTrafficSwitch.squeeze().unsqueeze(0).unsqueeze(0), target_dataTrafficSwitch.unsqueeze(0))
                lossesTrafficSwitch.append(lossTrafficSwitch.data.item())
                lossHolderTrafficSwitch+=lossTrafficSwitch
                lossTrafficSwitch.backward()#retain_graph=True
                optimizerTrafficSwitch.step()

                print(timeStep)
                print("Time Change: " + str(time.time()-start_time))
                start_time = time.time()
                print("Time Since Last Change: " + str(timeSinceLastLightChange))
                print("target data Switch: ")
                print(target_dataTrafficSwitch)
                print("Output Data Stay: ")
                print(outputTrafficSwitch)
                print("Input Data")
                print(storedInputsSwitch[i])
                print("Loss Stay: {:0.6f}".format(lossTrafficSwitch.data.item()))
                print("")
                print("")
                i+=1
            storedInputsSwitch = []
            hiddenStatesTrafficSwitch = []
            trainingDataTrafficSwitch = []
            trainingTrafficTimeAssociatedSwitch = []

            i=0
            while i<len(trainingDataTrafficStay):
                outputTrafficStay, hiddenTrafficStayTemp = modelTrafficStay(storedInputsStay[i].unsqueeze(0).unsqueeze(0), hiddenStatesTrafficStay[i])

                target_dataTrafficStay = torch.Tensor([trainingDataTrafficStay[i]])
                lossTrafficStay = criterionTrafficStay(outputTrafficStay.squeeze().unsqueeze(0).unsqueeze(0), target_dataTrafficStay.unsqueeze(0))
                lossesTrafficStay.append(lossTrafficStay.data.item())
                lossHolderTrafficStay+=lossTrafficStay
                lossTrafficStay.backward()#retain_graph=True
                optimizerTrafficStay.step()

                print(timeStep)
                print("Time Change: " + str(time.time()-start_time))
                start_time = time.time()
                print("Time Since Last Change: " + str(timeSinceLastLightChange))
                print("target data Stay: ")
                print(target_dataTrafficStay)
                print("Output Data Stay: ")
                print(outputTrafficStay)
                print("Input Data")
                print(storedInputsStay[i])
                print("Loss Stay: {:0.6f}".format(lossTrafficStay.data.item()))
                print("")
                print("")
                i+=1
            storedInputsStay = []
            hiddenStatesTrafficStay = []
            trainingDataTrafficStay = []
            trainingTrafficTimeAssociatedStay = []


        #Mequon Green Direction
        if traci.trafficlight.getPhase("gneJ5") == 0:
            input_dataTraffic = []
            input_dataTraffic.append(inputDay)
            input_dataTraffic.append(tenMinTimeStep)
            input_dataTraffic.append(timeSinceLastLightChange)
            input_dataTraffic.append(0)
            input_dataTraffic+=laneNumCarsLastCyclePerMinMeqNext
            input_dataTraffic+=inductionLoopTimesBunt
            input_dataTraffic+=inductionLoopTimesMeq
            input_dataTraffic+=timeSinceFirstCarBunt+[0,0,0,0]
            input_dataTraffic+=timeSinceSecondCarBunt+[0,0,0,0]
            input_dataTraffic+=[0,0,0,0]

            input_dataTensorTraffic = torch.cat((torch.Tensor(input_dataTraffic), outputCarPredictBunt.squeeze()), 0)

            outputTrafficSwitch, hiddenTrafficSwitchTemp = modelTrafficSwitch(input_dataTensorTraffic.unsqueeze(0).unsqueeze(0), hiddenStatesTrafficSwitchLast)
            hiddenStatesTrafficSwitchLast = hiddenTrafficSwitchTemp
            outputTrafficStay, hiddenTrafficStayTemp = modelTrafficStay(input_dataTensorTraffic.unsqueeze(0).unsqueeze(0), hiddenStatesTrafficStayLast)
            hiddenStatesTrafficStayLast = hiddenTrafficStayTemp

            #Handles switch or stay logic
            if outputTrafficSwitch < outputTrafficStay and timeSinceLastLightChange>=1:
                #Train the network with whatever it has
                i = 0
                while i < len(trainingDataTrafficSwitch):
                    outputTrafficSwitch, hiddenTrafficSwitchTemp = modelTrafficStay(storedInputsSwitch[i].unsqueeze(0).unsqueeze(0), hiddenStatesTrafficSwitch[i])

                    target_dataTrafficSwitch = (torch.Tensor([trainingDataTrafficSwitch[i]]))
                    lossTrafficSwitch = criterionTrafficStay(outputTrafficSwitch.squeeze().unsqueeze(0).unsqueeze(0), target_dataTrafficSwitch.unsqueeze(0))
                    lossesTrafficSwitch.append(lossTrafficSwitch.data.item())
                    lossHolderTrafficSwitch+=lossTrafficSwitch
                    lossTrafficSwitch.backward()#retain_graph=True
                    optimizerTrafficSwitch.step()

                    print(timeStep)
                    print("Time Change: " + str(time.time()-start_time))
                    start_time = time.time()
                    print("Time Since Last Change: " + str(timeSinceLastLightChange))
                    print("target data Switch: ")
                    print(target_dataTrafficSwitch)
                    print("Output Data Stay: ")
                    print(outputTrafficSwitch)
                    print("Input Data")
                    print(storedInputsSwitch[i])
                    print("Loss Stay: {:0.6f}".format(lossTrafficSwitch.data.item()))
                    print("")
                    print("")
                    i+=1
                storedInputsSwitch = []
                hiddenStatesTrafficSwitch = []
                trainingDataTrafficSwitch = []
                trainingTrafficTimeAssociatedSwitch = []

                i=0
                while i<len(trainingDataTrafficStay):
                    outputTrafficStay, hiddenTrafficStayTemp = modelTrafficStay(storedInputsStay[i].unsqueeze(0).unsqueeze(0), hiddenStatesTrafficStay[i])

                    target_dataTrafficStay = torch.Tensor([trainingDataTrafficStay[i]])
                    lossTrafficStay = criterionTrafficStay(outputTrafficStay.squeeze().unsqueeze(0).unsqueeze(0), target_dataTrafficStay.unsqueeze(0))
                    lossesTrafficStay.append(lossTrafficStay.data.item())
                    lossHolderTrafficStay+=lossTrafficStay
                    lossTrafficStay.backward()#retain_graph=True
                    optimizerTrafficStay.step()

                    print(timeStep)
                    print("Time Change: " + str(time.time()-start_time))
                    start_time = time.time()
                    print("Time Since Last Change: " + str(timeSinceLastLightChange))
                    print("target data Stay: ")
                    print(target_dataTrafficStay)
                    print("Output Data Stay: ")
                    print(outputTrafficStay)
                    print("Input Data")
                    print(storedInputsStay[i])
                    print("Loss Stay: {:0.6f}".format(lossTrafficStay.data.item()))
                    print("")
                    print("")
                    i+=1
                storedInputsStay = []
                hiddenStatesTrafficStay = []
                trainingDataTrafficStay = []
                trainingTrafficTimeAssociatedStay = []

                storedInputsSwitch.append(input_dataTensorTraffic)
                hiddenStatesTrafficSwitch.append(hiddenStatesTrafficSwitchLast)
                trainingDataTrafficSwitch.append(0)
                trainingTrafficTimeAssociatedSwitch.append(0)
                traci.trafficlight.setPhase("gneJ5", 1)
                carsData = []
            else:
                storedInputsStay.append(input_dataTensorTraffic)
                hiddenStatesTrafficStay.append(hiddenStatesTrafficStayLast)
                trainingDataTrafficStay.append(0)
                trainingTrafficTimeAssociatedStay.append(timeSinceLastLightChange+5)
                traci.trafficlight.setPhase("gneJ5", 0)
        #Buntrock Green Direction
        if traci.trafficlight.getPhase("gneJ5") == 2:
            input_dataTraffic = []
            input_dataTraffic.append(inputDay)
            input_dataTraffic.append(tenMinTimeStep)
            input_dataTraffic.append(timeSinceLastLightChange)
            input_dataTraffic.append(2)
            input_dataTraffic+=laneNumCarsLastCyclePerMinBuntNext+[0,0,0,0]
            input_dataTraffic+=inductionLoopTimesBunt
            input_dataTraffic+=inductionLoopTimesMeq
            input_dataTraffic+=timeSinceFirstCarMeq
            input_dataTraffic+=timeSinceSecondCarMeq

            input_dataTensorTraffic = torch.cat((torch.Tensor(input_dataTraffic), outputCarPredictMeq.squeeze()), 0)


            outputTrafficSwitch, hiddenTrafficSwitchTemp = modelTrafficSwitch(input_dataTensorTraffic.unsqueeze(0).unsqueeze(0), hiddenStatesTrafficSwitchLast)
            hiddenStatesTrafficSwitchLast = hiddenTrafficSwitchTemp
            outputTrafficStay, hiddenTrafficStayTemp = modelTrafficStay(input_dataTensorTraffic.unsqueeze(0).unsqueeze(0), hiddenStatesTrafficStayLast)
            hiddenStatesTrafficStayLast = hiddenTrafficStayTemp

            #Handles switch or stay logic
            if outputTrafficSwitch < outputTrafficStay and timeSinceLastLightChange>=1:
                #Train the network with whatever it has
                i = 0
                while i < len(trainingDataTrafficSwitch):
                    outputTrafficSwitch, hiddenTrafficSwitchTemp = modelTrafficStay(storedInputsSwitch[i].unsqueeze(0).unsqueeze(0), hiddenStatesTrafficSwitch[i])

                    target_dataTrafficSwitch = torch.Tensor([trainingDataTrafficSwitch[i]])
                    lossTrafficSwitch = criterionTrafficStay(outputTrafficSwitch.squeeze().unsqueeze(0).unsqueeze(0), target_dataTrafficSwitch.unsqueeze(0))
                    lossesTrafficSwitch.append(lossTrafficSwitch.data.item())
                    lossHolderTrafficSwitch+=lossTrafficSwitch
                    lossTrafficSwitch.backward()#retain_graph=True
                    optimizerTrafficSwitch.step()

                    print(timeStep)
                    print("Time Change: " + str(time.time()-start_time))
                    start_time = time.time()
                    print("Time Since Last Change: " + str(timeSinceLastLightChange))
                    print("target data Switch: ")
                    print(target_dataTrafficSwitch)
                    print("Output Data Stay: ")
                    print(outputTrafficSwitch)
                    print("Input Data")
                    print(storedInputsSwitch[i])
                    print("Loss Stay: {:0.6f}".format(lossTrafficSwitch.data.item()))
                    print("")
                    print("")
                    i+=1
                storedInputsSwitch = []
                hiddenStatesTrafficSwitch = []
                trainingDataTrafficSwitch = []
                trainingTrafficTimeAssociatedSwitch = []

                i=0
                while i<len(trainingDataTrafficStay):
                    outputTrafficStay, hiddenTrafficStayTemp = modelTrafficStay(storedInputsStay[i].unsqueeze(0).unsqueeze(0), hiddenStatesTrafficStay[i])

                    target_dataTrafficStay = torch.Tensor([trainingDataTrafficStay[i]])
                    lossTrafficStay = criterionTrafficStay(outputTrafficStay.squeeze().unsqueeze(0).unsqueeze(0), target_dataTrafficStay.unsqueeze(0))
                    lossesTrafficStay.append(lossTrafficStay.data.item())
                    lossHolderTrafficStay+=lossTrafficStay
                    lossTrafficStay.backward()#retain_graph=True
                    optimizerTrafficStay.step()

                    print(timeStep)
                    print("Time Change: " + str(time.time()-start_time))
                    start_time = time.time()
                    print("Time Since Last Change: " + str(timeSinceLastLightChange))
                    print("target data Stay: ")
                    print(target_dataTrafficStay)
                    print("Output Data Stay: ")
                    print(outputTrafficStay)
                    print("Input Data")
                    print(storedInputsStay[i])
                    print("Loss Stay: {:0.6f}".format(lossTrafficStay.data.item()))
                    print("")
                    print("")
                    i+=1
                storedInputsStay = []
                hiddenStatesTrafficStay = []
                trainingDataTrafficStay = []
                trainingTrafficTimeAssociatedStay = []

                storedInputsSwitch.append(input_dataTensorTraffic)
                hiddenStatesTrafficSwitch.append(hiddenStatesTrafficSwitchLast)
                trainingDataTrafficSwitch.append(0)
                trainingTrafficTimeAssociatedSwitch.append(0)
                traci.trafficlight.setPhase("gneJ5", 3)
                carsData = []
            else:
                storedInputsStay.append(input_dataTensorTraffic)
                hiddenStatesTrafficStay.append(hiddenStatesTrafficStayLast)
                trainingDataTrafficStay.append(0)
                trainingTrafficTimeAssociatedStay.append(timeSinceLastLightChange+5)
                traci.trafficlight.setPhase("gneJ5", 2)


        if timeStep % 60 == 0:
            print("Switch:")
            print(outputTrafficSwitch)
            print("Stay:")
            print(outputTrafficStay)
            print("car predict meq")
            print(outputCarPredictMeq)
            print("car predict bunt")
            print(outputCarPredictBunt)
            print('')
            print('')

        #print(trainingDataTrafficStay)
        #print(trainingDataTrafficSwitch)
        #print('')
        #print('')
        #print(carsData)
        #print('')
        #print(trainingDataTrafficSwitch)
        #print(usedTrafficSwitch)
        #print('')
        #print(trainingDataTrafficStay)
        #print(usedTrafficStay)
        #print(trainingDataTrafficStay[0])
        #print('')
        #print(trainingDataTrafficStay[1])
        #print('')
        #print('')
        #print('')
        timeStep += 1

    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def cudaInit():
    #Set device
    USE_CUDA = torch.cuda.is_available()
    if USE_CUDA:
        device = torch.device("cuda")
        cuda = True
    else:
        device = torch.device("cpu")
        cuda = False

    print("Device =", device)
    gpus = [0]

#Define model
class Model(nn.Module):

    #Define model parameters
    def __init__(self, input_size, hidden_size, num_layers, dropout, output_size):
        super(Model, self).__init__()

        #Model parameters
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout

        #Model layers
        self.lstm = nn.LSTM(input_size = input_size, hidden_size = hidden_size, num_layers = num_layers, dropout = dropout)
        self.linear = nn.Linear(hidden_size, output_size)

    #Define initial hidden and cell states
    def init_states(self, num_layers, hidden_size):
        hidden = [Variable(torch.zeros(num_layers, 1, hidden_size)),
                  Variable(torch.zeros(num_layers, 1, hidden_size))]

        #Initialize forget gate bias to 1
        for names in self.lstm._all_weights:
            for name in filter(lambda n: "bias" in n, names):
                bias = getattr(self.lstm, name)
                n = bias.size(0)
                start, end = n//4, n//2

                nn.init.constant_(bias.data[start:end], 1.0)

        return hidden

    #Define forward propagation
    def forward(self, inp, hidden):
        #LSTM
        output, hidden = self.lstm(inp, (hidden[0].detach(), hidden[1].detach()))

        #Linear Layer
        output = self.linear(output)

        return output, hidden

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    sig = nn.Sigmoid()

    #connect neural network
    #Initialize model parameters
    input_sizeCarPredictMeq = 43
    hidden_sizeCarPredictMeq = 1024
    num_layersCarPredictMeq = 3
    dropoutCarPredictMeq = .2
    learning_rateCarPredictMeq = 0.000002
    output_sizeCarPredictMeq = 8

    input_sizeCarPredictBunt = 23
    hidden_sizeCarPredictBunt = 1024
    num_layersCarPredictBunt = 3
    dropoutCarPredictBunt = .2
    learning_rateCarPredictBunt = 0.000002
    output_sizeCarPredictBunt = 4

    input_sizeTrafficSwitch = 60
    hidden_sizeTrafficSwitch = 1024
    num_layersTrafficSwitch = 4
    dropoutTrafficSwitch = .2
    learning_rateTrafficSwitch = 0.000001
    output_sizeTrafficSwitch = 1

    input_sizeTrafficStay = 60
    hidden_sizeTrafficStay = 1024
    num_layersTrafficStay = 4
    dropoutTrafficStay = .2
    learning_rateTrafficStay = 0.000001
    output_sizeTrafficStay = 1

    #List of losses
    lossesCarPredictMeq = []
    lossesCarPredictBunt = []
    lossesTrafficSwitch = []
    lossesTrafficStay = []

    #Call model, set optimizer and loss function
    modelCarPredictMeq = Model(input_sizeCarPredictMeq, hidden_sizeCarPredictMeq, num_layersCarPredictMeq, dropoutCarPredictMeq, output_sizeCarPredictMeq)
    modelCarPredictMeq.load_state_dict(torch.load("networkCarPredictMeq_8_0_13.pth"))
    modelCarPredictBunt = Model(input_sizeCarPredictBunt, hidden_sizeCarPredictBunt, num_layersCarPredictBunt, dropoutCarPredictBunt, output_sizeCarPredictBunt)
    modelCarPredictBunt.load_state_dict(torch.load("networkCarPredictBunt_8_0_13.pth"))

    optimizerCarPredictMeq = torch.optim.Adam(modelCarPredictMeq.parameters(), lr = learning_rateCarPredictMeq)
    criterionCarPredictMeq = nn.MSELoss()
    optimizerCarPredictBunt = torch.optim.Adam(modelCarPredictBunt.parameters(), lr = learning_rateCarPredictBunt)
    criterionCarPredictBunt = nn.MSELoss()

    #Run on GPU if available
    if cuda:
        modelCarPredictMeq.cuda()
        criterionCarPredictMeq.cuda()
        modelCarPredictBunt.cuda()
        criterionCarPredictBunt.cuda()

    #Total number of parameters
    total_params = sum(p.numel() for p in modelCarPredictMeq.parameters())
    print("Total number of parameters in network CarPredictMeq: " + str(total_params))
    total_params = sum(p.numel() for p in modelCarPredictBunt.parameters())
    print("Total number of parameters in network CarPredictBunt: " + str(total_params))

    #Call model, set optimizer and loss function
    modelTrafficSwitch = Model(input_sizeTrafficSwitch, hidden_sizeTrafficSwitch, num_layersTrafficSwitch, dropoutTrafficSwitch, output_sizeTrafficSwitch)
    modelTrafficSwitch.load_state_dict(torch.load("networkTrafficSwitch_8_0_13.pth"))
    optimizerTrafficSwitch = torch.optim.Adam(modelTrafficSwitch.parameters(), lr = learning_rateTrafficSwitch)
    criterionTrafficSwitch = nn.MSELoss()
    #Call model, set optimizer and loss function
    modelTrafficStay = Model(input_sizeTrafficStay, hidden_sizeTrafficStay, num_layersTrafficStay, dropoutTrafficStay, output_sizeTrafficStay)
    modelTrafficStay.load_state_dict(torch.load("networkTrafficStay_8_0_13.pth"))
    optimizerTrafficStay = torch.optim.Adam(modelTrafficStay.parameters(), lr = learning_rateTrafficStay)
    criterionTrafficStay = nn.MSELoss()

    #Run on GPU if available
    if cuda:
        modelTrafficSwitch.cuda()
        criterionTrafficSwitch.cuda()
        modelTrafficStay.cuda()
        criterionTrafficStay.cuda()

    #Total number of parameters
    total_params = sum(p.numel() for p in modelTrafficSwitch.parameters())
    print("Total number of parameters in network TrafficSwitch: " + str(total_params))
    #Total number of parameters
    total_params = sum(p.numel() for p in modelTrafficStay.parameters())
    print("Total number of parameters in network TrafficStay: " + str(total_params))

    hiddenCarPredictMeq = modelCarPredictMeq.init_states(num_layersCarPredictMeq, hidden_sizeCarPredictMeq)
    hiddenCarPredictBunt = modelCarPredictBunt.init_states(num_layersCarPredictBunt, hidden_sizeCarPredictBunt)

    #Run on GPU if available
    if cuda:
        hiddenCarPredictMeq = (hiddenCarPredictMeq[0].cuda(), hiddenCarPredictMeq[1].cuda())
        hiddenCarPredictBunt = (hiddenCarPredictBunt[0].cuda(), hiddenCarPredictBunt[1].cuda())
    #Set initial gradients
    modelCarPredictMeq.zero_grad()
    modelCarPredictBunt.zero_grad()
    #Set initial loss
    lossCarPredictMeq = 0
    lossCarPredictBunt = 0

    hiddenTrafficSwitch = modelTrafficSwitch.init_states(num_layersTrafficSwitch, hidden_sizeTrafficSwitch)
    #Run on GPU if available
    if cuda:
        hiddenTrafficSwitch = (hiddenTrafficSwitch[0].cuda(), hiddenTrafficSwitch[1].cuda())
    #Set initial gradients
    modelTrafficSwitch.zero_grad()
    #Set initial loss
    lossTrafficSwitch = 0
    hiddenTrafficStay = modelTrafficStay.init_states(num_layersTrafficStay, hidden_sizeTrafficStay)
    #Run on GPU if available
    if cuda:
        hiddenTrafficStay = (hiddenTrafficStay[0].cuda(), hiddenTrafficStay[1].cuda())
    #Set initial gradients
    modelTrafficStay.zero_grad()
    #Set initial loss
    lossTrafficStay = 0

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    #generate_routefile()

    #big sim num for file storage, epoch for cycles through data set, simulaition day number
    #runNum 1 - pre removing induction loop times for car CarPredict
    runNum = 8
    epochNum = 1
    simNum = 1
    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    while(epochNum<10):
        print(files[simNum-1])
        print(str(epochNum)+"____"+str(simNum))
        traci.start([sumoBinary, "-c", files[simNum-1],
                                "--tripinfo-output", "tripinfo"+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+".xml"])
        optimizerCarPredictMeq.zero_grad()
        modelCarPredictMeq.zero_grad()
        optimizerCarPredictBunt.zero_grad()
        modelCarPredictBunt.zero_grad()
        optimizerTrafficSwitch.zero_grad()
        modelTrafficSwitch.zero_grad()
        optimizerTrafficStay.zero_grad()
        modelTrafficStay.zero_grad()
        run()
        torch.save(modelCarPredictMeq.state_dict(), "networkCarPredictMeq"+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+".pth")
        torch.save(modelCarPredictBunt.state_dict(), "networkCarPredictBunt"+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+".pth")
        torch.save(modelTrafficSwitch.state_dict(), "networkTrafficSwitch"+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+".pth")
        torch.save(modelTrafficStay.state_dict(), "networkTrafficStay"+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+".pth")
        with open('lossesCarPredictMeq'+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+'.txt', 'w') as f:
            for item in lossesCarPredictMeq:
                f.write("%s\n" % item)
        lossesCarPredictMeq = []
        with open('lossesCarPredictBunt'+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+'.txt', 'w') as f:
            for item in lossesCarPredictBunt:
                f.write("%s\n" % item)
        lossesCarPredictBunt = []
        with open('lossesTrafficSwitch'+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+'.txt', 'w') as f:
            for item in lossesTrafficSwitch:
                f.write("%s\n" % item)
        lossesTrafficSwitch = []
        with open('lossesTrafficStay'+"_"+str(runNum)+"_"+str(epochNum)+"_"+str(simNum)+'.txt', 'w') as f:
            for item in lossesTrafficStay:
                f.write("%s\n" % item)
        lossesTrafficStay = []
        simNum+=1
        if simNum == 15:
            simNum=1
            epochNum+=1
