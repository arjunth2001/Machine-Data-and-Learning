import numpy as np
import os


def P(from_state, action, to_state, actions_to_states):
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
        if((health2 == health1+25 or (health1 == health2 and health2 == 100)) and (pos1 == "C" or pos1 == "E") and arrow2 == 0):
            isAttacked = True

    if pos1 == "C" and mat1 == mat2:  # if in center square, mat equal
        # Successfully Moved
        if((action, pos2) in actions_to_states["C"][0:5] and health1 == health2 and arrow1 == arrow2):
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
            if(health2 == health1-50 or (health2 == 0 and health1 == 25)):  # Dem he did damage
                correction = True
                isValid = True
                p1 = 0.1
            elif(health2 == health1):  # Shit nothing happened...
                isValid = True
                p1 = 0.9

    if pos1 == "N" and health1 == health2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["N"][0:2] and arrow1 == arrow2 and mat1 == mat2):
            correction = True
            isValid = True
            p1 = 0.85
        # failed
        elif(pos2 == "E" and action not in ["CRAFT"] and mat2 == mat1 and arrow1 == arrow2):
            p1 = 0.15
            isValid = True
        elif(action == "CRAFT" and mat1 > 0 and mat2 == mat1 - 1 and pos1 == pos2):  # successfully crafting
            if arrow1 == 0:
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
            if arrow1 == 1:
                if arrow2 == 2 or arrow2 == 3:
                    p1 = 0.5
                    correction = True
                    isValid = True
            if arrow1 == 2:
                if arrow2 == 3:
                    p1 = 1
                    correction = True
                    isValid = True

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["S"][0:2] and mat1 == mat2):
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
        if((action, pos2) in actions_to_states["E"][0:2] and health1 == health2 and arrow1 == arrow2):
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
            if(health2 == health1-50 or (health2 == 0 and health1 == 25)):  # Dem he did damage
                correction = True
                p1 = 0.2
                isValid = True
            elif(health2 == health1):  # Shit nothing happened...
                p1 = 0.8
                isValid = True

    if pos1 == "W" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["W"][0:2] and health1 == health2 and arrow1 == arrow2):
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


def R(from_state, action, to_state, actions_to_states):
    reward = 0
    pos1, mat1, arrow1, state1, health1 = from_state
    pos2, mat2, arrow2, state2, health2 = to_state

    if pos1 == "C" and mat1 == mat2:  # if in center square, mat equal
        # Successfully Moved
        if((action, pos2) in actions_to_states["C"][0:5] and health1 == health2 and arrow1 == arrow2):
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
            if(health2 == health1-50 or (health2 == 0 and health1 == 25)):  # Dem he did damage
                if health2 == 0:
                    reward = 45
                else:
                    reward = -5
            elif(health2 == health1):  # Shit nothing happened...
                reward = -5

    if pos1 == "N" and health1 == health2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["N"][0:2] and arrow1 == arrow2 and mat1 == mat2):
            reward = -5
        # failed
        elif(pos2 == "E" and action not in ["CRAFT"] and mat2 == mat1 and arrow1 == arrow2):
            reward = -5
        elif(action == "CRAFT" and mat1 > 0 and mat2 == mat1 - 1 and pos1 == pos2):  # successfully crafting
            if arrow2 > arrow1:
                reward = -5

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["S"][0:2] and mat1 == mat2):
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
        if((action, pos2) in actions_to_states["E"][0:2] and health1 == health2 and arrow1 == arrow2):
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
            if(health2 == health1-50 or (health2 == 0 and health1 == 25)):  # Dem he did damage
                if health2 == 0:
                    reward = 45
                else:
                    reward = -5
            elif(health2 == health1):  # Shit nothing happened...
                reward = -5

    if pos1 == "W" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["W"][0:2] and health1 == health2 and arrow1 == arrow2):
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
        # He attacked?
        if (health2 == health1+25 or (health1 == health2 and health2 == 100)) and (pos1 == "C" or pos1 == "E") and arrow2 == 0:
            return -45
    return reward


def action_is_successful(success_prob):
    result = np.random.uniform()
    return result < success_prob


