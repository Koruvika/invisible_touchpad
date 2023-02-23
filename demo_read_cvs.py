import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data_dir = "D:/pythonProject/bach_khoa/pbl5/data/press/7.csv"
    data = pd.read_csv(data_dir)
    data = np.array(data, dtype=np.float64)
    data = data.reshape(-1, 6)
    ax = data[:, 0]
    ay = data[:, 1]
    az = data[:, 2]
    gx = data[:, 3]
    gy = data[:, 4]
    gz = data[:, 5]
    plt.plot(ax, label="ax")
    plt.plot(ay, label="ay")
    plt.plot(az, label="az")
    plt.plot(gx, label="gx")
    plt.plot(gy, label="gy")
    plt.plot(gz, label="gz")
    plt.legend()
    plt.show()
    print("Debug...")
