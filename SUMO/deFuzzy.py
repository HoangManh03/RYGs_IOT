import traci
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
Duration_of_green['Normal'] = fuzz.trimf(Duration_of_green.universe, [0, 15, 20])
Duration_of_green['Long'] = fuzz.trimf(Duration_of_green.universe, [15, 20, 30])
Duration_of_green['Crowded'] = fuzz.trimf(Duration_of_green.universe, [20, 30, 50])
Duration_of_green['veryCrowded'] = fuzz.trimf(Duration_of_green.universe, [35, 50, 90])

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
     
def set_next_phase_duration(tls_id, next_phase_index, duration):
    """
    Thiết lập thời gian cho pha tiếp theo của đèn giao thông.
    tls_id: ID của đèn giao thông
    next_phase_index: Chỉ số của pha tiếp theo cần điều chỉnh
    duration: Thời gian mới cho pha (giây)
    """
    logic = traci.trafficlight.getAllProgramLogics(tls_id)[0]
    logic.phases[next_phase_index].duration = duration
    traci.trafficlight.setProgramLogic(tls_id, logic)

tls_id = "J1"

def deFuzzy(Number_Vehicles, Queue, lane_id):
    current_phase = traci.trafficlight.getPhase(tls_id)
    #if(current_phase == 0):
    if current_phase == 0:
        next_phase = 2
    elif current_phase == 2:
        next_phase = 4
    elif current_phase == 4:
        next_phase = 6
    elif current_phase == 6:
        next_phase = 0
    #if next_phase_index == 0:
        #set_next_phase_duration(tls_id, 0, 30)

    cmd_output.input['NumberOfVehicles'] = Number_Vehicles
    cmd_output.input['Queue'] = Queue
    cmd_output.compute()
    result = round(cmd_output.output['Duration'])
    print(f"Queue on lane {lane_id}: {Queue}m")
    print(f"Number_of_vehicles on lane {lane_id} is {Number_Vehicles}")
    set_next_phase_duration(tls_id, next_phase, result)
    phase_duration = traci.trafficlight.getPhaseDuration(tls_id)
    print(f"phase_duration = {result}")
        #phase_duration = traci.trafficlight.getPhaseDuration(tls_id)
        #remaining_time = phase_duration - traci.trafficlight.getPhaseDuration(tls_id)
        #if(remaining_time == 5):  
        #print(f"Step {step}:")
        #np.round(Queue)