def get_MM_next_state(current_state):
    pos1, mat1, arrow1, state1, health1 = current_state
    if state1 == "D":
        if action_is_successful(0.2):
            state1 = "R"
    else:
        if action_is_successful(0.5):
            state1 = "D"
    return state1


def get_IJ_next_state(current_state, next_action):
    pos1, mat1, arrow1, mm1, health1 = current_state
    pos2, mat2, arrow2, mm2, health2 = current_state

    mm2 = get_MM_next_state(current_state)

    if mm1 == "R" and mm2 == "D":
        # attack happened
        if pos1 == "C" or pos1 == "E":
            # attack affected IJ
            if health2 < 100:
                health2 += 25
            arrow2 = 0
            return pos2, mat2, arrow2, mm2, health2

    if pos1 == "C":
        if next_action == "UP":
            if action_is_successful(0.85):
                pos2 = "N"
            else:
                pos2 = "E"
        if next_action == "DOWN":
            if action_is_successful(0.85):
                pos2 = "S"
            else:
                pos2 = "E"
        if next_action == "LEFT":
            if action_is_successful(0.85):
                pos2 = "W"
            else:
                pos2 = "E"
        if next_action == "RIGHT":
            pos2 = "E"
        if next_action == "STAY":
            if action_is_successful(0.85):
                pos2 = "C"
            else:
                pos2 = "E"
        if next_action == "HIT":
            if action_is_successful(0.1):
                if health2 < 50:
                    health2 = 0
                else:
                    health2 -= 50
        if next_action == "SHOOT":
            arrow2 -= 1
            if action_is_successful(0.5):
                if health2 > 0:
                    health2 -= 25

    if pos1 == "N":
        if next_action == "DOWN":
            if action_is_successful(0.85):
                pos2 = "C"
            else:
                pos2 = "E"
        if next_action == "STAY":
            if action_is_successful(0.85):
                pos2 = "N"
            else:
                pos2 = "E"
        if next_action == "CRAFT":
            mat2 -= 1
            prob_arrows = np.random.uniform()
            if prob_arrows < 0.5:
                arrow2 += 1
            elif prob_arrows < 0.85:
                arrow2 += 2
            else:
                arrow2 += 3
            if arrow2 > 3:
                arrow2 = 3

    if pos1 == "S":
        if next_action == "UP":
            if action_is_successful(0.85):
                pos2 = "C"
            else:
                pos2 = "E"
        if next_action == "STAY":
            if action_is_successful(0.85):
                pos2 = "S"
            else:
                pos2 = "E"
        if next_action == "GATHER":
            if action_is_successful(0.75):
                mat2 += 1

    if pos1 == "E":
        if next_action == "LEFT":
            pos2 = "C"
        if next_action == "STAY":
            pos2 = "E"
        if next_action == "SHOOT":
            arrow2 -= 1
            if action_is_successful(0.9):
                if health2 > 0:
                    health2 -= 25
        if next_action == "HIT":
            if action_is_successful(0.2):
                if health2 < 50:
                    health2 = 0
                else:
                    health2 -= 50

    if pos1 == "W":
        if next_action == "RIGHT":
            pos2 = "C"
        if next_action == "STAY":
            pos2 = "W"
        if next_action == "SHOOT":
            arrow2 -= 1
            if action_is_successful(0.25):
                if health2 > 0:
                    health2 -= 25

    return pos2, mat2, arrow2, mm2, health2


def simulate_IJ_movement(start_state, policy, f2):

    current_state = start_state
    step_count = 1
    while True:
        pos1, mat1, arrow1, state1, health1 = current_state
        print(
            f'Step Number: {step_count}  Current State: ({pos1},{mat1},{arrow1},{state1},{health1})  Taking Action: {policy[current_state]}', file=f2)
        if health1 == 0:
            break
        current_state = get_IJ_next_state(current_state, policy[current_state])
        step_count += 1


