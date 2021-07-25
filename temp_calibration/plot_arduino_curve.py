"""
Designed to plot temperature curve extracted from serial
"""
import re
import matplotlib.pyplot as plt
import numpy as np

def read_data(filemame):
    """
    Read data from file.

    :param str filemame:
    :return: time, temperature
    """

    obj = open(filemame, "r")

    lines = obj.readlines()

    pattern = "Uptime: ([0-9]+) s ; Current temperature: ([0-9.]+)"

    times = []
    temperatures = []
    for line in lines:
        match = re.search(pattern, line)
        time = float(match.group(1))
        temperature = float(match.group(2))

        times.append(time)
        temperatures.append(temperature)

    times = np.asarray(times)
    temperatures = np.asarray(temperatures)

    correct_t = correct_temperatures(temperatures)

    return times, temperatures, correct_t


def correct_temperatures(input_t):
    """

    :param input_t:
    :return:
    """
    # temperature measured
    RawHigh = 97.81
    RawLow = 0.06

    # Actual temperature
    ReferenceHigh = 99.7
    ReferenceLow = 0

    temp_slope = (ReferenceHigh - ReferenceLow) / (RawHigh - RawLow)
    temp_zeropoint = ReferenceHigh - temp_slope * RawHigh

    corrected_t = temp_slope * input_t + temp_zeropoint

    return corrected_t

filename = "cold_to_room.dat"
filename = "idle_temp.dat"
filename = "idle_temp2.dat"

time, temperature, correct_t = read_data(filename)



fig, ax = plt.subplots(figsize=(10,7.5))
ax.plot(time, temperature, label="Raw Temperature")
ax.plot(time, correct_t, label="Corrected Temperature")

ax.set_xlabel("Time [s]")
ax.set_ylabel("Temperature [°C]")
ax.legend()
fig.suptitle("Arduino temperature profile with DS18B20 sensor")

fig.savefig("arduino_temp.pdf")

plt.show()

# Calibration eau du robinet
# Reference ; Capteur arduino soudé ; sonde température chocolat ; Pistolet infrarouge
# 0.0       ; 1.6                   ; 1.2                        ; 1.2
# 99.7      ; 98.9                 ; 106                         ; 90
#
# Calibration eau déminéralisée
# Reference ; Capteur arduino soudé ; sonde température chocolat ; Pistolet infrarouge
# 0.0       ; 0.06                  ; -0.3                       ; 1.1
# 99.7      ; 97.81                 ; 100.7                      ; 87.6