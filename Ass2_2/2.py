actions_to_states = {
    "C": [("UP", "N"), ("DOWN", "S"), ("LEFT", "W"), ("RIGHT", "E"), ("STAY", "C"), ("UP", "E"), ("DOWN", "E"), ("LEFT", "E"), ("STAY", "E"), ("SHOOT", "C"), ("HIT", "C")],
    "N": [("DOWN", "C"), ("STAY", "N"), ("DOWN", "E"), ("STAY", "E"), ("CRAFT", "N")],
    "S": [("UP", "C"), ("STAY", "S"), ("UP", "E"), ("STAY", "E"), ("GATHER", "S")],
    "E": [("LEFT", "C"), ("STAY", "E"), ("SHOOT", "E"), ("HIT", "E")],
    "W": [("RIGHT", "C"), ("STAY", "W"), ("SHOOT", "W")]
}
states = [(pos, mat, arrow, state, health) for pos in ["W", "N", "E", "S", "C"] for mat in range(
    3) for arrow in range(4) for state in ["D", "R"] for health in range(0, 120, 25)]


def P(from_state, action, to_state):
    pos1, mat1, arrow1, state1, health1 = from_state
    pos2, mat2, arrow2, state2, health2 = to_state
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

    if pos1 == "C" and mat1 == mat2:  # if in center square, mat equal
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
        # Successfully Moved
        if((action, pos2) in [actions_to_states["N"][0:2]] and arrow1 == arrow2 and mat1 == mat2):
            correction = True
            p1 = 0.85
        # failed
        elif(pos2 == "E" and action not in ["CRAFT"] and mat2 == mat1 and arrow1 == arrow2):
            p1 = 0.15
        elif(action == "CRAFT" and mat1 > 0 and mat2 == mat1 - 1):  # successfully crafting
            # 1 arrow crafted
            if(arrow2 == arrow1+1):
                p1 = 0.5
                correction = True
            # 2 arrows crafted
            if(arrow2 == arrow1+2):
                p1 = 0.35
                correction = True
            # 3 arrows crafted
            if(arrow2 == arrow1+3):
                p1 = 0.15
                correction = True

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["S"][0:2]] and mat1 == mat2):
            correction = True
            p1 = 0.85
        # failed
        elif(pos2 == "E" and action not in ["GATHER"] and mat2 == mat1):
            p1 = 0.15
        elif(action == "GATHER" and mat1 != 2):
            # Successfully gathered material
            if mat1 == mat2-1:
                p1 = 0.75
                correction = True
            # failed
            elif mat1 == mat2:
                p1 = 0.25
                
    if pos1 == "E" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["E"][0:2]]  and health1 == health2 and arrow1 == arrow2):
            correction = True
            p1 = 1.0
        elif(action == "SHOOT"):  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.9
                    correction = True
                elif health2 == health1:  # Shit he missed
                    p1 = 0.1
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == "C") and arrow1 == arrow2:
            if(health2 == health1-50):  # Dem he did damage
                correction = True
                p1 = 0.2
            elif(health2 == health1):  # Shit nothing happened...
                p1 = 0.8
                
    if pos1 == "W" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["W"][0:2]]  and health1 == health2 and arrow1 == arrow2):
            correction = True
            p1 = 1.0             
        elif(action == "SHOOT"):  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.25
                    correction = True
                elif health2 == health1:  # Shit he missed
                    p1 = 0.75       

    if isAttacked and not correction:
        return p2
    if isAttacked and correction:
        return 0
    return p1*p2

def R(from_state, action, to_state):
    reward = 0
    pos1, mat1, arrow1, state1, health1 = from_state
    pos2, mat2, arrow2, state2, health2 = to_state

    # Demon Slayer
    if state1 == "R" and state2 == "D":  # He attacked?
        return -45

    if pos1 == "C" and mat1 == mat2:  # if in center square, mat equal
        # Successfully Moved
        if((action, pos2) in [actions_to_states["C"][0:5]] and health1 == health2 and arrow1 == arrow2):
           reward = -5
        # failed
        elif(pos2 == "E" and action not in ["SHOOT", "HIT"] and health1 == health2 and arrow1 == arrow2):
            reward = -5
        elif(action == "SHOOT"):  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    if health2 <= 0:
                        reward = 45
                    else:
                        reward = -5
                elif health2 == health1:  # Shit he missed
                    reward = -5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == "C") and arrow1 == arrow2:
            if(health2 == health1-50):  # Dem he did damage
                if health2 <= 0:
                    reward = 45
                else:
                    reward = -5
            elif(health2 == health1):  # Shit nothing happened...
                reward = -5

    if pos1 == "N" and health1 == health2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["N"][0:2]] and arrow1 == arrow2 and mat1 == mat2):
            reward = -5
        # failed
        elif(pos2 == "E" and action not in ["CRAFT"] and mat2 == mat1 and arrow1 == arrow2):
            reward = -5
        elif(action == "CRAFT" and mat1 > 0 and mat2 == mat1 - 1):  # successfully crafting
            reward = -5

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["S"][0:2]] and mat1 == mat2):
            reward = -5
        # failed
        elif(pos2 == "E" and action not in ["GATHER"] and mat2 == mat1):
            reward = -5
        elif(action == "GATHER" and mat1 != 2):
            # Successfully gathered material
            reward = -5
                
    if pos1 == "E" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["E"][0:2]]  and health1 == health2 and arrow1 == arrow2):
            reward = -5
        elif(action == "SHOOT"):  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    if health2 <= 0:
                        reward = 45
                    else:
                        reward = -5
                elif health2 == health1:  # Shit he missed
                    reward = -5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == "C") and arrow1 == arrow2:
            if(health2 == health1-50):  # Dem he did damage
                if health2 <= 0:
                    reward = 45
                else:
                    reward = -5
            elif(health2 == health1):  # Shit nothing happened...
                reward = -5
                
    if pos1 == "W" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["W"][0:2]]  and health1 == health2 and arrow1 == arrow2):
            reward = -5          
        elif(action == "SHOOT"):  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    if health2 <= 0:
                        reward = 45
                    else:
                        reward = -5 
                elif health2 == health1:  # Shit he missed
                    reward = -5       
    return reward
    
