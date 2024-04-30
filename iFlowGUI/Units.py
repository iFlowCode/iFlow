"""
Description
"""
import numpy as np
# 'Temperature ('+u'\N{DEGREE SIGN}'+'C)'
class UNIT():

    def SetTime(self,value):
        self.time_unit = value
        return
    def GetTime(self):
        return self.time_unit
    
    def ConvertTime(self,array):
        if self.time_unit == "s":
            return array
        elif self.time_unit == "min":
            return array / 60.0
        elif self.time_unit == "h":
            return array / 3660.0
        elif self.time_unit == "d":
            return array / 86400.0
        
    def LabelTime(self):
        if self.time_unit == "s":
            return "Time (s)"
        elif self.time_unit == "min":
            return "Time (min)"
        elif self.time_unit == "h":
            return "Time (h)"
        elif self.time_unit == "d":
            return "Time (d)"
        
    def SetTemperature(self,value):
        self.temperature_unit = value
        return
    def GetTemperature(self):
        return self.temperature_unit
    
    def ConvertTemperature(self,array):
        if self.temperature_unit == "C":
            return array
        elif self.temperature_unit == "K":
            return (array + 273.15)
        elif self.temperature_unit == "F":
            return (array * 9.0 / 5.0) + 32.0
        
    def LabelTemperature(self):
        if self.temperature_unit == "C":
            return 'Temperature ('+u'\N{DEGREE SIGN}'+'C)'
        elif self.temperature_unit == "K":
            return 'Temperature ('+u'\N{DEGREE SIGN}'+'K)'
        elif self.temperature_unit == "F":
            return 'Temperature ('+u'\N{DEGREE SIGN}'+'F)'
        
    def ConvertAmplitude(self,array):
        if self.temperature_unit == "C":
            return array
        elif self.temperature_unit == "K":
            return (array + 273.15)
        elif self.temperature_unit == "F":
            return (array * 9.0 / 5.0) + 32.0
        
    def LabelAmplitude(self):
        if self.temperature_unit == "C":
            return 'Amplitude ('+u'\N{DEGREE SIGN}'+'C)'
        elif self.temperature_unit == "K":
            return 'Amplitude ('+u'\N{DEGREE SIGN}'+'K)'
        elif self.temperature_unit == "F":
            return 'Amplitude ('+u'\N{DEGREE SIGN}'+'F)'
        
    def SetFrequency(self,value):
        self.frequency_unit = value
        return
    def GetFrequency(self):
        return self.frequency_unit
    
    def ConvertFrequency(self,array):
        if self.frequency_unit == "Hz":
            return array
        elif self.frequency_unit == "h":
            return array * 3600.0
        elif self.frequency_unit == "d":
            return array * 86400.0
        
    def LabelFrequency(self):
        if self.frequency_unit == "Hz":
            return "Frequency (Hz)"
        elif self.frequency_unit == "h":
            return "Frequency (h$^{-1}$)"
        elif self.frequency_unit == "d":
            return "Frequency (d$^{-1}$)"
        
    def SetAngle(self,value):
        self.angle_unit = value
        return
    def GetAngle(self):
        return self.angle_unit
    
    def ConvertAngle(self,array):
        if self.angle_unit == "rad":
            return array
        elif self.angle_unit == "degree":
            return array / 2 / np.pi * 360.0
        
    def LabelPhase(self):
        if self.angle_unit == "rad":
            return "Phase (rad)"
        elif self.angle_unit == "degree":
            return "Phase (degree)"
        
    def LabelDiffPhase(self):
        if self.angle_unit == "rad":
            return "DiffPhase (rad)"
        elif self.angle_unit == "degree":
            return "DiffPhase (degree)"
    
    def SetLenght(self,value):
        self.lenght_unit = value
        return
    def GetLenght(self):
        return self.lenght_unit
    
    def ConvertLenght(self,array):
        if self.lenght_unit == "m":
            return array
        elif self.lenght_unit == "cm":
            return array * 100.0
        elif self.lenght_unit == "mm":
            return array * 1000.0
        elif self.lenght_unit == "in":
            return array * 39.3701
        elif self.lenght_unit == "ft":
            return array * 3.28084
        
    def LabelLenght(self):
        if self.lenght_unit == "m":
            return "Elevation (m)"
        elif self.lenght_unit == "cm":
            return "Elevation (cm)"
        elif self.lenght_unit == "mm":
            return "Elevation (mm)"
        elif self.lenght_unit == "in":
            return "Elevation (in)"
        elif self.lenght_unit == "ft":
            return "Elevation (ft)"
        
    def ConvertThermDiff(self,array):
        if self.lenght_unit == "m":
            if self.time_unit == "s":
                return array # m2 s-1
            elif self.time_unit == "min":
                return array * 60.0 # m2 min-1
            elif self.time_unit == "h":
                return array * 3600.0 # m2 h-1
            elif self.time_unit == "d":
                return array * 86400.0 # m2 d-1
        elif self.lenght_unit == "cm":
            if self.time_unit == "s":
                return array * 100 ** 2 # cm2 s-1
            elif self.time_unit == "min":
                return array * 60.0 * 100 ** 2 # cm2 min-1
            elif self.time_unit == "h":
                return array * 3600.0 * 100 ** 2 # cm2 h-1
            elif self.time_unit == "d":
                return array * 86400.0 * 100 ** 2 # cm2 d-1
        elif self.lenght_unit == "mm":
            if self.time_unit == "s":
                return array * 1000 ** 2 # mm2 s-1
            elif self.time_unit == "min":
                return array * 60.0 * 1000 ** 2 # mm2 min-1
            elif self.time_unit == "h":
                return array * 3600.0 * 1000 ** 2 # mm2 h-1
            elif self.time_unit == "d":
                return array * 86400.0 * 1000 ** 2 # mm2 d-1
        elif self.lenght_unit == "in":
            if self.time_unit == "s":
                return array * 39.3701 ** 2 # in2 s-1
            elif self.time_unit == "min":
                return array * 60.0 * 39.3701 ** 2 # in2 min-1
            elif self.time_unit == "h":
                return array * 3600.0 * 39.3701 ** 2 # in2 h-1
            elif self.time_unit == "d":
                return array * 86400.0 * 39.3701 ** 2 # in2 d-1
        elif self.lenght_unit == "ft":
            if self.time_unit == "s":
                return array * 3.28084 ** 2 # ft2 s-1
            elif self.time_unit == "min":
                return array * 60.0 * 3.28084 ** 2 # ft2 min-1
            elif self.time_unit == "h":
                return array * 3600.0 * 3.28084 ** 2 # ft2 h-1
            elif self.time_unit == "d":
                return array * 86400.0 * 3.28084 ** 2 # ft2 d-1
        
    def LabelThermDiff(self):
        if self.lenght_unit == "m":
            if self.time_unit == "s":
                return "k$_{e}$ (m$^{2}$ s$^{-1}$)" # m2 s-1
            elif self.time_unit == "min":
                return "k$_{e}$ (m$^{2}$ min$^{-1}$)" # m2 min-1
            elif self.time_unit == "h":
                return "k$_{e}$ (m$^{2}$ h$^{-1}$)" # m2 h-1
            elif self.time_unit == "d":
                return "k$_{e}$ (m$^{2}$ d$^{-1}$)" # m2 d-1
        elif self.lenght_unit == "cm":
            if self.time_unit == "s":
                return "k$_{e}$ (cm$^{2}$ s$^{-1}$)" # cm2 s-1
            elif self.time_unit == "min":
                return "k$_{e}$ (cm$^{2}$ min$^{-1}$)" # cm2 min-1
            elif self.time_unit == "h":
                return "k$_{e}$ (cm$^{2}$ h$^{-1}$)" # cm2 h-1
            elif self.time_unit == "d":
                return "k$_{e}$ (cm$^{2}$ d$^{-1}$)" # cm2 d-1
        elif self.lenght_unit == "mm":
            if self.time_unit == "s":
                return "k$_{e}$ (mm$^{2}$ s$^{-1}$)" # mm2 s-1
            elif self.time_unit == "min":
                return "k$_{e}$ (mm$^{2}$ min$^{-1}$)" # mm2 min-1
            elif self.time_unit == "h":
                return "k$_{e}$ (mm$^{2}$ h$^{-1}$)" # mm2 h-1
            elif self.time_unit == "d":
                return "k$_{e}$ (mm$^{2}$ d$^{-1}$)" # mm2 d-1
        elif self.lenght_unit == "in":
            if self.time_unit == "s":
                return "k$_{e}$ (in$^{2}$ s$^{-1}$)" # in2 s-1
            elif self.time_unit == "min":
                return "k$_{e}$ (in$^{2}$ min$^{-1}$)" # in2 min-1
            elif self.time_unit == "h":
                return "k$_{e}$ (in$^{2}$ h$^{-1}$)" # in2 h-1
            elif self.time_unit == "d":
                return "k$_{e}$ (in$^{2}$ d$^{-1}$)" # in2 d-1
        elif self.lenght_unit == "ft":
            if self.time_unit == "s":
                return "k$_{e}$ (ft$^{2}$ s$^{-1}$)" # ft2 s-1
            elif self.time_unit == "min":
                return "k$_{e}$ (ft$^{2}$ min$^{-1}$)" # ft2 min-1
            elif self.time_unit == "h":
                return "k$_{e}$ (ft$^{2}$ h$^{-1}$)" # ft2 h-1
            elif self.time_unit == "d":
                return "k$_{e}$ (ft$^{2}$ d$^{-1}$)" # ft2 d-1

    def LabelDiff(self):
        if self.lenght_unit == "m":
            if self.time_unit == "s":
                return "k (m$^{2}$ s$^{-1}$)" # m2 s-1
            elif self.time_unit == "min":
                return "k (m$^{2}$ min$^{-1}$)" # m2 min-1
            elif self.time_unit == "h":
                return "k (m$^{2}$ h$^{-1}$)" # m2 h-1
            elif self.time_unit == "d":
                return "k (m$^{2}$ d$^{-1}$)" # m2 d-1
        elif self.lenght_unit == "cm":
            if self.time_unit == "s":
                return "k (cm$^{2}$ s$^{-1}$)" # cm2 s-1
            elif self.time_unit == "min":
                return "k (cm$^{2}$ min$^{-1}$)" # cm2 min-1
            elif self.time_unit == "h":
                return "k (cm$^{2}$ h$^{-1}$)" # cm2 h-1
            elif self.time_unit == "d":
                return "k (cm$^{2}$ d$^{-1}$)" # cm2 d-1
        elif self.lenght_unit == "mm":
            if self.time_unit == "s":
                return "k (mm$^{2}$ s$^{-1}$)" # mm2 s-1
            elif self.time_unit == "min":
                return "k (mm$^{2}$ min$^{-1}$)" # mm2 min-1
            elif self.time_unit == "h":
                return "k (mm$^{2}$ h$^{-1}$)" # mm2 h-1
            elif self.time_unit == "d":
                return "k (mm$^{2}$ d$^{-1}$)" # mm2 d-1
        elif self.lenght_unit == "in":
            if self.time_unit == "s":
                return "k (in$^{2}$ s$^{-1}$)" # in2 s-1
            elif self.time_unit == "min":
                return "k (in$^{2}$ min$^{-1}$)" # in2 min-1
            elif self.time_unit == "h":
                return "k (in$^{2}$ h$^{-1}$)" # in2 h-1
            elif self.time_unit == "d":
                return "k (in$^{2}$ d$^{-1}$)" # in2 d-1
        elif self.lenght_unit == "ft":
            if self.time_unit == "s":
                return "k (ft$^{2}$ s$^{-1}$)" # ft2 s-1
            elif self.time_unit == "min":
                return "k (ft$^{2}$ min$^{-1}$)" # ft2 min-1
            elif self.time_unit == "h":
                return "k (ft$^{2}$ h$^{-1}$)" # ft2 h-1
            elif self.time_unit == "d":
                return "k (ft$^{2}$ d$^{-1}$)" # ft2 d-1
            
    def ConvertThermVel(self,array):
        if self.lenght_unit == "m":
            if self.time_unit == "s":
                return array # m s-1
            elif self.time_unit == "min":
                return array * 60.0 # m min-1
            elif self.time_unit == "h":
                return array * 3600.0 # m2h-1
            elif self.time_unit == "d":
                return array * 86400.0 # m d-1
        elif self.lenght_unit == "cm":
            if self.time_unit == "s":
                return array * 100# cm s-1
            elif self.time_unit == "min":
                return array * 60.0 * 100 # cm min-1
            elif self.time_unit == "h":
                return array * 3600.0 * 100 # cm h-1
            elif self.time_unit == "d":
                return array * 86400.0 * 100 # cm d-1
        elif self.lenght_unit == "mm":
            if self.time_unit == "s":
                return array * 1000 # mm s-1
            elif self.time_unit == "min":
                return array * 60.0 * 1000 # mm min-1
            elif self.time_unit == "h":
                return array * 3600.0 * 1000 # mm h-1
            elif self.time_unit == "d":
                return array * 86400.0 * 1000 # mm d-1
        elif self.lenght_unit == "in":
            if self.time_unit == "s":
                return array * 39.3701 # in s-1
            elif self.time_unit == "min":
                return array * 60.0 * 39.3701 # in min-1
            elif self.time_unit == "h":
                return array * 3600.0 * 39.3701 # in h-1
            elif self.time_unit == "d":
                return array * 86400.0 * 39.3701 # in d-1
        elif self.lenght_unit == "ft":
            if self.time_unit == "s":
                return array * 3.28084 # ft s-1
            elif self.time_unit == "min":
                return array * 60.0 * 3.28084 # ft min-1
            elif self.time_unit == "h":
                return array * 3600.0 * 3.28084 # ft h-1
            elif self.time_unit == "d":
                return array * 86400.0 * 3.28084 # ft d-1
        
    def LabelThermVel(self):
        if self.lenght_unit == "m":
            if self.time_unit == "s":
                return "v$_{t}$ (m s$^{-1}$)" # m s-1
            elif self.time_unit == "min":
                return "v$_{t}$ (m min$^{-1}$)" # m min-1
            elif self.time_unit == "h":
                return "v$_{t}$ (m h$^{-1}$)" # m h-1
            elif self.time_unit == "d":
                return "v$_{t}$ (m d$^{-1}$)" # m d-1
        elif self.lenght_unit == "cm":
            if self.time_unit == "s":
                return "v$_{t}$ (cm s$^{-1}$)" # cm s-1
            elif self.time_unit == "min":
                return "v$_{t}$ (cm min$^{-1}$)" # cm min-1
            elif self.time_unit == "h":
                return "v$_{t}$ (cm h$^{-1}$)" # cm h-1
            elif self.time_unit == "d":
                return "v$_{t}$ (cm d$^{-1}$)" # cm d-1
        elif self.lenght_unit == "mm":
            if self.time_unit == "s":
                return "v$_{t}$ (mm s$^{-1}$)" # mm s-1
            elif self.time_unit == "min":
                return "v$_{t}$ (mm min$^{-1}$)" # mm min-1
            elif self.time_unit == "h":
                return "v$_{t}$ (mm h$^{-1}$)" # mm h-1
            elif self.time_unit == "d":
                return "v$_{t}$ (mm d$^{-1}$)" # mm d-1
        elif self.lenght_unit == "in":
            if self.time_unit == "s":
                return "v$_{t}$ (in s$^{-1}$)" # in s-1
            elif self.time_unit == "min":
                return "v$_{t}$ (in min$^{-1}$)" # in min-1
            elif self.time_unit == "h":
                return "v$_{t}$ (in h$^{-1}$)" # in h-1
            elif self.time_unit == "d":
                return "v$_{t}$ (in d$^{-1}$)" # in d-1
        elif self.lenght_unit == "ft":
            if self.time_unit == "s":
                return "v$_{t}$ (ft s$^{-1}$)" # ft s-1
            elif self.time_unit == "min":
                return "v$_{t}$ (ft min$^{-1}$)" # ft min-1
            elif self.time_unit == "h":
                return "v$_{t}$ (ft h$^{-1}$)" # ft h-1
            elif self.time_unit == "d":
                return "v$_{t}$ (ft d$^{-1}$)" # ft d-1

    def LabelFlux(self):
        if self.lenght_unit == "m":
            if self.time_unit == "s":
                return "q (m s$^{-1}$)" # m s-1
            elif self.time_unit == "min":
                return "q (m min$^{-1}$)" # m min-1
            elif self.time_unit == "h":
                return "q (m h$^{-1}$)" # m h-1
            elif self.time_unit == "d":
                return "q (m d$^{-1}$)" # m d-1
        elif self.lenght_unit == "cm":
            if self.time_unit == "s":
                return "q (cm s$^{-1}$)" # cm s-1
            elif self.time_unit == "min":
                return "q (cm min$^{-1}$)" # cm min-1
            elif self.time_unit == "h":
                return "q (cm h$^{-1}$)" # cm h-1
            elif self.time_unit == "d":
                return "q (cm d$^{-1}$)" # cm d-1
        elif self.lenght_unit == "mm":
            if self.time_unit == "s":
                return "q (mm s$^{-1}$)" # mm s-1
            elif self.time_unit == "min":
                return "q (mm min$^{-1}$)" # mm min-1
            elif self.time_unit == "h":
                return "q (mm h$^{-1}$)" # mm h-1
            elif self.time_unit == "d":
                return "q (mm d$^{-1}$)" # mm d-1
        elif self.lenght_unit == "in":
            if self.time_unit == "s":
                return "q (in s$^{-1}$)" # in s-1
            elif self.time_unit == "min":
                return "q (in min$^{-1}$)" # in min-1
            elif self.time_unit == "h":
                return "q (in h$^{-1}$)" # in h-1
            elif self.time_unit == "d":
                return "q (in d$^{-1}$)" # in d-1
        elif self.lenght_unit == "ft":
            if self.time_unit == "s":
                return "q (ft s$^{-1}$)" # ft s-1
            elif self.time_unit == "min":
                return "q (ft min$^{-1}$)" # ft min-1
            elif self.time_unit == "h":
                return "q (ft h$^{-1}$)" # ft h-1
            elif self.time_unit == "d":
                return "q (ft d$^{-1}$)" # ft d-1