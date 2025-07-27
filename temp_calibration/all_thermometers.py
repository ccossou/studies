import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import lmfit
from lmfit.models import ExpressionModel

filename = "E:/Dropbox/calibration_temperature.csv"

def read_temperatures(filename):
    """
    Read temperature when all row do not necessarily apply to all columns
    :param filename:
    :return:
    """
    DELIMITER = ";"

    obj = open(filename, "r", encoding="utf-8")
    lines = obj.readlines()
    obj.close()

    # Read header
    header = lines.pop(0)

    col_names = header[:-1].split(DELIMITER)
    temp_names = col_names[1:]
    nb_cols = len(col_names)
    nb_temp = nb_cols - 1


    times = []
    temperatures = []
    for i in range(nb_temp):
        times.append([])
        temperatures.append([])
    # times = [[]] * nb_temp
    # temperatures = [[]] * nb_temp


    t0 = None
    for line in lines:
        # Get rid of the \m character before the split to ensure "if ti" works properly
        elements = line[:-1].split(DELIMITER)

        time_i = float(elements[0])

        # t0 is the first time
        if t0 is None:
            t0 = time_i


        for i in range(nb_temp):
            ti = elements[i+1]
            if ti:
                times[i].append(time_i)
                temperatures[i].append(float(ti))

    times = [np.asarray(ti) - t0 for ti in times]
    temperatures = [np.asarray(ti) for ti in temperatures]

    return temp_names, times, temperatures


def interpolate_data(xs, ys):
    """
    Make sure that all sub lists are interpolated over the same x values
    By default, out_x will be all combined x values

    :param xs: All i-elements of x and y must have the same length, be i and j can have different length
    :type xs: list(np.array)
    :param ys:
    :type ys: list(np.array)
    :return:
    """

    out_x = np.concatenate(xs)
    out_x = np.asarray(list(set(out_x)))
    out_x.sort()

    out_ys = []
    for x, y in zip(xs, ys):
        interp = interpolate.interp1d(x, y, fill_value="extrapolate")

        out_ys.append(interp(out_x))

    return out_x, out_ys


def get_fit(x, ys, names, fig=None):
    # model = ExpressionModel("a * exp(b*x) + c", name="exponential")
    # model = ExpressionModel("a * x**b + c", name="power_law")
    # model = ExpressionModel("a * x**2 + b", name="square")
    model = ExpressionModel("a * x + b", name="linear")

    # source: https://matplotlib.org/stable/gallery/color/named_colors.html
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan", ]


    if fig is None:
        fig, ax = plt.subplots(figsize=(10, 7.5))
        pstyle = "+"
    else:
        ax = fig.axes[0]
        nb_previous_items = len(ax.lines)
        colors = colors[nb_previous_items:]
        pstyle = "*"

    ax.set_xlabel("Reference Temperature [°C]")
    ax.set_ylabel("Thermometer Temperature [°C]")

    for y, name, color in zip(ys, names, colors):
        ax.plot(x, y, pstyle, color=color, label=name)
        result = model.fit(y, x=x, a=1, b=1, c=1)

        print(f"For {name}:")
        print(lmfit.report_fit(result))

        print(result.params.pretty_print())

        result.eval()

        ax.plot(x, result.best_fit, color=color, label=result.model.expr)

    ax.legend()

    return fig


names, r_times, r_temperatures = read_temperatures(filename)
# time, ref_t, t200, t1, t2, t3 = np.loadtxt(filename, skiprows=1, dtype=float, delimiter=";", unpack=True)

times, temperatures = interpolate_data(r_times, r_temperatures)



fig, ax = plt.subplots(figsize=(10, 7.5))

for (ni, tempi) in zip(names, temperatures):
    ax.plot(times, tempi, "+", label=ni)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Temperature [°C]")
ax.xaxis.grid(True, which='minor', color='#000000', linestyle=':')
ax.yaxis.grid(True, which='minor', color='#000000', linestyle=':')
ax.xaxis.grid(True, which='major', color='#000000', linestyle='--')
ax.yaxis.grid(True, which='major', color='#000000', linestyle='--')
ax.legend()

fig2, ax2 = plt.subplots(figsize=(10, 7.5))

reft = temperatures[0]

fig3 = get_fit(reft, temperatures[1:], names[1:])

french_thermometer = np.array(
    [21, 38, 40, 43, 45, 48, 50, 52, 54, 56, 58, 62, 65, 67, 70, 72, 79, 82, 87, 90, 92, 94, 95, 97,
     99.5])

ali_thermometer = np.array(
    [24, 41, 43, 45, 47, 50, 52, 53, 56, 58, 59, 63, 65.5, 67.5, 70.5, 72, 79.5, 82, 88, 89.5, 91, 93, 94,
     96.5, 99.5])
get_fit(french_thermometer, [ali_thermometer], ["T1_orig"], fig=fig3)

for (ni, tempi) in zip(names[1:], temperatures[1:]):
    ax2.plot(reft, tempi, label=ni)
ax2.set_xlabel("Reference Temperature [°C]")
ax2.set_ylabel("Temperature [°C]")
ax2.xaxis.grid(True, which='minor', color='#000000', linestyle=':')
ax2.yaxis.grid(True, which='minor', color='#000000', linestyle=':')
ax2.xaxis.grid(True, which='major', color='#000000', linestyle='--')
ax2.yaxis.grid(True, which='major', color='#000000', linestyle='--')
ax2.legend()
plt.show()

print("")