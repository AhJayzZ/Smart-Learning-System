"""
pocessing of the croped img, to be easier to recognition

"""

import cv2


def cropped_img_handler(crop_img):
    try:
        crop_img_new = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)

        crop_img_new.flags.writeable = True

        crop_img_new = cv2.medianBlur(crop_img_new, 3)  # 除噪(降低邊緣雜訊)
        crop_img_new = cv2.adaptiveThreshold(
            crop_img_new, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)    # 自適應二值化
        #crop_img_new = cv2.medianBlur(crop_img_new, 3)

        crop_img_new.flags.writeable = False
        cv2.imshow("new crop", crop_img_new)
        return crop_img_new

    except:
        pass
