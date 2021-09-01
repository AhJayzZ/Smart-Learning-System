import cv2
import STATE


def show_ROI_handler(
        image,
        state_recognition,
        list_position):
    position_x_initial = list_position[0]
    position_y_initial = list_position[1]
    position_x_final = list_position[2]
    position_y_final = list_position[3]
    if (state_recognition == STATE.START_CROP):
        position_x_initial = int(list[3*8]*float(image.shape[1]))
        position_y_initial = int(list[3*8+1]*float(image.shape[0]))
    elif (state_recognition == STATE.CROPPING):
        position_x_now = int(list[3*8]*float(image.shape[1]))
        position_y_now = int(list[3*8+1]*float(image.shape[0]))

        cv2.rectangle(image, (position_x_initial, position_y_initial),
                      (position_x_now, position_y_now), (255, 105, 65), 2)
    elif (state_recognition == STATE.END_CROP):
        position_x_final = int(list[3*8]*float(image.shape[1]))
        position_y_final = int(list[3*8+1]*float(image.shape[0]))
    elif (state_recognition == STATE.GET_IMAGE):
        if (position_y_initial > position_y_final):
            position_y_initial, position_y_final = position_y_final, position_y_initial
        if position_x_initial > position_x_final:
            position_x_initial, position_x_final = position_x_final, position_x_initial

    return [[position_x_initial, position_y_initial], [position_x_final, position_y_final]]
