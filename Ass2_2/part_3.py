import numpy as np
import cvxpy as cp
import os
import json


def P(from_state, action, to_state, actions_to_states):
    pos1, mat1, arrow1, state1, health1 = from_state
    pos2, mat2, arrow2, state2, health2 = to_state
    p1 = 0

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
        if (pos1 == "C" or pos1 == "E") and (health1 >= health2 and health2 != 100):
            return 0
        if (pos1 == "C" or pos1 == "E") and (arrow2 != 0):
            return 0
            # SHit he successfully did it...
        if((health2 == health1+25 or (health1 == health2 and health2 == 100)) and (pos1 == "C" or pos1 == "E") and arrow2 == 0):
            if(pos1 == pos2 and mat1 == mat2):
                if (action == "SHOOT" and arrow1 == 0) or (action == "CRAFT" and mat1 == 0):
                    return 0
                else:
                    return p2

            else:
                return 0

    if pos1 == "C" and mat1 == mat2:  # if in center square, mat equal
        # Successfully Moved
        if pos2 == "E" and action == "RIGHT" and health1 == health2 and arrow1 == arrow2:
            p1 = 1.0
        elif((action, pos2) in actions_to_states["C"][0:5] and health1 == health2 and arrow1 == arrow2):
            p1 = 0.85
        # failed
        elif(pos2 == "E" and action not in ["SHOOT", "HIT"] and health1 == health2 and arrow1 == arrow2):
            p1 = 0.15
        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.5

                elif health2 == health1:  # Shit he missed

                    p1 = 0.5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == pos1) and arrow1 == arrow2:
            if(health2 == health1-50 or (health2 == 0 and health1 == 25)):  # Dem he did damage

                p1 = 0.1
            elif(health2 == health1):  # Shit nothing happened...

                p1 = 0.9

    if pos1 == "N" and health1 == health2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["N"][0:2] and arrow1 == arrow2 and mat1 == mat2):

            p1 = 0.85
        # failed
        elif(pos2 == "E" and action not in ["CRAFT"] and mat2 == mat1 and arrow1 == arrow2):
            p1 = 0.15

        elif(action == "CRAFT" and mat1 > 0 and mat2 == mat1 - 1 and pos1 == pos2):  # successfully crafting
            if arrow1 == 0:
                # 1 arrow crafted
                if(arrow2 == arrow1+1):
                    p1 = 0.5

                # 2 arrows crafted
                if(arrow2 == arrow1+2):
                    p1 = 0.35

                # 3 arrows crafted
                if(arrow2 == arrow1+3):
                    p1 = 0.15

            if arrow1 == 1:
                if arrow2 == 2 or arrow2 == 3:
                    p1 = 0.5

            if arrow1 == 2:
                if arrow2 == 3:
                    p1 = 1
            if arrow1 == 3 and arrow2 == 3:
                p1 = 1

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["S"][0:2] and mat1 == mat2):

            p1 = 0.85
        # failed
        elif(pos2 == "E" and action not in ["GATHER"] and mat2 == mat1):
            p1 = 0.15

        elif(action == "GATHER" and pos1 == pos2):
            # Successfully gathered material
            if mat1 == mat2 and mat1 == 2:
                p1 = 1
            elif mat1 == mat2-1:
                p1 = 0.75

            # failed
            elif mat1 == mat2:
                p1 = 0.25

    if pos1 == "E" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["E"][0:2] and health1 == health2 and arrow1 == arrow2):

            p1 = 1.0

        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.9

                elif health2 == health1:  # Shit he missed
                    p1 = 0.1

        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == pos1) and arrow1 == arrow2:
            if(health2 == health1-50 or (health2 == 0 and health1 == 25)):  # Dem he did damage

                p1 = 0.2

            elif(health2 == health1):  # Shit nothing happened...
                p1 = 0.8

    if pos1 == "W" and mat1 == mat2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["W"][0:2] and health1 == health2 and arrow1 == arrow2):

            p1 = 1.0
        elif(action == "SHOOT") and pos1 == pos2:  # Indiana decided to SHOOT
            if(arrow2 == arrow1-1):  # He shot
                if health2 == health1-25:  # Successful
                    p1 = 0.25

                elif health2 == health1:  # Shit he missed
                    p1 = 0.75

    return p1*p2


