#Function of distance against time for a simple pendulum
from math import cos, pi
import pylab
import numpy as np

def distancefunc():
    x = []
    N = 301
    t = np.linspace(0, 30, N)
    l = 1.0 #length of rod
    g = 9.81 #gravity of earth
    tau = 2.0*pi*((l/g)**0.5)
    X = -75.0 #the distance we move it away from the centre (max distance)
    for i in t:
        x.append(float(X)*cos((float(pi)*i)/float(tau)))
    return x, t

def distancedata(file):
    f = open(file, 'r+')
    T = []
    X = []
    Time = []
    Tfactor = 100000.0 #converts the time into something..
    for line in f:
        a,b = line.split()
        T.append(a)
        X.append(b)
    f.close()
    #For some reason the data was coming out as a string rather than an integer..
    for i in range(len(T)):
        T[i] = int(T[i])
    #Need to fix the position data, as the raw position is in the 600s.
    for i in range(len(X)):
        X[i] = int(X[i])
    #This reduces the time, not sure what value of time we are in.
    for i in range(len(T)):
        if i == 0:
            Time.append(i)
        else:
            Time.append((T[i]-T[0])/Tfactor)
    Xfactor = X[-1]
    X[:] = [i - Xfactor for i in X]
    return X, Time

#X, T = distancedata(Data_1) 

xoft, tfunc = distancefunc()
Data_1 = "Swing Test_7.txt"
Data_2 = "Swing Test_2.txt"
Data_3 = "Swing Test_3.txt"
Data_4 = "Swing Test_4.txt"
Data_5 = "Swing Test_5.txt"
Data_6 = "Swing Test_6.txt"
Data_7 = "Swing and Flick.txt"
Data_8 = "Swing and Flick_2.txt"
Data_9 = "Swing and Flick_3.txt"

X_1, T_1 = distancedata(Data_1)
X_2, T_2 = distancedata(Data_2)
X_3, T_3 = distancedata(Data_3)
X_4, T_4 = distancedata(Data_4)
X_5, T_5 = distancedata(Data_5)
X_6, T_6 = distancedata(Data_6)
X_7, T_7 = distancedata(Data_7)
X_8, T_8 = distancedata(Data_8)
X_9, T_9 = distancedata(Data_9)

pylab.plot(tfunc, xoft)
pylab.title('ideal pendulum swinging')
pylab.xlabel('time') 
pylab.ylabel('Distance from the centre')
pylab.show()  

pylab.plot(T_1, X_1, label='Data 1')
pylab.plot(T_2, X_2, label='Data 2')
pylab.plot(T_3, X_3, label='Data 3')
pylab.plot(T_4, X_4, label='Data 4')
#pylab.plot(T_5, X_5, label='Data 5')
pylab.plot(T_6, X_6, label='Data 5')
#pylab.plot(tfunc, xoft)
pylab.title('Our Pendulum Swinging with an offset')
pylab.xlabel('time')
pylab.ylabel('Distance from centre')
pylab.legend()

#pylab.plot(T_7, X_7)
#pylab.plot(T_8, X_8)
#pylab.plot(T_9, X_9)
#pylab.plot(tfunc, xoft)
#pylab.legend()
#pylab.title('Pendulum starts from centre and is wacked')
#pylab.xlabel('time in microseconds')
#pylab.ylabel('Distance from centre')
#pylab.show()