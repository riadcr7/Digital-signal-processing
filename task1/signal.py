import numpy as np
import matplotlib.pyplot as plt
import os

class Signal:
    def __init__(self, fileName):
        self.signal = np.loadtxt(fileName,skiprows=3)
        self.name = fileName
        self.const = 1
        
    def MultiplyByConst(self,const):
        signalCopy = self.signal.copy()
        signalCopy[:,1] = signalCopy[:,1] * const
        
        signals = [
                [self.signal,"signal"], 
                [signalCopy,"signal multiplied by " + str(const)]
            ]
        
        with open('signal multiplied by ' + str(const) + '.txt', "w") as f:
            f.write("0\n")
            f.write("0\n")
            f.write(f"{len(self.signal)}\n")
            np.savetxt(f, signalCopy, fmt='%d')
        
        for signal , name in signals:
            plt.figure()
            x = signal[:,0]
            y = signal[:,1]
            plt.plot(x,y)
            plt.title(name)  
            plt.grid(True)
        plt.show()
        
    def AddSignals(self,signal2):
        signal1Copy = self.signal.copy()
        signal2Copy = signal2.signal.copy()
        signal1Copy[:,1] = signal1Copy[:,1] + signal2Copy[:,1]
        
        signals = [
                [self.signal,"signal 1"], 
                [signal2.signal,"signal 2"],
                [signal1Copy,"signal 1 + signal 2"]
            ]
        name1 = os.path.splitext(os.path.basename(self.name))[0]
        name2 = os.path.splitext(os.path.basename(signal2.name))[0]
        with open(name1 + " + " + name2 + ".txt" , "w") as f:
            f.write("0\n")
            f.write("0\n")
            f.write(f"{len(self.signal)}\n")
            np.savetxt(f, signal1Copy, fmt='%d')
            
        for signal , name in signals:
            plt.figure()
            x = signal[:,0]
            y = signal[:,1]
            plt.plot(x,y)
            plt.title(name)  
            plt.grid(True)
        plt.show()
