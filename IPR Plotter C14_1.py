import numpy as np
import pylab as plt
from scipy import signal


def getdata(file):
    f = open(file,'r+')
    T_column=[]
    Time=[]
    Pos=[]
    V=[]
    
    for line in f:
        a,b,c = line.split()
        T_column.append(int(a))
        Pos.append(float(b))
        V.append(int(c))
    f.close()
    
    for i in range(len(T_column)):
        Time.append((T_column[i]-T_column[0])*10**-6)
        
    dT = []
    for i in range(len(Time)-1):
        dT.append(Time[i+1]-Time[i])
    dTmean = np.mean(dT)
    dTstd = np.std(dT)
    
    return Time, Pos, V, dTmean, dTstd

def truncate(Time, Pos, V, Length):
    Time_plot=[]
    Pos_plot=[]
    V_plot=[]
    for i in range(len(Time)):
        if Time[i] <= Length:
            Time_plot.append(Time[i])
            Pos_plot.append(Pos[i])
            V_plot.append(V[i])
    
    return Time_plot, Pos_plot, V_plot

def spec_unfiltered(X, T, F_max=500):
    dF = 1.0/T[-1]
    F_ny = (len(X)/2)*dF
    Xf = abs(np.fft.fft(X))[0:int(len(X)/(2*(F_ny/F_max)))]
    Frq = [(i*dF) for i in range(0,int(len(X)/(2*(F_ny/F_max))))]
    
    return Xf, Frq

def sig_filtered(X, dT, F_off):
    F_s = 1/dT
    w_off = F_off/(F_s/2)
    a, b = signal.butter(4, w_off, 'low')
    X_filt = signal.filtfilt(a, b, X)
    
    return X_filt
    
Data_1 = "Foam (Kp=60, Kd=5, Ki=0, Baud=115200).txt"
Data_2 = "Foam (Kp=120, Kd=10, Ki=0, Baud=115200).txt"
Data_3 = "Foam (Kp=120, Kd=20, Ki=0, Baud=115200).txt"
Data_4 = "(Kp=90, Kd=0, Ki=0, Baud=115200).txt"

Plot_Time = 25
Freq_Max = 4
F_off = 5

Time_1, Pos_1, V_1, dTmean_1, dTstd_1 = getdata(Data_1)
Time_2, Pos_2, V_2, dTmean_2, dTstd_2 = getdata(Data_2)
Time_3, Pos_3, V_3, dTmean_3, dTstd_3 = getdata(Data_3)
Time_4, Pos_4, V_4, dTmean_4, dTstd_4 = getdata(Data_4)

Time_1plot, Pos_1plot, V_1plot = truncate(Time_1, Pos_1, V_1, Plot_Time)
Time_2plot, Pos_2plot, V_2plot = truncate(Time_2, Pos_2, V_2, Plot_Time)
Time_3plot, Pos_3plot, V_3plot = truncate(Time_3, Pos_3, V_3, Plot_Time)
Time_4plot, Pos_4plot, V_4plot = truncate(Time_4, Pos_4, V_4, Plot_Time)       

Spec_1, Frq_1 = spec_unfiltered(Pos_1, Time_1, Freq_Max)
Spec_2, Frq_2 = spec_unfiltered(Pos_2, Time_2, Freq_Max)
Spec_3, Frq_3 = spec_unfiltered(Pos_3, Time_3, Freq_Max)
Spec_4, Frq_4 = spec_unfiltered(Pos_4, Time_4, Freq_Max)

Pos_1_filt = sig_filtered(Pos_1, dTmean_1, F_off)
Pos_2_filt = sig_filtered(Pos_2, dTmean_2, F_off)
Pos_3_filt = sig_filtered(Pos_3, dTmean_3, F_off)
Pos_4_filt = sig_filtered(Pos_4, dTmean_4, F_off)

V_1_filt = sig_filtered(V_1, dTmean_1, F_off)
V_2_filt = sig_filtered(V_2, dTmean_2, F_off)
V_3_filt = sig_filtered(V_3, dTmean_3, F_off)
V_4_filt = sig_filtered(V_4, dTmean_4, F_off)

Time_1filtplot, Pos_1filtplot, V_1filtplot = truncate(Time_1, Pos_1_filt, V_1_filt, Plot_Time)
Time_2filtplot, Pos_2filtplot, V_2filtplot = truncate(Time_2, Pos_2_filt, V_2_filt, Plot_Time)
Time_3filtplot, Pos_3filtplot, V_3filtplot = truncate(Time_3, Pos_3_filt, V_3_filt, Plot_Time)
Time_4filtplot, Pos_4filtplot, V_4filtplot = truncate(Time_4, Pos_4_filt, V_4_filt, Plot_Time)  

Spec_1filt, Frq_1filt = spec_unfiltered(Pos_1_filt, Time_1, Freq_Max)
Spec_2filt, Frq_2filt = spec_unfiltered(Pos_2_filt, Time_2, Freq_Max)
Spec_3filt, Frq_3filt = spec_unfiltered(Pos_3_filt, Time_3, Freq_Max)
Spec_4filt, Frq_4filt = spec_unfiltered(Pos_4_filt, Time_4, Freq_Max)

plt.figure()
plt.plot(Time_1plot, Pos_1plot, label='Data 1')
plt.plot(Time_2plot, Pos_2plot, label='Data 2')
plt.plot(Time_3plot, Pos_3plot, label='Data 3')
plt.plot(Time_4plot, Pos_4plot, label='Data 4')
plt.xlabel('Time (s)')
plt.ylabel('Position (Raw Input)')
plt.legend()

plt.figure()
plt.plot(Time_1plot, V_1plot, label='Data 1')
plt.plot(Time_2plot, V_2plot, label='Data 2')
plt.plot(Time_3plot, V_3plot, label='Data 3')
plt.plot(Time_4plot, V_4plot, label='Data 4')
plt.xlabel('Time (s)')
plt.ylabel('Duty Cycle Output')
plt.legend()

plt.figure()
plt.plot(Time_1filtplot, Pos_1filtplot, label='Data 1')
plt.plot(Time_2filtplot, Pos_2filtplot, label='Data 2')
plt.plot(Time_3filtplot, Pos_3filtplot, label='Data 3')
plt.plot(Time_4filtplot, Pos_4filtplot, label='Data 4')
plt.xlabel('Time (s)')
plt.ylabel('Position (Raw Input)')
plt.legend()

plt.figure()
plt.plot(Time_1filtplot, V_1filtplot, label='Data 1')
plt.plot(Time_2filtplot, V_2filtplot, label='Data 2')
plt.plot(Time_3filtplot, V_3filtplot, label='Data 3')
plt.plot(Time_4filtplot, V_4filtplot, label='Data 4')
plt.xlabel('Time (s)')
plt.ylabel('Duty Cycle Output')
plt.legend()

plt.figure()
plt.plot(Frq_1, Spec_1, label='Data 1')
plt.plot(Frq_2, Spec_2, label='Data 2')
plt.plot(Frq_3, Spec_3, label='Data 3')
plt.plot(Frq_4, Spec_4, label='Data 4')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.legend()

plt.figure()
plt.plot(Frq_1, 20*np.log10(Spec_1), label='Data 1')
plt.plot(Frq_2, 20*np.log10(Spec_2), label='Data 2')
plt.plot(Frq_3, 20*np.log10(Spec_3), label='Data 3')
plt.plot(Frq_4, 20*np.log10(Spec_4), label='Data 4')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (dB)')
plt.legend()