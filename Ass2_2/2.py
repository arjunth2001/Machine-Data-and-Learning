actions_to_states = {
    "C": [("UP", "N"), ("DOWN", "S"), ("LEFT", "W"), ("RIGHT", "E"), ("STAY", "C"), ("UP", "E"), ("DOWN", "E"), ("LEFT", "E"), ("STAY", "E"), ("SHOOT", "C"), ("HIT", "C")],
    "N": [("DOWN", "C"), ("STAY", "N"), ("DOWN", "E"), ("STAY", "E"), ("CRAFT", "N")],
    "S": [("UP", "C"), ("STAY", "S"), ("UP", "E"), ("STAY", "E"), ("GATHER", "S")],
    "E": [("LEFT", "C"), ("STAY", "E"), ("SHOOT", "E"), ("HIT", "E")],
    "W": [("RIGHT", "C"), ("STAY", "W"), ("SHOOT", "W")]
}
states = [(pos, mat, arrow, state, health) for pos in ["W", "N", "E", "S", "C"] for mat in range(
    3) for arrow in range(4) for state in ["D", "R"] for health in range(0, 120, 25)]
Gamma = 0.999
Delta = 0.5
utility = {
    pos: 0 for pos in ["W", "N", "E", "S", "C"]
}
utility_prime = {
    pos: 0 for pos in ["W", "N", "E", "S", "C"]
}


def P(from_state, action, to_state):
    pos1, mat1, arrow1, state1, health1 = from_state
    pos2, mat2, arrow2, state2, health2 = to_state
    p1 = 0
    correction = False
    isAttacked = False
    isValid = False

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
            isValid = True
            correction = True
        # failed
        elif(pos2 == "E" and action not in ["SHOOT", "HIT"] and health1 == health2 and arrow1 == arrow2):
            p1 = 0.15
            isValid = True
        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.5
                    isValid = True
                    correction = True
                elif health2 == health1:  # Shit he missed
                    isValid = True
                    p1 = 0.5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == pos1) and arrow1 == arrow2:
            if(health2 == health1-50):  # Dem he did damage
                correction = True
                isValid = True
                p1 = 0.1
            elif(health2 == health1):  # Shit nothing happened...
                isValid = True
                p1 = 0.9

    if pos1 == "N" and health1 == health2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["N"][0:2]] and arrow1 == arrow2 and mat1 == mat2):
            correction = True
            isValid = True
            p1 = 0.85
        # failed
        elif(pos2 == "E" and action not in ["CRAFT"] and mat2 == mat1 and arrow1 == arrow2):
            p1 = 0.15
            isValid = True
        elif(action == "CRAFT" and mat1 > 0 and mat2 == mat1 - 1 and pos1 == pos2):  # successfully crafting
            # 1 arrow crafted
            if(arrow2 == arrow1+1):
                p1 = 0.5
                correction = True
                isValid = True    
            # 2 arrows crafted
            if(arrow2 == arrow1+2):
                p1 = 0.35
                correction = True
                isValid = True
            # 3 arrows crafted
            if(arrow2 == arrow1+3):
                p1 = 0.15
                correction = True
                isValid = True

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["S"][0:2]] and mat1 == mat2):
            correction = True
            isValid = True
            p1 = 0.85
        # failed
        elif(pos2 == "E" and action not in ["GATHER"] and mat2 == mat1):
            p1 = 0.15
            isValid = True
        elif(action == "GATHER" and mat1 != 2 and pos1 == pos2):
            # Successfully gathered material
            if mat1 == mat2-1:
                p1 = 0.75
                correction = True
                isValid = True
            # failed
            elif mat1 == mat2:
                p1 = 0.25
                isValid = True

    if pos1 == "E" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["E"][0:2]] and health1 == health2 and arrow1 == arrow2):
            correction = True
            p1 = 1.0
            isValid = True
        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.9
                    correction = True
                    isValid = True
                elif health2 == health1:  # Shit he missed
                    p1 = 0.1
                    isValid = True
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == pos1) and arrow1 == arrow2:
            if(health2 == health1-50):  # Dem he did damage
                correction = True
                p1 = 0.2
                isValid = True
            elif(health2 == health1):  # Shit nothing happened...
                p1 = 0.8
                isValid = True

    if pos1 == "W" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["W"][0:2]] and health1 == health2 and arrow1 == arrow2):
            correction = True
            isValid = True
            p1 = 1.0
        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.25
                    isValid = True
                    correction = True
                elif health2 == health1:  # Shit he missed
                    p1 = 0.75
                    isValid = True

    if not isValid:
        return 0
    if isAttacked and not correction:
        return p2
    if isAttacked and correction:
        return 0
    return p1*p2


