import random

def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    left = 1. / 10
    down = 1. / 11
    right = 1. / 30
    up = 1. / 20
    with open("test2.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="car" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="11.11" />
        <vType id="car1" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="11.11"/>

        <route id="left_up" edges="left -up" />
        <route id="left_right" edges="left -right" /> 
        <route id="left_down" edges="left -down" />
        <route id="down_left" edges="down -left" />
        <route id="down_up" edges="down -up" />
        <route id="down_right" edges="down -right" /> 
        <route id="right_down" edges="right -down" />
        <route id="right_left" edges="right -left" />
        <route id="right_up" edges="right -up" />
        <route id="up_right" edges="up -right" /> 
        <route id="up_down" edges="up -down" />
        <route id="up_left" edges="up -left" />""", file=routes)
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < left:
                print('    <vehicle id="left_%i" type="car" route="left_up" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < left:
                print('    <vehicle id="left_%i" type="car" route="left_right" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < left:
                print('    <vehicle id="left_%i" type="car1" route="left_down" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < down:
                print('    <vehicle id="down_%i" type="car1" route="down_left" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < down:
                print('    <vehicle id="down_%i" type="car" route="down_up" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < down:
                print('    <vehicle id="down_%i" type="car" route="down_right" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < right:
                print('    <vehicle id="right_%i" type="car1" route="right_down" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < right:
                print('    <vehicle id="right_%i" type="car1" route="right_left" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < right:
                print('    <vehicle id="right_%i" type="car" route="right_up" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < up:
                print('    <vehicle id="up_%i" type="car" route="up_right" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < up:
                print('    <vehicle id="up_%i" type="car1" route="up_down" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < up:
                print('    <vehicle id="up_%i" type="car1" route="up_left" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print("</routes>", file=routes)
