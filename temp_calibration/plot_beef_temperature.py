import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import ExpressionModel

exponential = ExpressionModel("a * exp(b*x) + c", name="exponential")
power_law = ExpressionModel("a * x**b + c", name="power_law")
square = ExpressionModel("a * x**2 + b", name="square")
linear = ExpressionModel("a * x + b", name="linear")

temperature = np.array([53, 55, 57, 58, 59, 60, 61])
time = np.array([0, 60, 95, 117, 126, 137, 145])

fig, ax = plt.subplots(figsize=(10, 7.5))
ax.plot(time, temperature, "+")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Temperature [°C]")

functions = [power_law, square] # exponential

for f in functions:
    result = f.fit(temperature, x=time, a=1, b=1, c=1)

    print(result.fit_report())

    ax.plot(time, result.best_fit, label=f.name)

ax.legend()
plt.show()
