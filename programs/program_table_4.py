from .utils import *
import math
import os
from .label_config import max_param, max_step
from misc import get_distance_to_center

###################################
# generate tables with "thick" supports
# tabletop can be: circle, square, rectangle
# supports can be: circle, square
# max steps: 2
###################################


def generate_single(d):

    data = np.zeros((32, 32, 32), dtype=np.uint8)
    steps = []

    # sample tabletop thickness
    p = np.random.rand()
    if p < 0.8:
        top_t = np.random.randint(1, 3)
    else:
        top_t = np.random.randint(3, 4)
    # sample bottom base thickness
    p = np.random.rand()
    if p < 0.75:
        base_h = 1
    else:
        base_h = 2
    # sample support height
    p = np.random.rand()
    if p < 0.7:
        support_h = 2 * np.random.randint(8, 13) - top_t
    else:
        support_h = 2 * np.random.randint(5, 13) - top_t

    total_height = support_h + top_t
    base_start = - int(total_height / 2)
    support_start = base_start
    tabletop_start = support_start + support_h

    # sample the tabletop
    p = np.random.rand()
    top_type = -1
    if p < 0.25:
        # rectangle tabletop
        top_r1 = np.random.randint(8, 13)
        top_r2 = np.random.randint(11, 13)
        if top_r1 > top_r2:
            tmp = top_r1
            top_r1 = top_r2
            top_r2 = tmp
        if top_r1 == top_r2:
            top_r1 -= 1
        top_r = min(top_r1, top_r2)
        data, step = draw_rectangle_top(data, tabletop_start, 0, 0, top_t, top_r1, top_r2)
        steps.append(step)
        top_type = 0
    elif p < 0.55:
        # square tabletop
        q = np.random.rand()
        if q < 0.75:
            top_r = np.random.randint(11, 13)
        elif q < 0.9:
            top_r = np.random.randint(9, 11)
        else:
            top_r = np.random.randint(8, 9)
        data, step = draw_square_top(data, tabletop_start, 0, 0, top_t, top_r)
        steps.append(step)
        top_type = 1
    else:
        # circle tabletop
        q = np.random.rand()
        if q < 0.75:
            top_r = np.random.randint(11, 13)
        elif q < 0.9:
            top_r = np.random.randint(9, 11)
        else:
            top_r = np.random.randint(8, 9)
        data, step = draw_circle_top(data, tabletop_start, 0, 0, top_t, top_r)
        steps.append(step)
        top_type = 2

    # sample supports
    p = np.random.rand()
    if p < 0.65:
        # sample circle support
        q = np.random.rand()
        if q < 0.7:
            support_r = np.random.randint(5, 7)
        else:
            support_r = np.random.randint(3, min(9, top_r))
        data, step = draw_circle_support(data, support_start, 0, 0, support_h+top_t, support_r)
        steps.append(step)
    else:
        # sample square support
        q = np.random.rand()
        if q < 0.7:
            support_r = np.random.randint(4, 6)
        else:
            support_r = np.random.randint(3, min(8, top_r))
        if top_type == 2:
            support_r = min(int(top_r*math.sqrt(2)/2), support_r)
        data, step = draw_square_support(data, support_start, 0, 0, support_h+top_t, support_r)
        steps.append(step)

    return data, steps


def generate_batch(num):
    data = np.zeros((num, 32, 32, 32), dtype=np.uint8)
    label = np.zeros((num, max_step, max_param), dtype=np.int32)

    d = get_distance_to_center()

    for i in range(num):
        x, y = generate_single(d)
        data[i, ...] = x

        for k1 in range(len(y)):
            label[i, k1, 0:len(y[k1])] = y[k1]

    return data, label


def check_max_steps():

    d = get_distance_to_center()

    step = 0
    for i in range(200):
        x, y = generate_single(d)
        if len(y) > step:
            step = len(y)
    print("Maximum Steps: " + str(step) + " " + os.path.basename(__file__))

    return step

