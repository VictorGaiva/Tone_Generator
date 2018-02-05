"""Meh"""
import numpy
import matplotlib.pyplot as plt
import pyaudio
import json

def play_sound(data, sample):
    """play"""
    the = pyaudio.PyAudio()
    stream = the.open(
        format=pyaudio.paInt32,
        channels=1,
        rate=sample,
        output=True
    )
    normal = (data*1073741824.0).astype(numpy.int32)

    for _, val in enumerate(numpy.array_split(normal, 1024)):
        stream.write(val.tobytes())
    stream.stop_stream()
    stream.close()
    the.terminate()

def bake_multiplier(multiplier, sr, duration):
    """
    Returns the baked multiplier
    """
    signal = 1
    for mult in multiplier:
        if mult["type"] == "fixed":
            sig = mult["value"]
        elif mult["type"] == "dynamic":
            sig = bake_signal(mult["value"], sr, duration)
        
        #if there is no signal yet, assign the first one
        if signal is 1:
            signal = sig
        #if there already is one, combine them with a multiplication
        else:
            signal *= sig
    return signal

def bake_modifier(modifier, sr, duration):
    """
    Returns the baked modifier
    """
    signal = 0
    for modf in modifier:
        sig = bake_signal(modf, sr, duration)
        #if there is no signal yet, assign the first one
        if signal is 0:
            signal = sig
        #if there already is one, combine them with a multiplication
        else:
            signal += sig
    return signal
def bake_signal(signal, sr, duration):
    """
    Given a dict with instructions, bake a signal and return it
    """
    if signal["type"] == "sine":
        carrier_domain = numpy.linspace(0, duration, int(sr*duration), endpoint=False) * numpy.pi * 2
        carrier_freq = signal["frequency"]
        carrier_mult = bake_multiplier(signal["multiplier"], sr, duration)
        carrier_modf = bake_modifier(signal["modifier"], sr, duration)
        baked_signal = numpy.sin(carrier_domain * carrier_freq + carrier_modf) * carrier_mult
    else:
        print("error")
        exit(-1)
    return baked_signal

def main():
    """main foo"""
    sample_rate = 44100
    dur = 4

    with open("signal_creator.json") as sig_file:
        signals = json.load(sig_file)

        for sig in signals:
            baked = bake_signal(sig, sample_rate, dur)
            play_sound(baked, sample_rate)

if __name__ == '__main__':
    main()
