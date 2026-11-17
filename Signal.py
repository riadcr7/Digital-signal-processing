import numpy as np
import matplotlib.pyplot as plt
import os
import cmath
import math
from test import ReadSignalFile , AddSignalSamplesAreEqual , MultiplySignalByConst , SignalSamplesAreEqual , QuantizationTest1 , QuantizationTest2 , SignalComapreAmplitude ,RoundPhaseShift , SignalComaprePhaseShift , Shift_Fold_Signal , ConvTest

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

    def Smoothing(self, points):
        indices, samples = ReadSignalFile(self.name)

        points = int(points)

        if points <= 0 or points > len(samples):
            raise ValueError("Invalid number of averaging points.")

        result = []
        result_indices = []

        for i in range(len(samples) - points + 1):
            average = sum(samples[i:i + points]) / points
            result.append(average)
            result_indices.append(indices[i])
            
            
        input_path1 = os.path.normcase(
            os.path.normpath(
                r"D:\Digital-signal-processing-main\Signals\Signal1.txt"
            )
        )
        
        input_path2 = os.path.normcase(
            os.path.normpath(
                r"D:\Digital-signal-processing-main\Signals\Signal2.txt"
            )
        )

        current_path = os.path.normcase(
            os.path.normpath(self.name)
        )

        if current_path == input_path1:
            SignalSamplesAreEqual(
                "smoothing signal",
                r"D:\Digital-signal-processing-main\output\OutMovAvgTest1.txt",
                result_indices, result
            )
        elif current_path == input_path2:
            SignalSamplesAreEqual(
                "smoothing signal",
                r"D:\Digital-signal-processing-main\output\OutMovAvgTest2.txt",
                result_indices, result
            )

        return result_indices, result

    def DerivativeSignal(self):
        InputSignal=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0]  
        expectedOutput_first = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        expectedOutput_second = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        """
        Write your Code here:
        Start
        """

        FirstDrev = [
            InputSignal[i] - InputSignal[i - 1]
            for i in range(1, len(InputSignal))
        ]

        SecondDrev = [
            InputSignal[i + 1] - 2 * InputSignal[i] + InputSignal[i - 1]
            for i in range(1, len(InputSignal) - 1)
        ]

        """
        End
        """
        if( (len(FirstDrev)!=len(expectedOutput_first)) or (len(SecondDrev)!=len(expectedOutput_second))):
            print("mismatch in length") 
            return
        first=second=True
        for i in range(len(expectedOutput_first)):
            if abs(FirstDrev[i] - expectedOutput_first[i]) < 0.01:
                continue
            else:
                first=False
                print("1st derivative wrong")
                return
        for i in range(len(expectedOutput_second)):
            if abs(SecondDrev[i] - expectedOutput_second[i]) < 0.01:
                continue
            else:
                second=False
                print("2nd derivative wrong") 
                return
        if(first and second):
            print("Derivative Test case passed successfully")
        else:
            print("Derivative Test case failed")
        return

    def Shift(self, k , fold=False):
        if fold:
            indices, samples = self.Folding()
        else:
            indices, samples = ReadSignalFile(self.name)
            
        k = int(k)

        result_indices = [index + k for index in indices]
        
        if k == 500 and fold:
            Shift_Fold_Signal(r"D:\Digital-signal-processing-main\output\Output_ShifFoldedby500.txt", result_indices, samples)
        elif k == -500 and fold:
            Shift_Fold_Signal(r"D:\Digital-signal-processing-main\output\Output_ShiftFoldedby-500.txt", result_indices, samples)

        return result_indices, samples

    def Folding(self):
        indices, samples = ReadSignalFile(self.name)

        for i in range(len(samples)//2):
            samples[i] , samples[len(samples) - 1 - i] = samples[len(samples) - 1 - i] , samples[i]
        
        input_path = os.path.normcase(
            os.path.normpath(
                r"D:\Digital-signal-processing-main\Signals\input_fold.txt"
            )
        )

        current_path = os.path.normcase(
            os.path.normpath(self.name)
        )

        if current_path == input_path:
            SignalSamplesAreEqual(
                "folding signal",
                r"D:\Digital-signal-processing-main\output\Output_fold.txt",
                indices,
                samples
            )
            
        return indices , samples

    def RemoveDC_TimeDomain(self):
        indices, samples = ReadSignalFile(self.name)

        if not samples:
            return indices, []

        dc_value = sum(samples) / len(samples)

        result = [
            sample - dc_value
            for sample in samples
        ]
        
        SignalSamplesAreEqual(
                "remove DC component in time domain",
                r"D:\Digital-signal-processing-main\output\DC_component_output.txt",
                indices,
                result
            )

        return indices, result

    def Convolution(self, other_signal):
        indices1, samples1 = ReadSignalFile(self.name)

        # Accept either another Signal object or a file path.
        other_name = (
            other_signal.name
            if isinstance(other_signal, Signal)
            else other_signal
        )

        indices2, samples2 = ReadSignalFile(other_name)

        result = {}

        for i, x in zip(indices1, samples1):
            for j, h in zip(indices2, samples2):
                output_index = i + j

                result[output_index] = (
                    result.get(output_index, 0) + x * h
                )

        result_indices = sorted(result.keys())
        result_samples = [
            result[index] for index in result_indices
        ]
        
        ConvTest(result_indices, result_samples)

        return result_indices, result_samples
 