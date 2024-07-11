
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import random


#Khởi tạo miền cho input
#Antecedent(universe, lable)
NumberOfVehicles= ctrl.Antecedent(np.arange(0, 100), 'NumberOfVehicles')
Queue = ctrl.Antecedent(np.arange(0, 500), 'Queue')


# Consequents(Universe, Lable): Số giây đèn xanh
Duration_of_green = ctrl.Consequent(np.arange(0, 100), 'Duration')
     
######################################### DOMAIN #################################################     
# NumberOfVehicle memberships (Số lượng xe)
#trapmf: vẽ miền hình thang
NumberOfVehicles['Small'] = fuzz.trimf(NumberOfVehicles.universe, [0, 0, 4])
NumberOfVehicles['Quiet'] = fuzz.trimf(NumberOfVehicles.universe, [0, 4, 8])
NumberOfVehicles['Normal'] = fuzz.trimf(NumberOfVehicles.universe, [4, 8, 12])
NumberOfVehicles['Crowded'] = fuzz.trimf(NumberOfVehicles.universe, [8, 12, 16])
NumberOfVehicles['veryCrowded'] = fuzz.trimf(NumberOfVehicles.universe, [12, 16, 100])



# Queue memberships (Chiều dài hàng đợi)
Queue['veryShort'] = fuzz.trimf(Queue.universe, [0, 0, 3])
Queue['Short'] = fuzz.trimf(Queue.universe, [0, 3, 10])
Queue['Normal'] = fuzz.trimf(Queue.universe, [3, 10, 20])
Queue['Long'] = fuzz.trimf(Queue.universe, [10, 50, 100])
Queue['veryLong'] = fuzz.trimf(Queue.universe, [50, 100, 500])

# Duration memberships (Thời gian đèn xanh)
Duration_of_green['Short'] = fuzz.trimf(Duration_of_green.universe, [0, 10, 15])
Duration_of_green['Normal'] = fuzz.trimf(Duration_of_green.universe, [0, 20, 30])
Duration_of_green['Long'] = fuzz.trimf(Duration_of_green.universe, [20, 30, 40])
Duration_of_green['Crowded'] = fuzz.trimf(Duration_of_green.universe, [30, 35, 55])
Duration_of_green['veryCrowded'] = fuzz.trimf(Duration_of_green.universe, [35, 55, 100])
#########################################################################################

####################### Xay dung luat ###################################################
rule1 = ctrl.Rule(
    (NumberOfVehicles['veryCrowded'] & Queue['veryShort'])|
    (NumberOfVehicles['Quiet'] & Queue['veryShort']) |
    (NumberOfVehicles['Normal'] & Queue['veryShort']) |
    (NumberOfVehicles['Crowded'] & Queue['veryShort']) |
    (NumberOfVehicles['Small'] & Queue['veryShort'])|
    (NumberOfVehicles['Small'] & Queue['Short']) |
    (NumberOfVehicles['Small'] & Queue['Normal'])|
    (NumberOfVehicles['Small'] & Queue['Long'])|
    (NumberOfVehicles['Small'] & Queue['veryLong']), Duration_of_green['Short'])
     
rule2 = ctrl.Rule(
    (NumberOfVehicles['Normal'] & Queue['Short']) |   
    (NumberOfVehicles['Crowded'] & Queue['Short']) |
    (NumberOfVehicles['veryCrowded'] & Queue['Short'])|
    (NumberOfVehicles['Quiet'] & Queue['Short'])|
    (NumberOfVehicles['Quiet'] & Queue['Normal']), Duration_of_green['Normal'])

rule3 = ctrl.Rule(
    (NumberOfVehicles['veryCrowded'] & Queue['Normal'])|
    (NumberOfVehicles['Normal'] & Queue['Normal'])|
    (NumberOfVehicles['Quiet'] & Queue['Long'])|
    (NumberOfVehicles['Quiet'] & Queue['veryLong']), Duration_of_green['Long'])

rule4 = ctrl.Rule(
    (NumberOfVehicles['veryCrowded'] & Queue['Long'])|
    (NumberOfVehicles['Crowded'] & Queue['Normal'])|
    (NumberOfVehicles['Normal'] & Queue['Long'])|
    (NumberOfVehicles['Normal'] & Queue['veryLong']), Duration_of_green['Crowded'])

rule5 = ctrl.Rule(
    (NumberOfVehicles['veryCrowded'] & Queue['veryLong'])|
    (NumberOfVehicles['Crowded'] & Queue['Long'])|
    (NumberOfVehicles['Crowded'] & Queue['veryLong']), Duration_of_green['veryCrowded'])
     
###############################################################################################
# Tổng hợp các Rules
cmd_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
cmd_output = ctrl.ControlSystemSimulation(cmd_ctrl)

output = []
xpoints = np.arange(1, 7)
NumberOfVehicles_value = np.array([2, 2, 8, 8, 20, 20])
Queue_value = np.array([2, 100, 3, 30, 20, 200])

for i in xpoints:
    cmd_output.input['NumberOfVehicles'] = NumberOfVehicles_value[i - 1]
    cmd_output.input['Queue'] = Queue_value[i - 1]

    cmd_output.compute()
    a = round(cmd_output.output['Duration'])

    output.append(a)

def deFuzzy(NumberOfVehicles, Queue):
    result = 5
    if NumberOfVehicles != 0:
        cmd_output.input['NumberOfVehicles'] = NumberOfVehicles
        cmd_output.input['Queue'] = Queue
        cmd_output.compute()
        result = cmd_output.output['Duration']
    return result