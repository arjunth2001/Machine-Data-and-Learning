actions_to_states = {
    "C": [("UP", "N"), ("DOWN", "S"), ("LEFT", "W"), ("RIGHT", "E"), ("STAY", "C"), ("UP", "E"), ("DOWN", "E"), ("LEFT", "E"), ("STAY", "E"), ("SHOOT", "C"), ("HIT", "C")],
    "N": [("DOWN", "C"), ("STAY", "N"), ("DOWN", "E"), ("STAY", "E"), ("CRAFT", "N")],
    "S": [("UP", "C"), ("STAY", "S"), ("UP", "E"), ("STAY", "E"), ("GATHER", "S")],
}
states = [(pos, mat, arrow, state, health) for pos in ["W", "N", "E", "S", "C"] for mat in range(
    3) for arrow in range(4) for state in ["D", "R"] for health in range(0, 120, 25)]


def P(from_state, action, to_state):
    pos1, mat1, arrow1, state1, health1 = from_state
    pos2, mat2, arrow2, state2, health2 = from_state
    p1 = 0
    correction = False
    isAttacked = True

    # Demon Slayer
    p2 = 0
    if(state1 == "D" and state2 == "D"):  # He is lazy
        p2 = 0.8
    elif(state1 == "D" and state2 == "R"):  # He will attack soon
        p2 = 0.2
    # He didn't attack.. Lmao
    elif(state1 == "R" and state2 == "R"):
        p2 = 0.5
    else:  # He attacked?
        p2 = 0.5
        # SHit he successfully did it...
        if(health2 == health1+25 and (pos1 == "C" or pos1 == "E") and arrow2 == 0):
            isAttacked = True

    if(pos1 == "C" and mat1 == mat2):  # if in center square, mat equal
        # Successfully Moved
        if((action, pos2) in [actions_to_states["C"][0:5]] and health1 == health2 and arrow1 == arrow2):
            p1 = 0.85
            correction = True
        # failed
        elif(pos2 == "E" and action not in ["SHOOT", "HIT"] and health1 == health2 and arrow1 == arrow2):
            p1 = 0.15
        elif(action == "SHOOT"):  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.5
                    correction = True
                elif health2 == health1:  # Shit he missed
                    p1 = 0.5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == "C") and arrow1 == arrow2:
            if(health2 == health1-50):  # Dem he did damage
                correction = True
                p1 = 0.1
            elif(health2 == health1):  # Shit nothing happened...
                p1 = 0.9

    if pos1 == "N" and health1 == health2:
        if((action, pos2) in [actions_to_states["N"][0:2]] and arrow1 == arrow2 and mat1 == mat2):
            correction = True
            p1 = 0.85
        elif(pos2 == "E" and action not in ["CRAFT"] and mat2 == mat1 and arrow1 == arrow2):
            p1 = 0.15
        elif(action == "CRAFT" and mat1 > 0 and mat2 == 0):  # This need's clarification
            if(arrow2 == arrow1+1):
                p1 = 0.5
                correction = True
            if(arrow2 == arrow1+2):
                p1 = 0.35
                correction = True
            if(arrow2 == arrow1+3):
                p1 = 0.15
                correction = True

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        if((action, pos2) in [actions_to_states["S"][0:2]] and mat1 == mat2):
            correction = True
            p1 = 0.85
        elif(pos2 == "E" and action not in ["GATHER"] and mat2 == mat1):
            p1 = 0.15
        elif(action == "GATHER" and mat1 != 2):
            if mat1 == mat2-1:
                p1 = 0.75
                correction = True
            elif mat1 == mat2:
                p1 = 0.25

    if isAttacked and not correction:
        return p2
    if isAttacked and correction:
        return 0
    return p1*p2
