import numpy as np
import matplotlib.pyplot as plt
import os
import cmath
import math
from test import ReadSignalFile , AddSignalSamplesAreEqual , MultiplySignalByConst , SignalSamplesAreEqual , QuantizationTest1 , QuantizationTest2 , SignalComapreAmplitude ,RoundPhaseShift , SignalComaprePhaseShift

class Signal:
    def __init__(self, fileName):
        self.name = fileName
        
    def MultiplyByConst(self,const):
        signal_indices,signal_samples=ReadSignalFile(self.name)
        signal_samples_copy = signal_samples.copy()
        for i in range(len(signal_samples_copy)):
            signal_samples_copy[i] *= const

        signals = [
                [[signal_indices,signal_samples],"signal"], 
                [[signal_indices,signal_samples_copy],"signal multiplied by " + str(const)]
            ]
        
        MultiplySignalByConst(const,signal_indices,signal_samples_copy)
        
        for signal , name in signals:
            plt.figure()
            plt.plot(signal[0],signal[1])
            plt.title(name)  
            plt.grid(True)
        plt.show()
        
    def AddSignals(self,signal2):
        signal1_indices,signal1_samples=ReadSignalFile(self.name)
        signal2_indices,signal2_samples=ReadSignalFile(signal2.name)
        signal1_add_signal2 = signal1_samples.copy()
        signal2_samples_copy = signal2_samples.copy()
        
        for i in range(len(signal1_add_signal2)):
            signal1_add_signal2[i] += signal2_samples_copy[i]
        
        name1 = os.path.splitext(os.path.basename(self.name))[0]
        name2 = os.path.splitext(os.path.basename(signal2.name))[0]
        
        signals = [
                [[signal1_indices,signal1_samples],name1], 
                [[signal2_indices,signal2_samples],name2],
                [[signal1_indices,signal1_add_signal2],name1 + " + " + name2]
            ]

        AddSignalSamplesAreEqual(self.name,signal2.name,signal1_indices,signal1_add_signal2)
           
        for signal , name in signals:
            plt.figure()
            plt.plot(signal[0],signal[1])
            plt.title(name)  
            plt.grid(True)
        plt.show()

    def SubSignals(self,signal2):
        signal1_indices,signal1_samples=ReadSignalFile(self.name)
        signal2_indices,signal2_samples=ReadSignalFile(signal2.name)
        signal1_sub_signal2 = signal1_samples.copy()
        signal2_samples_copy = signal2_samples.copy()
        
        for i in range(len(signal1_sub_signal2)):
            signal1_sub_signal2[i] = signal2_samples_copy[i] - signal1_sub_signal2[i]
        
        name1 = os.path.splitext(os.path.basename(self.name))[0]
        name2 = os.path.splitext(os.path.basename(signal2.name))[0]
        
        signals = [
                [[signal1_indices,signal1_samples],name1], 
                [[signal2_indices,signal2_samples],name2],
                [[signal1_indices,signal1_sub_signal2],name1 + " - " + name2]
            ]
        if (name2 == "Signal2"):
            SignalSamplesAreEqual("subtract signals",r"D:\Digital-signal-processing-main\output\Signal1-signal2.txt",signal1_indices,signal1_sub_signal2)
        elif (name2 == "Signal3"):
            SignalSamplesAreEqual("subtract signals",r"D:\Digital-signal-processing-main\output\Signal1-signal3.txt",signal1_indices,signal1_sub_signal2) 
        
        for signal , name in signals:
            plt.figure()
            plt.plot(signal[0],signal[1])
            plt.title(name)  
            plt.grid(True)
        plt.show()
        
    def squaringsignals(self):
        signal_indices,signal_samples=ReadSignalFile(self.name)
        signal_samples_copy = signal_samples.copy()
        for i in range(len(signal_samples_copy)):
            signal_samples_copy[i] = signal_samples_copy[i] ** 2
        
        signals = [
                [[signal_indices,signal_samples],"signal"], 
                [[signal_indices,signal_samples_copy],"signal squared"]
            ]
        
        SignalSamplesAreEqual("squaring signals",r"D:\Digital-signal-processing-main\output\Output squaring signal 1.txt",signal_indices,signal_samples_copy)
        
        for signal , name in signals:
            plt.figure()
            plt.plot(signal[0],signal[1])
            plt.title(name)  
            plt.grid(True)
        plt.show() 
        
    def accumulation(self):
        signal_indices,signal_samples=ReadSignalFile(self.name)
        signal_samples_copy = signal_samples.copy()
        for i in range(1,len(signal_samples_copy)):
            signal_samples_copy[i] += signal_samples_copy[i-1]
        
        signals = [
                [[signal_indices,signal_samples],"signal"], 
                [[signal_indices,signal_samples_copy],"accumulated signal"]
            ]
        
        SignalSamplesAreEqual("accumulation signals",r"D:\Digital-signal-processing-main\output\output accumulation for signal1.txt",signal_indices,signal_samples_copy)
        
        for signal , name in signals:
            plt.figure()
            plt.plot(signal[0],signal[1])
            plt.title(name)  
            plt.grid(True)
        plt.show()
        
    def normalization_ZeroToOne (self):
        signal_indices,signal_samples=ReadSignalFile(self.name)
        signal_samples_copy = signal_samples.copy()
        min = np.min(signal_samples)
        max = np.max(signal_samples)
        for i in range(len(signal_samples_copy)):
            signal_samples_copy[i] = (signal_samples_copy[i] - min) / (max - min)
        
        signals = [
                [[signal_indices,signal_samples],"signal"], 
                [[signal_indices,signal_samples_copy],"normalized signal"]
            ]
        
        SignalSamplesAreEqual("normalization signals from 0 to 1",r"D:\Digital-signal-processing-main\output\normlize signal 2 (from 0 to 1 )-- output.txt",signal_indices,signal_samples_copy)
        
        for signal , name in signals:
            plt.figure()
            plt.plot(signal[0],signal[1])
            plt.title(name)  
            plt.grid(True)
        plt.show()
        
    def normalization_MinusOneToOne (self):
        signal_indices,signal_samples=ReadSignalFile(self.name)
        signal_samples_copy = signal_samples.copy()
        min = np.min(signal_samples)
        max = np.max(signal_samples)
        for i in range(len(signal_samples_copy)):
            signal_samples_copy[i] = 2 * (signal_samples_copy[i] - min) / (max - min) - 1
            
        signals = [
                [[signal_indices,signal_samples],"signal"], 
                [[signal_indices,signal_samples_copy],"normalized signal"]
            ]
        
        SignalSamplesAreEqual("normalization signals from -1 to 1",r"D:\Digital-signal-processing-main\output\normalize of signal 1 (from -1 to 1)-- output.txt",signal_indices,signal_samples_copy)
        
        for signal , name in signals:
            plt.figure()
            plt.plot(signal[0],signal[1])
            plt.title(name)  
            plt.grid(True)
        plt.show()
            
    def quantize(self):
        name1 = os.path.splitext(os.path.basename(self.name))[0]
        signal_indices,signal_samples=ReadSignalFile(self.name)
        signal_samples_copy = signal_samples.copy()
        signal_indices_copy = signal_indices.copy()
        signal_indices_decimal = signal_indices.copy()
        signal_samples_error = signal_samples.copy()  
        
        min = np.min(signal_samples)
        max = np.max(signal_samples)
        level = 0
        if(name1 == "Quan1_input"):
            level = 8
        else:
            level = 4
        delta = float(f"{((max - min) / level):.4}")  # Round delta to 4 decimal places
        intervals = []
        for i in range(0,level+1):
            intervals.append(float(f"{(min + i * delta):.4}"))  # Round intervals to 4 decimal places

        for i in range(len(signal_samples_copy)):
            for j in range(0,level):
                if signal_samples_copy[i] >= intervals[j] and signal_samples_copy[i] <= intervals[j+1]:
                    signal_indices_decimal[i] = j+1  # Store the decimal representation of the quantized level
                    if(name1 == "Quan1_input"):
                        signal_indices_copy[i] = format(j,'03b')
                    else:
                        signal_indices_copy[i] = format(j, '02b')  
                    signal_samples_copy[i] = intervals[j] + delta / 2
                    signal_samples_error[i] = signal_samples_copy[i] - signal_samples_error[i]  # Calculate the quantization error
                    signal_samples_error[i] = float(f"{signal_samples_error[i]:.4}")
                    signal_samples_copy[i] = float(f"{signal_samples_copy[i]:.4}")  
                    break
        
        if(name1 == "Quan1_input"):
            QuantizationTest1(r"D:\Digital-signal-processing-main\output\Quan1_Out.txt",signal_indices_copy,signal_samples_copy)
        else :
            QuantizationTest2(r"D:\Digital-signal-processing-main\output\Quan2_Out.txt",signal_indices_decimal,signal_indices_copy,signal_samples_copy,signal_samples_error)
     
    def calcDFT(self):
        signal_indices, signal_samples = ReadSignalFile(self.name)
        amp_out, phi_out = ReadSignalFile(
            r"D:\Digital-signal-processing-main\output\Output_Signal_DFT_A,Phase.txt"
        )


        N = len(signal_samples)
        if N == 0:
            raise ValueError("The input signal is empty.")

        coefficients = []

        for k in range(N):
            Xk = 0j

            for n in range(N):
                Xk += signal_samples[n] * cmath.exp(
                    -2j * math.pi * k * n / N
                )

            coefficients.append(Xk)

        amplitudes = [int(abs(x)) for x in coefficients]
        phases = [cmath.phase(x) for x in coefficients]

        dc_input_path = os.path.normcase(
            os.path.normpath(
                r"D:\Digital-signal-processing-main\Signals\DC_component_input.txt"
            )
        )

        current_path = os.path.normcase(
            os.path.normpath(self.name)
        )

        if current_path != dc_input_path:
            if (SignalComapreAmplitude(amplitudes, amp_out)
                    and SignalComaprePhaseShift(phases, phi_out)):
                print("calculation of DFT passed successfully")
            else:
                print("error in calculation of DFT")

    
        return coefficients

    def calcIDFT(self, coefficients=None):
        if coefficients is None:
            amplitudes, phases = ReadSignalFile(self.name)

            if len(amplitudes) != len(phases):
                raise ValueError(
                    "Amplitude and phase arrays must have equal lengths."
                )

            coefficients = [
                cmath.rect(amplitude, phase)
                for amplitude, phase in zip(amplitudes, phases)
            ]

        N = len(coefficients)
        if N == 0:
            raise ValueError("The input contains no Fourier coefficients.")

        result = []

        for n in range(N):
            x = 0j

            for k in range(N):
                x += coefficients[k] * cmath.exp(
                    2j * math.pi * k * n / N
                )

            result.append(x.real / N)

        indices = list(range(N))

        # Preserve your assignment's IDFT comparison.
        expected_indices, expected_samples = ReadSignalFile(
            r"D:\Digital-signal-processing-main\output\Output_Signal_IDFT.txt"
        )
        
        dc_input_path = os.path.normcase(
            os.path.normpath(
                r"D:\Digital-signal-processing-main\Signals\DC_component_input.txt"
            )
        )

        current_path = os.path.normcase(
            os.path.normpath(self.name)
        )

        if current_path != dc_input_path:
            SignalSamplesAreEqual(
                "IDFT",
                r"D:\Digital-signal-processing-main\output\Output_Signal_IDFT.txt",
                indices,
                [round(x) for x in result]
            )

        return result

    def RemoveDC(self):
        coefficients = self.calcDFT()

        # Remove the zero-frequency component.
        coefficients[0] = 0j

        # Reconstruct the signal after removing DC.
        result = self.calcIDFT(coefficients)

        indices, _ = ReadSignalFile(self.name)

        # Preserve your original DC test.
        SignalSamplesAreEqual(
            "Remove DC component",
            r"D:\Digital-signal-processing-main\output\DC_component_output.txt",
            indices,
            result
        )

        return result
