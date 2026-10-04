import numpy as np
import matplotlib.pyplot as plt

signal1 = np.loadtxt('Signal1.txt')
signal2 = np.loadtxt('Signal2.txt')
signal3 = np.loadtxt('signal3.txt')

def MultiplyByConst(signal,const):
    signalCopy = signal.copy()
    signalCopy[:,1] = signalCopy[:,1] * const
    signals = [
            [signal,"signal"], 
            [signalCopy,"signal multiplied by " + str(const)]
        ]
    np.savetxt('signal multiplied by ' + str(const) + '.txt', signalCopy, fmt='%d')
    for signal , name in signals:
        plt.figure()
        x = signal[:,0]
        y = signal[:,1]
        plt.plot(x,y)
        plt.title(name)  
        plt.grid(True)
    plt.show()
        
def AddSignals(signal1,signal2):
    signal1Copy = signal1.copy()
    signal2Copy = signal2.copy()
    signal1Copy[:,1] = signal1Copy[:,1] + signal2Copy[:,1]
    signals = [
            [signal1,"signal 1"], 
            [signal2,"signal 2"],
            [signal1Copy,"signal 1 + signal 2"]
        ]
    np.savetxt('signal 1 + signal 2.txt', signal1Copy, fmt='%d')
    for signal , name in signals:
        plt.figure()
        x = signal[:,0]
        y = signal[:,1]
        plt.plot(x,y)
        plt.title(name)  
        plt.grid(True)
    plt.show()
    