import random
from configparser import ConfigParser


if __name__ == "__main__":
    config = ConfigParser()
    config.read("cfg.ini")
    W, H = int(config["DEFAULT"]["width"]),int(config["DEFAULT"]["height"])
    MARGIN = int(config["DEFAULT"]["margin"])
    N = int(config["DEFAULT"]["n"])
    with open("points.txt", 'w') as f:
        for i in range(N):
            x = random.randint(MARGIN, W-MARGIN)
            y = random.randint(MARGIN, H-MARGIN)
            f.writelines(f"{x},{y}\n")
    print("Points Generated")
