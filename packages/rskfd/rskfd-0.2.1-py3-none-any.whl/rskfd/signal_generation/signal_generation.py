# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 2020

(C) 2020, Florian Ramian
"""


def CreateWGNSignal( NoisePower=-40, RecordLength=4096 ):
    # function returns white Gaussian noise baseband signal
    #  (Gaussian on I and Gaussian on Q, Rayleigh distributed on magnitude)
    # NoisePower:   mean power in dBm
    # RecordLength: Record length in samples
    # returns the noise vector (scaled in Volts)

    import numpy
    import logging

    # dBm to Volts^2, 10^(np/10)/1000*50; divided by 2, because of I and Q
    std_dev = numpy.sqrt( numpy.power( 10, NoisePower/10)/40)
    data_real = numpy.random.normal( 0, std_dev, RecordLength)
    data_imag = numpy.random.normal( 0, std_dev, RecordLength)
    data = data_real + 1j * data_imag
    
    logging.info( "WGN vector length: "+str(RecordLength)+"; power: "+str(numpy.log10(numpy.mean(numpy.square(numpy.abs(data)))/50)*10+30)+" dBm")
    
    return data



if __name__ == "__main__":
    # execute only if run as a script
    pass   