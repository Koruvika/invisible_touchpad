import pandas as pd
import serial
import os
from tqdm import tqdm

data_dir = "D:/pythonProject/bach_khoa/pbl5/data"
data_func = pd.Series({
    0: "click",
    1: "begin",
    2: "end",
    3: "press",
    4: "drop"
})
data_keyboard = pd.Series({
    0: "q",
    1: "w",
    2: "e",
    3: "r",
    4: "t"
})
data_classes = pd.DataFrame(
    {
        "function": data_func,
        "keyboard": data_keyboard
    }
)


def get_data(arduino_port="COM4", baud=38400, keyboard=None, samples=2000):
    print(keyboard)
    if keyboard is None:
        print("Please press any keyboard")
        return

    # get class to collect and create suitable file in this class folder
    func = data_classes[data_classes["keyboard"].str.match(keyboard)]["function"].iloc[0]
    path_dir = data_dir + "/" + func
    n = len(os.listdir(path_dir))
    print(f"Have {n} files in class {func}")
    filename = f"{path_dir}/{n+1}.csv"
    file = open(filename, "a")

    # init Serial reader
    ser = serial.Serial(arduino_port, baud)
    print("Connected to Serial: " + arduino_port)

    # get data
    for i in tqdm(range(samples)):
        getData = ser.readline()
        dataString = getData.decode('utf-8')
        data = dataString[0:][:-2]
        file.write(data)
        file.write("\n")
    file.close()
    print(f"Have {len(os.listdir(path_dir))} files in class {func}")


