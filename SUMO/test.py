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
lane_left = "left_0"
lane_right = "right_0"
lane_up = "up_0"
lane_down = "down_0"

#Khai báo id nút giao
tls_id = "J1"

#FPS
delay = 1/10

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
        #Lấy tọa độ của xe đầu tiên và xe cuối cùng trên làn đường 'lane_id1'
        #first_vehicle_position, last_vehicle_position = get_input.get_first_and_last_vehicle_positions(lane_left)
#
        ##Nếu trên làn đường 'lane_id1' có xe thì tính khoảng cách xe đầu tiên và xe cuối cùng
        #if first_vehicle_position and last_vehicle_position:
        #    distance = math.sqrt((last_vehicle_position[0] - first_vehicle_position[0])**2 + 
        #                         (last_vehicle_position[1] - first_vehicle_position[1])**2)
        #    vehicle_count = get_input.count_vehicles_on_lane(lane_left)
        ##Nếu trên làn đường 'lane_id1' không có xe thì khoảng cách và số xe = 0
        #else: 
        #    distance = 0
        #    vehicle_count = 0
        vehicle_count = get_input.count_vehicles_on_lane(lane_left)
        distance = get_input.get_distance_to_last_vehicle(tls_id, lane_left)
        #Bắt đầu áp dụng thuật toán để tính thời gian đèn
        #xanh phù hợp cho pha tiếp theo tại 5s cuối của pha hiện tại
        if remain_time_duration == 5: 
            deFuzzy.deFuzzy(vehicle_count, distance, lane_left)
    if current_phase == 2:
        #Lấy tọa độ của xe đầu tiên và xe cuối cùng trên làn đường 'lane_id3'
        first_vehicle_position, last_vehicle_position = get_input.get_first_and_last_vehicle_positions(lane_down)
        #Nếu trên làn đường 'lane_id3' có xe thì tính khoảng cách xe đầu tiên và xe cuối cùng
        if first_vehicle_position and last_vehicle_position:
            distance = math.sqrt((last_vehicle_position[0] - first_vehicle_position[0])**2 + 
                                 (last_vehicle_position[1] - first_vehicle_position[1])**2)
            vehicle_count = get_input.count_vehicles_on_lane(lane_down)
        #Nếu không có xe thì khoảng cách và số xe = 0
        else: 
            distance = 0
            vehicle_count = 0
      
        #Bắt đầu áp dụng thuật toán để tính thời gian đèn
        #xanh phù hợp cho pha tiếp theo tại 5s cuối của pha hiện tại
        if remain_time_duration == 5:
            deFuzzy.deFuzzy(vehicle_count, distance, lane_down)
    if current_phase == 4:
        #Lấy tọa độ của xe đầu tiên và xe cuối cùng trên làn đường 'lane_id1'
        first_vehicle_position, last_vehicle_position = get_input.get_first_and_last_vehicle_positions(lane_right)
        #Nếu trên làn đường 'lane_id1' có xe thì tính khoảng cách xe đầu tiên và xe cuối cùng
        if first_vehicle_position and last_vehicle_position:
            distance = math.sqrt((last_vehicle_position[0] - first_vehicle_position[0])**2 + 
                                 (last_vehicle_position[1] - first_vehicle_position[1])**2)
            vehicle_count = get_input.count_vehicles_on_lane(lane_right)
        #Nếu trên làn đường 'lane_id1' không có xe thì khoảng cách và số xe = 0
        else: 
            distance = 0
            vehicle_count = 0
        
        #Bắt đầu áp dụng thuật toán để tính thời gian đèn
        #xanh phù hợp cho pha tiếp theo tại 5s cuối của pha hiện tại
        if remain_time_duration == 5: 
            deFuzzy.deFuzzy(vehicle_count, distance, lane_right)
    if current_phase == 6:
        #Lấy tọa độ của xe đầu tiên và xe cuối cùng trên làn đường 'lane_id1'
        first_vehicle_position, last_vehicle_position = get_input.get_first_and_last_vehicle_positions(lane_up)
        #Nếu trên làn đường 'lane_id1' có xe thì tính khoảng cách xe đầu tiên và xe cuối cùng
        if first_vehicle_position and last_vehicle_position:
            distance = math.sqrt((last_vehicle_position[0] - first_vehicle_position[0])**2 + 
                                 (last_vehicle_position[1] - first_vehicle_position[1])**2)
            vehicle_count = get_input.count_vehicles_on_lane(lane_up)
        #Nếu trên làn đường 'lane_id1' không có xe thì khoảng cách và số xe = 0
        else: 
            distance = 0
            vehicle_count = 0        
        #Bắt đầu áp dụng thuật toán để tính thời gian đèn
        #xanh phù hợp cho pha tiếp theo tại 5s cuối của pha hiện tại
        if remain_time_duration == 5: 
            deFuzzy.deFuzzy(vehicle_count, distance, lane_up)
    print(f"current_phase: {current_phase}")
    print(remain_time_duration)

    #Sau mỗi step nhất định thì sẽ tạo ra một xe
    #if step % 10 == 0:
    #    vehicle_id = f"lefttoright_{step}"
    #    traci.vehicle.add(vehID=vehicle_id, routeID="route_1", typeID="car", depart=step)
    #if step % 7 == 0:
    #    vehicle_id1 = f"uptodown_{step}"
    #    traci.vehicle.add(vehID=vehicle_id1, routeID="route_2", typeID="car2", depart=step)
    step += 1

traci.close()






