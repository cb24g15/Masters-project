import numpy as np
import pylab as plt
from scipy import signal


def getdata_2(file):
    f = open(file,'r+')
    T_column=[]
    Time=[]
    Pos=[]
    Pos_norm=[]
    
    for line in f:
        a,b = line.split()
        T_column.append(int(a))
        Pos.append(int(b))
    f.close()
    
    for i in range(len(T_column)):
        Time.append((T_column[i]-T_column[0])*10**-6)
        
    for i in range(len(Pos)):
        Pos_norm.append(Pos[i]-Pos[-1])
        
    dT = []
    for i in range(len(Time)-1):
        dT.append(Time[i+1]-Time[i])
    dTmean = np.mean(dT)
    dTstd = np.std(dT)
    
    return Time, Pos_norm, dTmean, dTstd

def truncate_2(Time, Pos, Length):
    Time_plot=[]
    Pos_plot=[]
    for i in range(len(Time)):
        if Time[i] <= Length:
            Time_plot.append(Time[i])
            Pos_plot.append(Pos[i])
    
    return Time_plot, Pos_plot

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

def get_maxima(Pos, Time):
    maxima=[]
    maxtimes=[]
    for i in range(1, len(Pos)-1): #find local maxima
       if abs(Pos[i]) > abs(Pos[i-1]) and abs(Pos[i]) > abs(Pos[i+1]):
           maxima.append(abs(Pos[i]))
           maxtimes.append(Time[i])
           
    return maxima, maxtimes
    
Data_1 = "Swing Test_1.txt"
Data_2 = "Swing Test_2.txt"
Data_3 = "Swing Test_3.txt"
Data_4 = "Swing Test_4.txt"

Plot_Time = 6
Freq_Max = 3
F_off = 5

Time_1, Pos_1, dTmean_1, dTstd_1 = getdata_2(Data_1)
Time_2, Pos_2, dTmean_2, dTstd_2 = getdata_2(Data_2)
Time_3, Pos_3, dTmean_3, dTstd_3 = getdata_2(Data_3)
Time_4, Pos_4, dTmean_4, dTstd_4 = getdata_2(Data_4)

Time_1plot, Pos_1plot = truncate_2(Time_1, Pos_1, Plot_Time)
Time_2plot, Pos_2plot = truncate_2(Time_2, Pos_2, Plot_Time)
Time_3plot, Pos_3plot = truncate_2(Time_3, Pos_3, Plot_Time)
Time_4plot, Pos_4plot = truncate_2(Time_4, Pos_4, Plot_Time)       

Spec_1, Frq_1 = spec_unfiltered(Pos_1, Time_1, Freq_Max)
Spec_2, Frq_2 = spec_unfiltered(Pos_2, Time_2, Freq_Max)
Spec_3, Frq_3 = spec_unfiltered(Pos_3, Time_3, Freq_Max)
Spec_4, Frq_4 = spec_unfiltered(Pos_4, Time_4, Freq_Max)

Pos_1_filt = sig_filtered(Pos_1, dTmean_1, F_off)
Pos_2_filt = sig_filtered(Pos_2, dTmean_2, F_off)
Pos_3_filt = sig_filtered(Pos_3, dTmean_3, F_off)
Pos_4_filt = sig_filtered(Pos_4, dTmean_4, F_off)

Maxima_1, Maxtimes_1 = get_maxima(Pos_1_filt, Time_1)
Maxima_2, Maxtimes_2 = get_maxima(Pos_2_filt, Time_2)
Maxima_3, Maxtimes_3 = get_maxima(Pos_3_filt, Time_3)
Maxima_4, Maxtimes_4 = get_maxima(Pos_4_filt, Time_4)

Time_1filtplot, Pos_1filtplot = truncate_2(Time_1, Pos_1_filt, Plot_Time)
Time_2filtplot, Pos_2filtplot = truncate_2(Time_2, Pos_2_filt, Plot_Time)
Time_3filtplot, Pos_3filtplot = truncate_2(Time_3, Pos_3_filt, Plot_Time)
Time_4filtplot, Pos_4filtplot = truncate_2(Time_4, Pos_4_filt, Plot_Time)  

plt.figure()
plt.plot(Time_1plot, Pos_1plot, label='Data 1')
plt.plot(Time_2plot, Pos_2plot, label='Data 2')
plt.plot(Time_3plot, Pos_3plot, label='Data 3')
plt.plot(Time_4plot, Pos_4plot, label='Data 4')
plt.xlabel('Time (s)')
plt.ylabel('Position (Raw Input)')
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

plt.figure()
plt.plot(Maxtimes_1, Maxima_1)
plt.plot(Maxtimes_2, Maxima_2)
plt.plot(Maxtimes_3, Maxima_3)
plt.plot(Maxtimes_4, Maxima_4)
plt.xlabel('Time(s)')
plt.ylabel('Position Maxima')