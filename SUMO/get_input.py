import traci
import math

#Lấy tọa độ của xe đầu tiên và xe cuối cùng ở hàng đợi
def get_first_and_last_vehicle_positions(lane_id):
    vehicle_ids = traci.lane.getLastStepVehicleIDs(lane_id)
    
    if not vehicle_ids:
        return None, None
    
    positions = [(traci.vehicle.getPosition(vid), vid) for vid in vehicle_ids]
    
    positions_sorted = sorted(positions, key=lambda pos: traci.vehicle.getLanePosition(pos[1]))
    
    first_vehicle_position = positions_sorted[0][0]
    last_vehicle_position = positions_sorted[-1][0]
    
    return first_vehicle_position, last_vehicle_position

def get_distance_to_last_vehicle(junction_id, lane_ids):
    # Lấy tọa độ của ngã tư
    junction_position = traci.junction.getPosition(junction_id)
    junction_x, junction_y = junction_position
    distance_new = 0
    # Lấy danh sách các xe trên làn đường
    for lane_id in lane_ids:
        vehicle_ids = traci.lane.getLastStepVehicleIDs(lane_id)

        if not vehicle_ids:
            vehicle_ids = 0
        else:
            # Lấy ID của xe cuối cùng
            last_vehicle_id = vehicle_ids[0]
            # Lấy vị trí của xe cuối cùng
            last_vehicle_position = traci.vehicle.getPosition(last_vehicle_id)
            last_vehicle_x, last_vehicle_y = last_vehicle_position
            # Tính khoảng cách từ ngã tư đến xe cuối cùng
            distance = calculate_distance(junction_x, junction_y, last_vehicle_x, last_vehicle_y)
            if distance > distance_new:
                distance_new = distance
                #print(f"list_vehicles = {vehicle_ids}")
                #print(f"last_vehicle_position = {last_vehicle_position}")
                #print(f"junction_position = {junction_position}")
                #print(f"distance = {distance}")
                #print(f"distance_new = {distance_new}")
                #print(f"last_vehicle_id: {last_vehicle_id}")
    return distance_new

#Đếm số xe ở hàng đợi
def count_vehicles_on_lane(lane_ids):
    numbers_vehicles = 0
    for lane_id in lane_ids:
        numbers_vehicles += traci.lane.getLastStepVehicleNumber(lane_id)
    return numbers_vehicles
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

