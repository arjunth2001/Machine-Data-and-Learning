import numpy as np
states = 8  # Edited to 8 from 9 as we have 8 states..
ac = 5
disc = 0.5
call = 2  # 0="off", 1="on"

tstay = 0.6
tmove = 0.1
RollNumber = 2019111009
LastFourDigitsOfRollNumber = 1009
# Agent probabilities
x = 1 - (((LastFourDigitsOfRollNumber) % 30 + 1) / 100)
reward = RollNumber % 90 + 10
cost = -1


def comp_to_num(a, t, c):
    num = a*16+t*2+c
    return num


def num_to_comp(num):
    c = num % 2
    t = (int(num/2)) % 8
    a = (int(num/16)) % 8
    return a, t, c


def check_call(k1, k2, i1, j1):

    switch_on = 0.5
    turn_off = 0.1
    nothing = 0.4

    if(i1 == j1):
        if(k1 == 0 and k2 == 1):
            pr_call = switch_on
        elif(k1 == 0 and k2 == 0):
            pr_call = nothing+turn_off
        elif(k1 == 1 and k2 == 0):
            pr_call = 1
        elif(k1 == 1 and k2 == 1):
            pr_call = 0
    else:
        if(k1 == 0 and k2 == 1):
            pr_call = switch_on
        elif(k1 == 0 and k2 == 0):
            pr_call = nothing+turn_off
        elif(k1 == 1 and k2 == 0):
            pr_call = turn_off
        elif(k1 == 1 and k2 == 1):
            pr_call = switch_on+nothing
    return pr_call


def calc_target_prob(x1, y1, x2, y2):
    t_prob = 0

    if (((y1 == y2) and ((x1 == x2) and (x1 == 3 or x1 == 0))) and ((x1 == x2) and ((y1 == y2) and (y1 == 1 or y1 == 0)))):
        t_prob = tstay+tmove+tmove
    elif((y1 == y2) and ((x1 == x2) and (x1 == 3 or x1 == 0))):
        t_prob = tstay+tmove
    elif ((x1 == x2) and ((y1 == y2) and (y1 == 1 or y1 == 0))):
        t_prob = tstay + tmove
    elif((x1 == x2) and (y1 == y2)):
        t_prob = tstay
    elif ((x2 == x1+1 or x2 == x1-1) and y1 == y2):
        t_prob = tmove
    elif ((y2 == y1+1 or y2 == y1-1) and x1 == x2):
        t_prob = tmove
    return t_prob


def stay(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2):
    pr_agent = 0

    # stays in the same state
    if(x1a == x2a and y1a == y2a):
        pr_agent = 1
    return pr_agent


def right(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2):
    pr_agent = 0

    # for agent
    if(y2a != y1a):
        pr_agent = 0
    elif((x2a == x1a+1) or (x2a == x1a and x2a == 3)):
        pr_agent = x
    elif((x2a == x1a - 1) or (x2a == x1a and x2a == 0)):
        pr_agent = 1-x
    return pr_agent


def left(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2):
    pr_agent = 0

    # for agent
    if(y2a != y1a):
        pr_agent = 0
    elif((x2a == x1a-1) or (x2a == x1a and x2a == 0)):
        pr_agent = x
    elif((x2a == x1a + 1) or (x2a == x1a and x2a == 3)):
        pr_agent = 1-x
    return pr_agent


def up(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2):
    pr_agent = 0

    # for agent
    if(x2a != x1a):
        pr_agent = 0
    elif((y2a == y1a+1) or (y2a == y1a and y2a == 1)):
        pr_agent = x
    elif((y2a == y1a - 1) or (y2a == y1a and y2a == 0)):
        pr_agent = 1-x
    return pr_agent


def down(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2):
    pr_agent = 0

    # for agent
    if(x2a != x1a):
        pr_agent = 0
    elif((y2a == y1a-1) or (y2a == y1a and y2a == 0)):
        pr_agent = x
    elif((y2a == y1a + 1) or (y2a == y1a and y2a == 1)):
        pr_agent = 1-x
    return pr_agent


def calc_trans_prob(i1, j1, k1, a, i2, j2, k2):

    x1a = i1 % 4
    y1a = int(i1/4)
    x2a = i2 % 4
    y2a = int(i2/4)

    x1t = j1 % 4
    y1t = int(j1/4)
    x2t = j2 % 4
    y2t = int(j2/4)

    # print("Calculating for (", x1a,y1a,") and (", x2a, y2a,")")
    # print("Calculating for (", x1t,y1t,") tnd (", x2t, y2t,")")

    if(a == 0):  # action: stay
        pr_agent = stay(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2)
    elif(a == 1):  # action: right
        pr_agent = up(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2)
    elif(a == 2):  # action: left
        pr_agent = down(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2)
    elif(a == 3):  # action: up
        pr_agent = left(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2)
    elif(a == 4):  # action: down
        pr_agent = right(x1a, y1a, x1t, y1t, k1, a, x2a, y2a, x2t, y2t, k2)

    # calc target prob
    pr_target = calc_target_prob(x1t, y1t, x2t, y2t)

    # check call value
    pr_call = check_call(k1, k2, i1, j1)

    # print("pr_agent = ", pr_agent)
    # print("pr_target = ", pr_target)
    # print("pr_call = ", pr_call)

    # calculate probability
    prob = (pr_agent)*(pr_target)*(pr_call)

    return prob


