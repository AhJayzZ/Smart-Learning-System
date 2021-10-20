import configparser


def create_new_conf_file(file_path, dict_to_write):
    config = configparser.ConfigParser()

    for entry in dict_to_write:
        config[entry] = dict_to_write[entry]

    with open(file_path, 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    file_path = "conf.cfg"

    dict_to_write = {
        "APP": {
            "VERSION": "0.0.1",
            "DEBUG": "TRUE"
        },
        "USER": {
            "NAME": "WAI",
            "HANDEDNESS": "left",
            "MODE": "0",
            "CAMERA": "0"
        },
        "hand_recognition": {
            "min_detection_confidence": "0.5",
            "min_tracking_confidence": "0.5"
        },
    }

    create_new_conf_file(file_path, dict_to_write)
