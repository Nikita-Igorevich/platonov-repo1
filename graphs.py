import numpy as np
import matplotlib.pyplot as plt

with open("settings.txt", "r") as settings:
    tmp = [float(i) for i in settings.read().split("\n")] #settings reading

data_array = np.loadtxt("data.txt", dtype=int) #data reading

voltage_array = tmp[0] * data_array #voltage and time axes
time_array = []
for i in range(len(voltage_array)):
    time_array.append(i*tmp[1])

fig, ax = plt.subplots(figsize=(16, 10), dpi = 400)
ax.plot(time_array, voltage_array, lw = 5, c = 'blue', marker = '^', markevery = 10, markersize = 15)

ax.set_xlim([min(time_array), max(time_array)]) #axes limits
ax.set_ylim([min(voltage_array), 1.05*max(voltage_array)])

plt.ylabel("Voltage, U") # axes
plt.xlabel("Time, t")
plt.title("RC cicuit graph", fontstyle = 'oblique')
plt.legend("U(t)")

plt.grid(b=True, which='major', color='grey', linestyle='-') #grid editing
plt.grid(b=True, which='minor', color='grey', linestyle='--')

print(tmp[1]*voltage_array.argmax())
plt.text(6.2, 2.3, "Charging time = 4.213", fontsize = 20)

plt.minorticks_on()
fig.savefig("test.svg")
plt.show()