def Indiana_Jones(task, start_state_num):
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
    Delta = 0.001
    policy = {
        state: "NONE" for state in states
    }
    actions = ["UP", "LEFT", "DOWN", "RIGHT",
               "STAY", "SHOOT", "HIT", "CRAFT", "GATHER"]

    utility = {
        state: 0 for state in states
    }

    utility_prime = {
        state: 0 for state in states
    }

    if task == 0:
        f = open("outputs/part_2_trace.txt", "w")
    else:
        f = open(f"outputs/part_2_trace.{task}_trace.txt", "w")
        if task == 1:
            actions_to_states = {
                "C": [("UP", "N"), ("DOWN", "S"), ("LEFT", "W"), ("RIGHT", "E"), ("STAY", "C"), ("UP", "E"), ("DOWN", "E"), ("LEFT", "E"), ("STAY", "E"), ("SHOOT", "C"), ("HIT", "C")],
                "N": [("DOWN", "C"), ("STAY", "N"), ("DOWN", "E"), ("STAY", "E"), ("CRAFT", "N")],
                "S": [("UP", "C"), ("STAY", "S"), ("UP", "E"), ("STAY", "E"), ("GATHER", "S")],
                "E": [("LEFT", "W"), ("STAY", "E"), ("SHOOT", "E"), ("HIT", "E")],
                "W": [("RIGHT", "C"), ("STAY", "W"), ("SHOOT", "W")]
            }
        if task == 3:
            Gamma = 0.25
    iteration_number = -1
    while True:
        iteration_number += 1
        print(f'iteration={iteration_number}', file=f)
        max_diff = None
        for from_state in states:
            optimal_action = "NONE"
            pos1, mat1, arrow1, state1, health1 = from_state
            if health1 == 0:
                print(
                    f'({pos1},{mat1},{arrow1},{state1},{health1}):NONE=[{round(utility_prime[from_state],3)}]', file=f)
                continue
            max_utility = None
            valid_actions = []
            for i_state in actions_to_states[pos1]:
                valid_actions.append(i_state[0])
            valid_actions = set(valid_actions)
            for action in valid_actions:
                sum_of_all_next_state_utilities = 0
                isValid = False
                for to_state in states:
                    p = P(from_state, action, to_state, actions_to_states)
                    r = R(from_state, action, to_state, actions_to_states)
                    if(p != 0):
                        isValid = True
                        # if pos1 == "W" and action == "UP":
                        #     print(f'P={p} and R={r}')
                    if task == 2 and action == "STAY":
                        r = 0
                    sum_of_all_next_state_utilities += (
                        p * (r + (Gamma * utility[to_state])))
                if isValid:
                    if max_utility == None or (max_utility != None and sum_of_all_next_state_utilities > max_utility):
                        max_utility = (sum_of_all_next_state_utilities)
                        optimal_action = action
            utility_prime[from_state] = max_utility
            policy[from_state] = optimal_action
            print(
                f'({pos1},{mat1},{arrow1},{state1},{health1}):{optimal_action}=[{round(utility_prime[from_state],3)}]', file=f)
            if max_diff == None:
                max_diff = abs(utility_prime[from_state] - utility[from_state])
            else:
                max_diff = max(max_diff, abs(
                    utility_prime[from_state] - utility[from_state]))
        utility = utility_prime.copy()
        # print(f'Max diff is {max_diff}')
        #print("-"*30, file=f)
        #print("\n", file=f)
        if max_diff < Delta:
            break
    f.close()
    if task == 0:
        if start_state_num == 2:
            f2 = open("outputs/part_2_simulation_state_2.txt", "w")
            simulate_IJ_movement(("C", 2, 0, "R", 100), policy, f2)
        elif start_state_num == 1:
            f2 = open("outputs/part_2_simulation_state_1.txt", "w")
            simulate_IJ_movement(("W", 0, 0, "D", 100), policy, f2)
        f2.close()


if not os.path.exists("./outputs"):
    os.mkdir("outputs")
Indiana_Jones(0, 1)
print("done")
Indiana_Jones(0, 2)
print("done")
Indiana_Jones(1, 0)
print("done")
Indiana_Jones(2, 0)
print("done")
Indiana_Jones(3, 0)