def R(from_state, action, to_state):
    reward = 0
    pos1, mat1, arrow1, state1, health1 = from_state
    pos2, mat2, arrow2, state2, health2 = to_state

    if pos1 == "C" and mat1 == mat2:  # if in center square, mat equal
        # Successfully Moved
        if((action, pos2) in [actions_to_states["C"][0:5]] and health1 == health2 and arrow1 == arrow2):
            reward = -5
        # failed
        elif(pos2 == "E" and action not in ["SHOOT", "HIT"] and health1 == health2 and arrow1 == arrow2):
            reward = -5
        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    if health2 == 0:
                        reward = 45
                    else:
                        reward = -5
                elif health2 == health1:  # Shit he missed
                    reward = -5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == pos1) and arrow1 == arrow2:
            if(health2 == health1-50):  # Dem he did damage
                if health2 == 0:
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
        elif(action == "CRAFT" and mat1 > 0 and mat2 == mat1 - 1 and pos1 == pos2):  # successfully crafting
            if(arrow2 == arrow1+1):
                reward = -5
            # 2 arrows crafted
            if(arrow2 == arrow1+2):
                reward = -5
            if(arrow2 == arrow1+3):
                reward = -5

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["S"][0:2]] and mat1 == mat2):
            reward = -5
        # failed
        elif(pos2 == "E" and action not in ["GATHER"] and mat2 == mat1):
            reward = -5
        elif(action == "GATHER" and mat1 != 2 and pos2 == pos1):
            # Successfully gathered material
            if mat1 == mat2-1:
                reward = -5
            # failed
            elif mat1 == mat2:
                reward = -5

    if pos1 == "E" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["E"][0:2]] and health1 == health2 and arrow1 == arrow2):
            reward = -5
        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    if health2 == 0:
                        reward = 45
                    else:
                        reward = -5
                elif health2 == health1:  # Shit he missed
                    reward = -5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == pos1) and arrow1 == arrow2:
            if(health2 == health1-50):  # Dem he did damage
                if health2 == 0:
                    reward = 45
                else:
                    reward = -5
            elif(health2 == health1):  # Shit nothing happened...
                reward = -5

    if pos1 == "W" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in [actions_to_states["W"][0:2]] and health1 == health2 and arrow1 == arrow2):
            reward = -5
        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    if health2 == 0:
                        reward = 45
                    else:
                        reward = -5
                elif health2 == health1:  # Shit he missed
                    reward = -5
    if reward != 0:
        if state1 == "R" and state2 == "D":  # He attacked?
            return -45
    return reward

iteration_number = 0
while iteration_number < 1:
    iteration_number += 1
    print (f'iteration={iteration_number}')
    max_diff = None
    for from_state in states:
        optimal_action = "NONE"
        pos1, mat1, arrow1, state1, health1 = from_state
        if health1 == 0:
            continue
        valid_next_states = []
        valid_actions = []
        for i_state in actions_to_states[pos1]:
            valid_actions.append(i_state[0])
            for state in states:
                if i_state[1] == state[0]:
                    valid_next_states.append(state)
        max_utility = None
        valid_actions = set(valid_actions)
        for action in valid_actions:
            sum_of_all_next_state_utilities = 0
            for to_state in valid_next_states:
                pos2, mat2, arrow2, state2, health2 = to_state
                p = P(from_state, action, to_state)
                r = R(from_state, action, to_state)
                # if ((p == 1000 or p == -1000) and r != 0) or ((p != 1000 and p != -1000) and r == 0):
                #     print (f'P={p} and R={r}')
                #     quit()
                # if p != 0 and r != 0:
                #     print (f'From state:   ({pos1},{mat1},{arrow1},{state1},{health1})') 
                #     print (f'Action:        {action}')
                #     print (f'To state:     ({pos2},{mat2},{arrow2},{state2},{health2})') 
                #     print(f'P={p}, R={r}')
                #     print('-'*10)                    
                sum_of_all_next_state_utilities += (p * (r + (Gamma * utility[pos1])))
            if max_utility == None or (max_utility != None and sum_of_all_next_state_utilities > max_utility):
                max_utility = (sum_of_all_next_state_utilities)
                optimal_action = action
        utility_prime[pos1] = max_utility 
        # print (f'({pos1},{mat1},{arrow1},{state1},{health1}):{optimal_action}=[{utility_prime[pos1]}]') 
        if max_diff == None:
            max_diff = abs(utility_prime[pos1] - utility[pos1])
        else:
            max_diff = max(max_diff, abs(utility_prime[pos1] - utility[pos1]))
    utility = utility_prime.copy()
    # print(f'Max diff is {max_diff}')
    if max_diff < Delta:
        break
    
                