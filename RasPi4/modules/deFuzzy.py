import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


NumberOfVehicles= ctrl.Antecedent(np.arange(0, 16), 'NumberOfVehicles')
Queue = ctrl.Antecedent(np.arange(0, 500), 'Queue')
Duration_of_green = ctrl.Consequent(np.arange(0, 60), 'Duration')

NumberOfVehicles['Small'] = fuzz.trimf(NumberOfVehicles.universe, [0, 0, 4])
NumberOfVehicles['Quiet'] = fuzz.trimf(NumberOfVehicles.universe, [0, 4, 8])
NumberOfVehicles['Normal'] = fuzz.trimf(NumberOfVehicles.universe, [4, 8, 12])
NumberOfVehicles['Crowded'] = fuzz.trimf(NumberOfVehicles.universe, [8, 12, 16])
NumberOfVehicles['veryCrowded'] = fuzz.trimf(NumberOfVehicles.universe, [12, 16, 16])

Queue['veryShort'] = fuzz.trimf(Queue.universe, [0, 0, 125])
Queue['Short'] = fuzz.trimf(Queue.universe, [0, 125, 250])
Queue['Normal'] = fuzz.trimf(Queue.universe, [125, 250, 375])
Queue['Long'] = fuzz.trimf(Queue.universe, [250, 375, 500])
Queue['veryLong'] = fuzz.trimf(Queue.universe, [375, 500, 500])

Duration_of_green['Short'] = fuzz.trimf(Duration_of_green.universe, [15, 15, 30])
Duration_of_green['Normal'] = fuzz.trimf(Duration_of_green.universe, [15, 30, 45])
Duration_of_green['Long'] = fuzz.trimf(Duration_of_green.universe, [30, 45, 60])
Duration_of_green['Crowded'] = fuzz.trimf(Duration_of_green.universe, [45, 50, 60])
Duration_of_green['veryCrowded'] = fuzz.trimf(Duration_of_green.universe, [50, 60, 60])

rule1 = ctrl.Rule(
    (NumberOfVehicles['Small'] & Queue['veryShort']) |
    (NumberOfVehicles['Small'] & Queue['Short']) |
    (NumberOfVehicles['Small'] & Queue['Normal'])|
    (NumberOfVehicles['Small'] & Queue['Long'])|
    (NumberOfVehicles['Small'] & Queue['veryLong']), Duration_of_green['Short'])

rule2 = ctrl.Rule(
    (NumberOfVehicles['Quiet'] & Queue['veryShort']) |
    (NumberOfVehicles['Quiet'] & Queue['Short']) |
    (NumberOfVehicles['Quiet'] & Queue['Normal'])|
    (NumberOfVehicles['Quiet'] & Queue['Long'])|
    (NumberOfVehicles['Quiet'] & Queue['veryLong']), Duration_of_green['Normal'])

rule3 = ctrl.Rule(
    (NumberOfVehicles['Normal'] & Queue['veryShort']) |
    (NumberOfVehicles['Normal'] & Queue['Short']) |
    (NumberOfVehicles['Normal'] & Queue['Normal'])|
    (NumberOfVehicles['Normal'] & Queue['Long'])|
    (NumberOfVehicles['Normal'] & Queue['veryLong']), Duration_of_green['Long'])

rule4 = ctrl.Rule(
    (NumberOfVehicles['Crowded'] & Queue['veryShort']) |
    (NumberOfVehicles['Crowded'] & Queue['Normal']) |
    (NumberOfVehicles['Crowded'] & Queue['Long'])|
    (NumberOfVehicles['Crowded'] & Queue['Short'])|
    (NumberOfVehicles['Crowded'] & Queue['veryLong']), Duration_of_green['Crowded'])

rule5 = ctrl.Rule(
    (NumberOfVehicles['veryCrowded'] & Queue['Short']) |
    (NumberOfVehicles['veryCrowded'] & Queue['Normal']) |
    (NumberOfVehicles['veryCrowded'] & Queue['Long'])|
    (NumberOfVehicles['veryCrowded'] & Queue['Short'])|
    (NumberOfVehicles['veryCrowded'] & Queue['Normal']), Duration_of_green['veryCrowded'])
     
cmd_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
cmd_output = ctrl.ControlSystemSimulation(cmd_ctrl)

def deFuzzy(NumberOfVehicles, Queue):
    cmd_output.input['NumberOfVehicles'] = NumberOfVehicles
    cmd_output.input['Queue'] = Queue
    cmd_output.compute()
    result = cmd_output.output['Duration']
    return result






     


     