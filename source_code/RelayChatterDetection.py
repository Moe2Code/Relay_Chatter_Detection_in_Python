import matplotlib.pyplot as plt

relay_data = open("relay_data.txt", "r")

rd_time = []
rd_value = []


for relay_pt in relay_data.readlines():
    rd_time.append(float(relay_pt.split()[0]))
    rd_value.append(float(relay_pt.split()[1]))

print(rd_time)
print(rd_value)

UL = 4.5

plt.plot(rd_time, rd_value, "-g", label="Contacts Signal")
plt.plot(rd_time, [UL]*len(rd_value), "-r", label="Chatter Threshold")
plt.legend()
plt.suptitle("Relay Contacts- Full Signal")
plt.xlabel("Time [sec]")
plt.ylabel("Relay Contacts Signal [V]")
plt.savefig("Relay Contacts- Full Signal.png")
plt.show()

UL_crossed = False
chatter_indices = []
chatter_instances = []
i = 0

if rd_value[0] <= UL:
    sig_init_wrong = True
else:
    sig_init_wrong = False

for value in rd_value:
    if sig_init_wrong and value >= UL:
        sig_init_wrong = False

    if value <= UL and not UL_crossed and not sig_init_wrong:
        chatter_indices.append(i)
        UL_crossed = True
    elif value <= UL and UL_crossed and not sig_init_wrong:
        chatter_indices.append(i)
    elif value >= UL and UL_crossed and not sig_init_wrong:
        chatter_instances.append(chatter_indices)
        chatter_indices = []
        UL_crossed = False
    i += 1

print(chatter_instances)

j = 0

for instance in chatter_instances:
    x = rd_time[instance[0]-1:instance[-1]+2]
    y = rd_value[instance[0]-1:instance[-1]+2]
    y_UL = [UL]*(len(instance)+2)

    a0 = (y[0]-y[1])/(x[0]-x[1])
    b0 = y[0] - a0*x[0]
    x_start = (UL - b0)/a0

    af = (y[-1]-y[-2])/(x[-1]-x[-2])
    bf = y[-1] - af*x[-1]
    x_end = (UL - bf) / af

    chat_dur = "Chatter Instance " + str(j) + "  [" + str(round((x_end - x_start),2)) + " sec]"
    print(chat_dur +".png")

    plt.plot(x, y, label="Contacts Signal")
    plt.plot(x, y_UL, label="Chatter Threshold")
    plt.legend()
    plt.suptitle(chat_dur)
    plt.xlabel("Time [sec]")
    plt.ylabel("Relay Contacts Signal [V]")
    plt.savefig(chat_dur +".png")
    plt.show()

    j += 1
relay_data.close()
