import numpy as np
import pylab

def getdata(file):
    f = open(file,'r+')
    T=[]
    for line in f:
        T.append(int(line))
    f.close()
    T = np.array(T)
    Time = []
    
    for i in range(len(T)):
        if i == 0:
            Time.append(i)
        else:
            Time.append((T[i]-T[i-1]))
    
    Newtime = []
    Ts = []
    Tfactor = 1000000.0
    
    for y in range(len(T)):
        if y == 0:
            Ts.append(T[0])
        else:
            Ts.append((T[y]-((T[y]-T[y-1])/2))/Tfactor)
    
    for x in range(len(Time)):
        Newtime.append(float(Time[x]/Tfactor))
    
    Speed = []
    for j in Newtime:
        if j == 0:
            Speed.append(0)
        else:
            Speed.append(1/j)
    TopSpeed = max(Speed)
    Tsmax = Ts[Speed.index(max(Speed))]
    return Speed, Ts, TopSpeed, Tsmax

def findtau(Speed, Ts): #obtain time constant
    topspeed = max(Speed)
    i=0
    while Speed[i] < (topspeed * 0.632):
        i+=1
    return Ts[i]

def init_accel(Speed, Time): #calculate intial angular accelleration
    accel = Speed[1]/Time[1]
    return accel

Data_1 = "Speed Data (V=10, DC=17, code 5).txt"
Data_2 = "Speed Data (V=10, DC=18, code 5).txt"
Data_3 = "Speed Data (V=10, DC=19, code 5).txt"
Data_4 = "Speed Data (V=10, DC=20, code 5).txt"
Data_5 = "Speed Data (V=10, DC=25, code 5).txt"
Data_6 = "Speed Data (V=10, DC=30, code 5).txt"
Data_7 = "Speed Data (V=10, DC=55, code 5).txt"
Data_8 = "Speed Data (V=10, DC=80, code 5).txt"
Data_9 = "Speed Data (V=10, DC=105, code 5).txt"
Data_10 = "Speed Data (V=10, DC=130, code 5).txt"
Data_11 = "Speed Data (V=10, DC=155, code 5).txt"
Data_12 = "Speed Data (V=10, DC=180, code 4).txt"
Data_13 = "Speed Data (V=10, DC=205, code 4).txt"
Data_14 = "Speed Data (V=10, DC=230, code 4).txt"
Data_15 = "Speed Data (V=10, DC=255, code 4).txt"

TopSpeed=np.zeros(15) #Arrays to plot
Tau=np.zeros(15)
Accel=np.zeros(15)
DutyCycle=[17, 18, 19, 20, 25, 30, 55, 80, 105, 130, 155, 180, 205, 230, 255]

Speed_1, Ts_1, TopSpeed_1, Tsmax_1 = getdata(Data_1)
Speed_2, Ts_2, TopSpeed_2, Tsmax_2 = getdata(Data_2)
Speed_3, Ts_3, TopSpeed_3, Tsmax_3 = getdata(Data_3)
Speed_4, Ts_4, TopSpeed_4, Tsmax_4 = getdata(Data_4)
Speed_5, Ts_5, TopSpeed_5, Tsmax_5 = getdata(Data_5)
Speed_6, Ts_6, TopSpeed_6, Tsmax_6 = getdata(Data_6)
Speed_7, Ts_7, TopSpeed_7, Tsmax_7 = getdata(Data_7)
Speed_8, Ts_8, TopSpeed_8, Tsmax_8 = getdata(Data_8)
Speed_9, Ts_9, TopSpeed_9, Tsmax_9 = getdata(Data_9)
Speed_10, Ts_10, TopSpeed_10, Tsmax_10 = getdata(Data_10)
Speed_11, Ts_11, TopSpeed_11, Tsmax_11 = getdata(Data_11)
Speed_12, Ts_12, TopSpeed_12, Tsmax_12 = getdata(Data_12)
Speed_13, Ts_13, TopSpeed_13, Tsmax_13 = getdata(Data_13)
Speed_14, Ts_14, TopSpeed_14, Tsmax_14 = getdata(Data_14)
Speed_15, Ts_15, TopSpeed_15, Tsmax_15 = getdata(Data_15)

TopSpeed[0] = max(Speed_1)
TopSpeed[1] = max(Speed_2)
TopSpeed[2] = max(Speed_3)
TopSpeed[3] = max(Speed_4)
TopSpeed[4] = max(Speed_5)
TopSpeed[5] = max(Speed_6)
TopSpeed[6] = max(Speed_7)
TopSpeed[7] = max(Speed_8)
TopSpeed[8] = max(Speed_9)
TopSpeed[9] = max(Speed_10)
TopSpeed[10] = max(Speed_11)
TopSpeed[11] = max(Speed_12)
TopSpeed[12] = max(Speed_13)
TopSpeed[13] = max(Speed_14)
TopSpeed[14] = max(Speed_15)

