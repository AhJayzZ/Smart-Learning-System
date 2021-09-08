'''input: 
        image,
        state_recognition,
        list_position[4]:[position_x_initial, position_y_initial, position_x_final, position_y_final]
    output:
        [position_x_initial, position_y_initial, position_x_final, position_y_final]
'''

import STATE


def ROI_bound_handler(
        image,
        state_recognition,
        list_position,
        list):
    if (state_recognition == STATE.START_CROP):
        position_x_initial = int(list[3*8]*float(image.shape[1]))
        position_y_initial = int(list[3*8+1]*float(image.shape[0]))
        position_x_final = position_x_initial
        position_y_final = position_y_initial

    elif (state_recognition == STATE.CROPPING):
        position_x_initial = list_position[0]
        position_y_initial = list_position[1]
        position_x_final = int(list[3*8]*float(image.shape[1]))
        position_y_final = int(list[3*8+1]*float(image.shape[0]))

    elif (state_recognition == STATE.END_CROP):
        position_x_initial = list_position[0]
        position_y_initial = list_position[1]
        position_x_final = int(list[3*8]*float(image.shape[1]))
        position_y_final = int(list[3*8+1]*float(image.shape[0]))
        if position_x_initial > position_x_final:
            position_x_initial, position_x_final = position_x_final, position_x_initial
        if (position_y_initial > position_y_final):
            position_y_initial, position_y_final = position_y_final, position_y_initial

    else:
        position_x_initial = 0
        position_y_initial = 0
        position_x_final = 0
        position_y_final = 0

    return position_x_initial, position_y_initial, position_x_final, position_y_final
