import traci

def Detect_tls(detector_id, vehicle_count):
    if traci.inductionloop.getLastStepVehicleIDs(detector_id):
        vehicle_count.append(traci.inductionloop.getLastStepVehicleIDs(detector_id))