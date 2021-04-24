import matplotlib.pyplot as plt

# Abhishek Bapna
# 2018A7PS0184H
# Ashna Swaika 
# 2018A7PS0027H
# Siddhant Kulkarni 
# 2018A7PS0185H
# Sravani Garapati 
# 2018A7PS0097H
# Vikram S Haritas
#  2018A7PS0302H

x1 = [0, 20, 40, 60, 80, 90]
loss = [2.89, 2.18, 2.08, 2.03, 0.774638671, 0.157646484]
for i in range(len(loss)):
    loss[i] *= 8
corrupt = [3.05, 2.83, 2.68, 2.3, 1.05, 0.376933593]
for i in range(len(corrupt)):
    corrupt[i] *= 8
delay = [3604.48, 1433.6, 762.53, 520.71, 386.59, 313.44]
for i in range(len(delay)):
    delay[i] /= 1024
    delay[i] *= 8
x2 = [0, 50, 100, 150, 200, 250]
plt.plot(x1, loss)
plt.title("Transfer Speed (mbps) vs Loss (%)")
plt.show()
plt.plot(x1, corrupt)
plt.title("Transfer Speed (mbps) vs Corruption (%)")
plt.show()
plt.plot(x2, delay)
plt.title("Transfer Speed (mbps) vs Delay (ms)")
plt.show()