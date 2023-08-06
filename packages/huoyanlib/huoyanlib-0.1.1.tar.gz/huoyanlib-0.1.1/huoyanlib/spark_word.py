from xingyunlib.pygame_set import clear_os
colors = [31, 32, 33, 34, 35, 36, 37, 91, 92, 93, 94, 95, 96, 97]


def spark(word):
    import random
    import time
    for i in range(25):
        print("\033[{}m{}".format(random.choice(colors), word))
        time.sleep(0.1)
        clear_os()


def spark_2(word):
    import random
    import os
    import time
    p = []
    for i in range(len(word)):
        p.append(word[i:i+1])
    for i in range(25):
        for s in range(1, len(p) + 1):
            for z in p:
                print("\033[{}m{}".format(random.choice(colors), z), end='')
                time.sleep(0.1)
            clear_os()

