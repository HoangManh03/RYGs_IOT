import traci
import math
import deFuzzy
import time
import get_input
import detect
import generate_route

generate_route.generate_routefile()
sumoCmd = ["sumo-gui", "-c", "test.sumocfg"]
traci.start(sumoCmd)

step = 0

#Khai báo id các làn đường
lane_left = ["left_1", "left_2"]
lane_right = ["right_1", "right_2"]
lane_up = ["up_1", "up_2"]
lane_down = ["down_1", "down_2"]

#Khai báo id nút giao
tls_id = "J1"

#FPS
delay = 1/4

#detector_id
detector_id = 'det_0'

vehicles_exited_lane = []

#Số step là 200
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    #Số khung hình trên giây (FPS)
    time.sleep(delay)
    current_phase = traci.trafficlight.getPhase(tls_id)
    remain_time_duration = traci.trafficlight.getNextSwitch(tls_id) - traci.simulation.getTime()
    if current_phase == 0:
        #Bắt đầu áp dụng thuật toán để tính thời gian đèn
        #xanh phù hợp cho pha tiếp theo tại 5s cuối của pha hiện tại
        if remain_time_duration == 5: 
            distance = get_input.get_distance_to_last_vehicle(tls_id, lane_left)
            vehicle_count = get_input.count_vehicles_on_lane(lane_left)

            deFuzzy.deFuzzy(vehicle_count, distance, lane_left)
    if current_phase == 2:
       
        #Bắt đầu áp dụng thuật toán để tính thời gian đèn
        #xanh phù hợp cho pha tiếp theo tại 5s cuối của pha hiện tại
        if remain_time_duration == 5:
             #Lấy tọa độ của xe đầu tiên và xe cuối cùng trên làn đường 'lane_id3'
            distance = get_input.get_distance_to_last_vehicle(tls_id, lane_down)
            vehicle_count = get_input.count_vehicles_on_lane(lane_down)

            deFuzzy.deFuzzy(vehicle_count, distance, lane_down)
    if current_phase == 4:
        
        #Bắt đầu áp dụng thuật toán để tính thời gian đèn
        #xanh phù hợp cho pha tiếp theo tại 5s cuối của pha hiện tại
        if remain_time_duration == 5: 
            distance = get_input.get_distance_to_last_vehicle(tls_id, lane_right)
            vehicle_count = get_input.count_vehicles_on_lane(lane_right)

            deFuzzy.deFuzzy(vehicle_count, distance, lane_right)
    if current_phase == 6:
        

        #Bắt đầu áp dụng thuật toán để tính thời gian đèn
        #xanh phù hợp cho pha tiếp theo tại 5s cuối của pha hiện tại
        if remain_time_duration == 5: 
            distance = get_input.get_distance_to_last_vehicle(tls_id, lane_up)
            vehicle_count = get_input.count_vehicles_on_lane(lane_up)
            deFuzzy.deFuzzy(vehicle_count, distance, lane_up)

    print(f"current_phase: {current_phase}")
    print(remain_time_duration)
    #if remain_time_duration == 5:
    #    vehicles_count = get_input.count_vehicles_on_lane(lane_left)
    #    distance = get_input.get_distance_to_last_vehicle(tls_id, lane_left)
    #    print(f"Số lượng xe = {vehicles_count}")
    #    print(f"distance = {distance}")
    #if step % 10 == 0:
    #    vehicle_id = f"lefttoright_{step}"
    #    traci.vehicle.add(vehID=vehicle_id, routeID="left_right", typeID="car", depart=step)
    #if step % 30 == 5:
    #    vehicle_id1 = f"lefttoup_{step}"
    #    traci.vehicle.add(vehID=vehicle_id1, routeID="left_up", typeID="car1", depart=step)
    step += 1

traci.close()






