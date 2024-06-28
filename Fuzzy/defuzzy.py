
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import random


#Khởi tạo miền cho input
#Antecedent(universe, lable)
NumberOfVehicles= ctrl.Antecedent(np.arange(0, 16), 'NumberOfVehicles')
Queue = ctrl.Antecedent(np.arange(0, 500), 'Queue')


# Consequents(Universe, Lable): Số giây đèn xanh
Duration_of_green = ctrl.Consequent(np.arange(0, 60), 'Duration')
     
     
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
Duration_of_green['veryCrowded'] = fuzz.trimf(Duration_of_green.universe, [40, 60, 90])

# Xây dựng luật cho miền đèn xanh là ngắn (từ 0-20s)
rule1 = ctrl.Rule(
    (NumberOfVehicles['Small'] & Queue['veryShort']) |
    (NumberOfVehicles['Small'] & Queue['Short']) |
    (NumberOfVehicles['Small'] & Queue['Normal'])|
    (NumberOfVehicles['Small'] & Queue['Long'])|
    (NumberOfVehicles['Small'] & Queue['veryLong']), Duration_of_green['Short'])
     

# Xây dựng luật cho miền đèn xanh là vừa (từ 10-30s)
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
     

# Tổng hợp các Rules
cmd_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
cmd_output = ctrl.ControlSystemSimulation(cmd_ctrl)
     

# Enter values to test

'''NumberOfVehicles_value = float(input("Enter NumberOfVehicles"))

Queue_value = float(input("Enter Queue"))'''

output = []
xpoints = np.arange(1, 11)
NumberOfVehicles_value = np.array([2, 6, 9, 25, 5, 6, 12, 13, 15, 16])
Queue_value = np.array([104, 143, 273, 141, 100, 500, 300, 200, 300, 350])

for i in xpoints:
    cmd_output.input['NumberOfVehicles'] = NumberOfVehicles_value[i - 1]
    cmd_output.input['Queue'] = Queue_value[i - 1]

    cmd_output.compute()
    a = round(cmd_output.output['Duration'])

    output.append(a)


# Print output command and plots
print("Output: ")

for i in output:
    print(i)

#Duration_of_green.view()

#NumberOfVehicles.view()
#Queue.view()

#Duration_of_green.view(sim=cmd_output)

#a = input()






     


     