Tau[0] = findtau(Speed_1, Ts_1)
Tau[1] = findtau(Speed_2, Ts_2)
Tau[2] = findtau(Speed_3, Ts_3)
Tau[3] = findtau(Speed_4, Ts_4)
Tau[4] = findtau(Speed_5, Ts_5)
Tau[5] = findtau(Speed_6, Ts_6)
Tau[6] = findtau(Speed_7, Ts_7)
Tau[7] = findtau(Speed_8, Ts_8)
Tau[8] = findtau(Speed_9, Ts_9)
Tau[9] = findtau(Speed_10, Ts_10)
Tau[10] = findtau(Speed_11, Ts_11)
Tau[11] = findtau(Speed_12, Ts_12)
Tau[12] = findtau(Speed_13, Ts_13)
Tau[13] = findtau(Speed_14, Ts_14)
Tau[14] = findtau(Speed_15, Ts_15)

Accel[0] = init_accel(Speed_1, Ts_1)
Accel[1] = init_accel(Speed_2, Ts_2)
Accel[2] = init_accel(Speed_3, Ts_3)
Accel[3] = init_accel(Speed_4, Ts_4)
Accel[4] = init_accel(Speed_5, Ts_5)
Accel[5] = init_accel(Speed_6, Ts_6)
Accel[6] = init_accel(Speed_7, Ts_7)
Accel[7] = init_accel(Speed_8, Ts_8)
Accel[8] = init_accel(Speed_9, Ts_9)
Accel[9] = init_accel(Speed_10, Ts_10)
Accel[10] = init_accel(Speed_11, Ts_11)
Accel[11] = init_accel(Speed_12, Ts_12)
Accel[12] = init_accel(Speed_13, Ts_13)
Accel[13] = init_accel(Speed_14, Ts_14)
Accel[14] = init_accel(Speed_15, Ts_15)

print TopSpeed_1, Tsmax_1,Tau[0]
print TopSpeed_2, Tsmax_2,Tau[1]
print TopSpeed_3, Tsmax_3,Tau[2]
print TopSpeed_4, Tsmax_4,Tau[3]
print TopSpeed_5, Tsmax_5,Tau[4]
print TopSpeed_6, Tsmax_6,Tau[5]
print TopSpeed_7, Tsmax_7,Tau[6]
print TopSpeed_8, Tsmax_8,Tau[7]
print TopSpeed_9, Tsmax_9,Tau[8]
print TopSpeed_10, Tsmax_10,Tau[9]
print TopSpeed_11, Tsmax_11,Tau[10]
print TopSpeed_12, Tsmax_12,Tau[11]
print TopSpeed_13, Tsmax_13,Tau[12]
print TopSpeed_14, Tsmax_14,Tau[13]
print TopSpeed_15, Tsmax_15,Tau[14]

pylab.figure()
pylab.plot(Ts_1, Speed_1)
pylab.plot(Ts_2, Speed_2)
pylab.plot(Ts_3, Speed_3)
pylab.plot(Ts_4, Speed_4)
pylab.plot(Ts_5, Speed_5)
pylab.plot(Ts_6, Speed_6)
pylab.plot(Ts_7, Speed_7)
pylab.plot(Ts_8, Speed_8)
pylab.plot(Ts_9, Speed_9)
pylab.plot(Ts_10, Speed_10)
pylab.plot(Ts_11, Speed_11)
pylab.plot(Ts_12, Speed_12)
pylab.plot(Ts_13, Speed_13)
pylab.plot(Ts_14, Speed_14)
pylab.plot(Ts_15, Speed_15)
pylab.xlabel('Time in Seconds')
pylab.ylabel('Speed in RPS')
pylab.show()

pylab.figure()
pylab.plot(DutyCycle, TopSpeed)
pylab.xlabel('PWM Duty Cycle')
pylab.ylabel('Max. Speed')
pylab.show()

pylab.figure()
pylab.plot(DutyCycle, Tau)
pylab.xlabel('PWM Duty Cycle')
pylab.ylabel('Time Constant')
pylab.show()

pylab.figure()
pylab.plot(DutyCycle, Accel)
pylab.xlabel('PWM Duty Cycle')
pylab.ylabel('Initial Acceleration')
pylab.show()