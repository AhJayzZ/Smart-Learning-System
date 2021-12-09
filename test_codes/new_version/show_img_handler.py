import cv2


class edit_img:
    def put_text(img, str_show_text, text_color=(0, 255, 255)):
        cv2.putText(img, str_show_text, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    def draw_point(img, position, point_color=(0, 0, 255), point_radius=3):
        point = (position.x, position.y)
        point_thickness = -1  # whole point fill in point_color

        cv2.circle(
            img, point, radius=point_radius, color=point_color, thickness=point_thickness)

    def draw_frame(img, position_start, position_end, frame_color=(255, 105, 65), frame_thickness=2):
        p1 = (position_start.x, position_start.y)
        p2 = (position_end.x, position_end.y)

        cv2.rectangle(img, p1, p2, color=frame_color,
                      thickness=frame_thickness)


def ajust_brightness(self, brightness):
    self._brightness = brightness


def ajust_contrast(self, contrast):
    self._contrast = contrast


_brightness = 0
_contrast = 1
