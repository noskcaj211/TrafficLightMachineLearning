from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

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

#def generate_routefile():
#    random.seed(42)  # make tests reproducible
#    N = 3600  # number of time steps
#    # demand per second from different directions
#    pWE = 1. / 10
#    pEW = 1. / 11
#    pNS = 1. / 30
#    with open("demand.rou.xml", "w") as routes:
#        print("""<routes>
#        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
#guiShape="passenger"/>
#        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>
#
#        <route id="right" edges="51o 1i 2o 52i" />
#        <route id="left" edges="52o 2i 1o 51i" />
#        <route id="down" edges="54o 4i 3o 53i" />""", file=routes)
#        vehNr = 0
#        for i in range(N):
#            if random.uniform(0, 1) < pWE:
#                print('    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />' % (
#                    vehNr, i), file=routes)
#                vehNr += 1
#            if random.uniform(0, 1) < pEW:
#                print('    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />' % (
#                    vehNr, i), file=routes)
#                vehNr += 1
#            if random.uniform(0, 1) < pNS:
#                print('    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>' % (
#                    vehNr, i), file=routes)
#                vehNr += 1
#        print("</routes>", file=routes)

# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#     </tlLogic>

#traci.trafficlight.setRedYellowGreenState("0", "GrGr")
def run():
    """execute the TraCI control loop"""
    step = 0
    time = -10

    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("gneJ5", 0)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        #Meq Green
        #print(time)
        if traci.trafficlight.getPhase("gneJ5") == 0:
            # Start Timer
            if traci.inductionloop.getLastStepVehicleNumber("16") > 0 or traci.inductionloop.getLastStepVehicleNumber("17") > 0 or traci.inductionloop.getLastStepVehicleNumber("18") > 0 or traci.inductionloop.getLastStepVehicleNumber("19") > 0:
                if time<=-10:
                    time=90
            if traci.inductionloop.getLastStepVehicleNumber("0") or traci.inductionloop.getLastStepVehicleNumber("1") or traci.inductionloop.getLastStepVehicleNumber("2") or traci.inductionloop.getLastStepVehicleNumber("3") or traci.inductionloop.getLastStepVehicleNumber("4") or traci.inductionloop.getLastStepVehicleNumber("5") or traci.inductionloop.getLastStepVehicleNumber("6") or traci.inductionloop.getLastStepVehicleNumber("7"):
                # if there is movement in the other direction then
                time += 4
            if time <= 0 and time>=-3:
                traci.trafficlight.setPhase("gneJ5", 1)
                time = -10
            else:
                traci.trafficlight.setPhase("gneJ5", 0)
                time -= 5
        if traci.trafficlight.getPhase("gneJ5") == 2:
            # we are not already switching
            if traci.inductionloop.getLastStepVehicleNumber("0") or traci.inductionloop.getLastStepVehicleNumber("1") or traci.inductionloop.getLastStepVehicleNumber("2") or traci.inductionloop.getLastStepVehicleNumber("3") or traci.inductionloop.getLastStepVehicleNumber("4") or traci.inductionloop.getLastStepVehicleNumber("5") or traci.inductionloop.getLastStepVehicleNumber("6") or traci.inductionloop.getLastStepVehicleNumber("7"):
                if time<=-10:
                    time=90
            if traci.inductionloop.getLastStepVehicleNumber("16") > 0 or traci.inductionloop.getLastStepVehicleNumber("17") > 0 or traci.inductionloop.getLastStepVehicleNumber("18") > 0 or traci.inductionloop.getLastStepVehicleNumber("19") > 0:
                # if there is movement in the other direction then
                time += 4
            if time <= 0 and time>=-5:
                traci.trafficlight.setPhase("gneJ5", 3)
                time = -10
            else:
                traci.trafficlight.setPhase("gneJ5", 2)
                time -= 5
        step += 1
    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    #generate_routefile()
    simNum = 1
    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    while(simNum<15):
        print(files[simNum-1])
        traci.start([sumoBinary, "-c", files[simNum-1]])
        run()
        simNum+=1
