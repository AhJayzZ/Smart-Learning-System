from recognition_program import recognition_program


def main_recognition():
    try:
        """from timeit import Timer
        t = Timer("Recognition = recognition_program()",
                  "from main_recognition import recognition_program")
        print(t.timeit())
        # 20210915 last test: 1.5569038999999982
        """
        Recognition = recognition_program()
        Recognition.run()
        return Recognition.text

    except:
        assert 0, "main_recognition failed"
        pass


if __name__ == "__main__":
    text = main_recognition()
    print("result: [\n%r\n]" % text)
