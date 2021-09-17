def update_ROI_position(image, index_finger_point):
    """
        Args: 
            image,
            index_finger_point, xy point of index finger from mediapipe in image now

        Raises: -

        Returns:
            [position_x_final, position_y_final]
    """
    position_x = int(index_finger_point.x*float(image.shape[1]))
    position_y = int(index_finger_point.y*float(image.shape[0]))

    return position_x, position_y


def get_ROI_position(image, position_initial, position_final):
    """
        Args: 
            image,
            position_initial[2], xy point of  index finger from mediapipe in image from start
            index_finger_point[2], xy point of index finger from mediapipe in image now

        Raises: -

        Returns:
            [position_x_final, position_y_final]
    """
    position_x_initial = position_initial.x
    position_y_initial = position_initial.y

    position_x_final = position_final.x
    position_y_final = position_final.y

    # do_ROI_reposition()
    temp = 0
    if position_x_initial > position_x_final:
        position_x_initial, position_x_final = position_x_final, position_x_initial
    if (position_y_initial > position_y_final):
        position_y_initial, position_y_final = position_y_final, position_y_initial

    return position_x_initial, position_y_initial, position_x_final, position_y_final
