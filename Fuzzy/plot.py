import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import deFuzzy_test

NumberOfVehicles_value = deFuzzy_test.NumberOfVehicles_value
Queue_value = deFuzzy_test.Queue_value
output = deFuzzy_test.output
temp = 0

plt.figure(figsize=(8, 8))
plt.subplot(3, 1, 1)
plt.plot(NumberOfVehicles_value)
plt.xticks(ticks=np.arange(1, 11))

for i in NumberOfVehicles_value:
    plt.text(temp, i + 0.5, str(i), horizontalalignment = 'center', color = 'green')
    temp += 1

plt.xlabel("Numbers of vehicles")

plt.subplot(3, 1, 2)
plt.plot(Queue_value)
plt.xticks(ticks=np.arange(1, 11))
temp = 0
for i in Queue_value:
    plt.text(temp, i + 0.5, str(i), horizontalalignment = 'center', color = 'green')
    temp += 1
plt.xlabel("queue")

plt.subplot(3, 1, 3)
plt.plot(output)
plt.xticks(ticks=np.arange(1, 11))
temp = 0
for i in output:
    plt.text(temp, i + 0.5, str(i) + "s", horizontalalignment = 'center', color = 'green')
    temp += 1
plt.show()

