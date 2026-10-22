
import math

#Use to test the Amplitude of DFT and IDFT
def SignalComapreAmplitude(SignalInput = [] ,SignalOutput= []):
    if len(SignalInput) != len(SignalOutput):
        return False
    else:
        for i in range(len(SignalInput)):
            if abs(SignalInput[i]-SignalOutput[i])>0.001:
                return False
        return True

def RoundPhaseShift(P):
    while P<0:
        P+=2*math.pi
    return float(P%(2*math.pi))

#Use to test the PhaseShift of DFT
def SignalComaprePhaseShift(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False

    for i in range(len(SignalInput)):
        difference = math.atan2(
            math.sin(SignalInput[i] - SignalOutput[i]),
            math.cos(SignalInput[i] - SignalOutput[i])
        )

        if abs(difference) > 0.001:
            return False

    return True