def R(from_state, action, to_state, actions_to_states):
    reward = 0
    pos1, mat1, arrow1, state1, health1 = from_state
    pos2, mat2, arrow2, state2, health2 = to_state

    if state1 == "R" and state2 == "D":
        if (pos1 == "C" or pos1 == "E") and (health1 >= health2 and health2 != 100):
            return 0
            # SHit he successfully did it...
        if (pos1 == "C" or pos1 == "E") and (arrow2 != 0):
            return 0
        if((health2 == health1+25 or (health1 == health2 and health2 == 100)) and (pos1 == "C" or pos1 == "E") and arrow2 == 0):
            if(pos1 == pos2 and mat1 == mat2):
                if (action == "SHOOT" and arrow1 == 0) or (action == "CRAFT" and mat1 == 0):
                    return 0
                else:
                    return -45
            else:
                return 0

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
                        reward = -5
                    else:
                        reward = -5
                elif health2 == health1:  # Shit he missed
                    reward = -5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == pos1) and arrow1 == arrow2:
            if(health2 == health1-50 or (health2 == 0 and health1 == 25)):  # Dem he did damage
                if health2 == 0:
                    reward = -5
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
            if arrow2 >= arrow1:
                reward = -5

    if pos1 == "S" and health1 == health2 and arrow1 == arrow2:
        # Successfully Moved
        if((action, pos2) in actions_to_states["S"][0:2] and mat1 == mat2):
            reward = -5
        # failed
        elif(pos2 == "E" and action not in ["GATHER"] and mat2 == mat1):
            reward = -5
        elif(action == "GATHER" and pos2 == pos1):
            # Successfully gathered material
            if mat1 == mat2 and mat1 == 2:
                reward = -5
            elif mat1 == mat2-1:
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
                        reward = -5
                    else:
                        reward = -5
                elif health2 == health1:  # Shit he missed
                    reward = -5
        # Oh he is gonna shoot...
        elif(action == "HIT") and (pos2 == pos1) and arrow1 == arrow2:
            if(health2 == health1-50 or (health2 == 0 and health1 == 25)):  # Dem he did damage
                if health2 == 0:
                    reward = -5
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
                        reward = -5
                    else:
                        reward = -5
                elif health2 == health1:  # Shit he missed
                    reward = -5
    return reward


def build_possible_actions(states, actions_to_states):
    possible_actions = {}
    total_actions = 0
    for from_state in states:
        pos1, mat1, arrow1, state1, health1 = from_state
        curr_actions = []
        valid_actions = []
        for i_state in actions_to_states[pos1]:
            valid_actions.append(i_state[0])
        valid_actions = set(valid_actions)
        for action in valid_actions:
            isValid = False
            for to_state in states:
                p = P(from_state, action, to_state, actions_to_states)
                if(p != 0):
                    isValid = True
            if isValid:
                curr_actions.append(action)
        if health1 == 0:
            curr_actions = ["NONE"]
        curr_actions.sort()
        possible_actions[from_state] = curr_actions
        total_actions += len(curr_actions)
    return possible_actions, total_actions


def construct_A(possible_actions, states, actions_to_states):
    A = []
    for to_state in states:
        temp = []
        for from_state in states:
            for action in possible_actions[from_state]:
                p = P(from_state, action, to_state, actions_to_states)
                if p != 0:
                    if from_state == to_state:
                        temp.append(1-p)
                    else:
                        temp.append(-p)
                elif from_state == to_state and from_state[-1] == 0 and action == "NONE":
                    temp.append(1)
                else:
                    temp.append(0)
        A.append(temp)
    return np.array(A)


def construct_R(possible_actions, states, actions_to_states):
    Reward = []
    for state in states:
        for action in possible_actions[state]:
            R_s_a = 0
            for to_state in states:
                p = P(state, action, to_state, actions_to_states)
                r = R(state, action, to_state, actions_to_states)
                R_s_a += (p*r)
            Reward.append(R_s_a)
    return np.array(Reward)


def get_optimal_policy(x, states, possible_actions):
    policy = []
    x_index = 0
    for i in range(len(states)):
        state = states[i]
        max_x_value_for_current_state = None
        best_action_for_current_state = None
        for j in range(len(possible_actions[state])):
            action = possible_actions[state][j]
            if max_x_value_for_current_state == None or (max_x_value_for_current_state != None and x[x_index] > max_x_value_for_current_state):
                max_x_value_for_current_state = x[x_index]
                best_action_for_current_state = action
            x_index += 1
        if best_action_for_current_state == None:
            best_action_for_current_state = "NONE"
        policy.append([state, best_action_for_current_state])
    return policy


def construct_alpha(states):
    alpha = [0 for pos in ["W", "N", "E", "S", "C"] for mat in range(
        3) for arrow in range(4) for state in ["D", "R"] for health in range(0, 120, 25)]
    alpha[states.index(("C", 2, 3, "R", 100))] = 1
    return np.expand_dims(np.array(alpha), axis=1)


def LP():
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
    actions = ["UP", "LEFT", "DOWN", "RIGHT",
               "STAY", "SHOOT", "HIT", "CRAFT", "GATHER", "NONE"]
    possible_actions, total_actions = build_possible_actions(
        states, actions_to_states)
    A = construct_A(possible_actions, states, actions_to_states)
    alpha = construct_alpha(states)
    Reward = construct_R(possible_actions, states, actions_to_states)
    x = cp.Variable(shape=(total_actions, 1), name='x')
    constraints = [cp.matmul(A, x) == alpha, x >= 0]
    objective = cp.Maximize(cp.matmul(Reward, x))
    problem = cp.Problem(objective, constraints)
    objective = problem.solve()
    x = x.value.reshape(len(x.value))
    optimal_policy = get_optimal_policy(x, states, possible_actions)
    final_output = {
        "a": A.tolist(),
        "r": Reward.tolist(),
        "alpha": np.squeeze(alpha).tolist(),
        "x": x.tolist(),
        "policy": optimal_policy,
        "objective": objective
    }
    with open("./outputs/part_3_output.json", "w") as f:
        json.dump(final_output, f)
    # for i in optimal_policy:
    #     print(i)


if not os.path.exists("./outputs"):
    os.mkdir("outputs")
LP()
