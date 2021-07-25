import lmfit
import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import ExpressionModel


def get_fit(x, y):
    exponential = ExpressionModel("a * exp(b*x) + c", name="exponential")
    power_law = ExpressionModel("a * x**b + c", name="power_law")
    square = ExpressionModel("a * x**2 + b", name="square")
    linear = ExpressionModel("a * x + b", name="linear")

    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.plot(x, y, "+")
    ax.set_xlabel("Reference Temperature [°C]")
    ax.set_ylabel("AliExpress Temperature [°C]")

    functions = [linear]  # exponential

    for f in functions:
        result = f.fit(y, x=x, a=1, b=1, c=1)

        print(lmfit.report_fit(result))

        print(result.params.pretty_print())

        result.eval()

        ax.plot(x, result.best_fit, label=result.model.expr)

    ax.legend()


def best_fit(t_in):
    """

    :param t_in:
    :return:
    """
    return 0.9467 * t_in + 4.455


french_thermometer = np.array(
    [21, 38, 40, 43, 45, 48, 50, 52, 54, 56, 58, 62, 65, 67, 70, 72, 79, 82, 87, 90, 92, 94, 95, 97,
     99.5])

ali_thermometer = np.array(
    [24, 41, 43, 45, 47, 50, 52, 53, 56, 58, 59, 63, 65.5, 67.5, 70.5, 72, 79.5, 82, 88, 89.5, 91, 93, 94,
     96.5, 99.5])

# get_fit(french_thermometer, ali_thermometer)

t_ref = np.arange(120)
t_ali = best_fit(t_ref)


# Display temperature table
print(f"Desired temperature ; Displayed temperature")
for (ti, ta) in zip(t_ref, t_ali):
    print(f"{ti:.0f} ; {ta:.1f}")

fig, ax = plt.subplots(figsize=(10, 7.5))
ax.plot(t_ref, t_ref-t_ali)
ax.set_xlabel("Reference Temperature [°C]")
ax.set_ylabel("Delta Temperature (ref-ali) [°C]")
ax.xaxis.grid(True, which='minor', color='#000000', linestyle=':')
ax.yaxis.grid(True, which='minor', color='#000000', linestyle=':')
ax.xaxis.grid(True, which='major', color='#000000', linestyle='--')
ax.yaxis.grid(True, which='major', color='#000000', linestyle='--')
plt.show()