def calc_obs_prob(i1, j1, k1):
    x1a = i1 % 4
    y1a = int(i1/4)

    x1t = j1 % 4
    y1t = int(j1/4)

    if(x1a == x1t and y1a == y1t):
        return "o1"
    elif(x1t == x1a+1 and y1t == y1a):
        return "o2"
    elif (y1t == y1a - 1 and x1a == x1t):
        return "o3"
    elif (x1t == x1a-1 and y1a == y1t):
        return "o4"
    elif (y1t == y1a + 1 and x1a == x1t):
        return "o5"
    else:
        return "o6"


def calc_reward(i1, j1, k1, a):

    r = 0
    if(i1 == j1 and k1 == 1):
        r += reward

    if(a != 0):
        r += cost
    return r


def gen_transition():
    # from : agent states
    for i1 in range(states):
        # from : target states
        for j1 in range(states):
            # from : call status
            for k1 in range(call):
                # actions
                for a in range(ac):
                    # sum=0
                    # print("-----------------------------------------------------------------------------")
                    # to : agent states
                    for i2 in range(states):
                        # to : target states
                        for j2 in range(states):
                            # to : call status
                            for k2 in range(call):

                                tp = calc_trans_prob(i1, j1, k1, a, i2, j2, k2)
                                start_state = comp_to_num(i1, j1, k1)
                                end_state = comp_to_num(i2, j2, k2)

                                # T: <action> : <start-state> : <end-state> %f
                                if(tp != 0):
                                    print("T:", a, ":", start_state,
                                          ":", end_state, tp)
                                # print()
                                # sum += tp
                    # print("SUM = ",sum,"\n")


def gen_observation():
    # from : agent states
    for i1 in range(states):
        # from : target states
        for j1 in range(states):
            # from : call status
            for k1 in range(call):

                obs = calc_obs_prob(i1, j1, k1)
                end_state = comp_to_num(i1, j1, k1)

                # O : <action> : <end-state> : <observation> %f
                print("O :", "*", ":", end_state, ":", obs, 1)


def gen_rewards():
    # from : agent states
    for i1 in range(states):
        # from : target states
        for j1 in range(states):
            # from : call status
            for k1 in range(call):
                for a in range(ac):
                    r = calc_reward(i1, j1, k1, a)
                    end_state = comp_to_num(i1, j1, k1)

                    # R: <action> : <start-state> : <end-state> : <observation> %f
                    print("R:", a, ": * :", end_state, ": *", r)


def gen_start_states1():

    s = []
    s.append(comp_to_num(1, 4, 0))
    s.append(comp_to_num(2, 4, 0))
    s.append(comp_to_num(3, 4, 0))
    s.append(comp_to_num(6, 4, 0))
    s.append(comp_to_num(7, 4, 0))
    s.append(comp_to_num(1, 4, 1))
    s.append(comp_to_num(2, 4, 1))
    s.append(comp_to_num(3, 4, 1))
    s.append(comp_to_num(6, 4, 1))
    s.append(comp_to_num(7, 4, 1))
    print("start include:", s[0], s[1], s[2],
          s[3], s[4], s[5], s[6], s[7], s[8], s[9])


def gen_start_states2():

    s = []
    s.append(comp_to_num(5, 1, 0))
    s.append(comp_to_num(5, 4, 0))
    s.append(comp_to_num(5, 5, 0))
    s.append(comp_to_num(5, 6, 0))

    # start include: 1 3
    print("start include:", s[0], s[1], s[2], s[3])


def gen_start_states4():

    print("start: ", end='')
    for i in range(128):
        pr_a = 0
        pr_t = 0
        pr_c = 0.5

        a, t, c = num_to_comp(i)
        if(a == 0):
            pr_a = 0.4
        elif(a == 7):
            pr_a = 0.6

        if(t == 1 or t == 2 or t == 5 or t == 6):
            pr_t = 0.25

        pr = pr_a*pr_c*pr_t
        print(pr, end=' ')


def main():

    # discount: %f
    # values: [ reward, cost ]
    # states: [ %d, <list of states> ]
    # actions: [ %d, <list of actions> ]
    # observations: [ %d, <list of observations> ]

    print("discount:", disc)
    print("values: reward")
    print("states:", 128)
    print("actions:", 5)
    print("observations: o1 o2 o3 o4 o5 o6")
    print()
    gen_start_states1()
    # gen_start_states2()
    # gen_start_states4()
    print()
    gen_transition()
    print()
    gen_observation()
    print()
    gen_rewards()


main()
