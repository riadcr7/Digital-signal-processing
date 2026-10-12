import os
def ReadSignalFile(file_name):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices,expected_samples

def AddSignalSamplesAreEqual(userFirstSignal,userSecondSignal,Your_indices,Your_samples):
    first = os.path.normcase(os.path.normpath(userFirstSignal))
    second = os.path.normcase(os.path.normpath(userSecondSignal))

    signal1 = os.path.normcase(os.path.normpath(
        r'D:\Digital-signal-processing-main\task1\Signal1.txt'
    ))
    signal2 = os.path.normcase(os.path.normpath(
        r'D:\Digital-signal-processing-main\task1\Signal2.txt'
    ))
    signal3 = os.path.normcase(os.path.normpath(
        r'D:\Digital-signal-processing-main\task1\Signal3.txt'
    ))

    if first == signal1 and second == signal2:
        file_name = r'D:\Digital-signal-processing-main\task1\output\Signal1+signal2.txt'

    elif first == signal1 and second == signal3:
        file_name = r'D:\Digital-signal-processing-main\task1\output\signal1+signal3.txt'

    else:
        raise ValueError(f"Unexpected input paths: {userFirstSignal}, {userSecondSignal}")
    
    expected_indices,expected_samples=ReadSignalFile(file_name)
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Addition Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Addition Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Addition Test case failed, your signal have different values from the expected one")
            return
    print("Addition Test case passed successfully")
    
def MultiplySignalByConst(User_Const,Your_indices,Your_samples):
    if(User_Const==5):
        file_name= r"D:\Digital-signal-processing-main\task1\output\MultiplySignalByConstant-Signal1 - by 5.txt" # write here path of MultiplySignalByConstant-Signal1 - by 5.txt
    elif(User_Const==10):
        file_name= r"D:\Digital-signal-processing-main\task1\output\MultiplySignalByConstant-signal2 - by 10.txt" # write here path of MultiplySignalByConstant-Signal2 - by 10.txt

    expected_indices,expected_samples=ReadSignalFile(file_name)
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Multiply by "+str(User_Const)+ " Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Multiply by "+str(User_Const)+" Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Multiply by "+str(User_Const)+" Test case failed, your signal have different values from the expected one")
            return
    print("Multiply by "+str(User_Const)+" Test case passed successfully")