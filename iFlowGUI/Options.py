#-----------------------------------------------------------------------------#
# Name:        module1
# Purpose:
#
# Author:      user
#
# Created:     02/18/2021
# Copyright:   (c) user 2021
#              Center for Ecohydraulics
#              University of Idaho
# Licence:     <your licence>
#-----------------------------------------------------------------------------#
class OPT():
#-----------------------------------------------------------------------------#
    '''
    '''
    def SetHarmonicFlag(self,Flag):
        self.TFAHarmFlag = Flag
        return
    def GetHarmonicFlag(self):
        return self.TFAHarmFlag
#-----------------------------------------------------------------------------#
    '''
    '''
    def SetTFAxAxisUnit(self,unit):
        self.TFAxAxisUnit = unit
        return
    def GetTFAxAxisUnit(self):
        return self.TFAxAxisUnit
#-----------------------------------------------------------------------------#
    '''
    '''
    def SetHarmonics(self,ListHarmonics):
        self.ListHarmonics = ListHarmonics
        return
    def GetHarmonics(self):
        return self.ListHarmonics
#-----------------------------------------------------------------------------#
    '''
    '''
    def SetFFTcorAMP(self,List):
        self.CorrRect = float(List[0])
        self.CorrTria = float(List[1])
        self.CorrBart = float(List[2])
        self.CorrHann = float(List[3])
        self.CorrHamm = float(List[4])
        self.CorrFlat = float(List[5])
        return
    def GetFFTcorAMP(self,Case):
        if Case == 0:
            return self.CorrRect
        elif Case == 1:
            return self.CorrTria
        elif Case == 2:
            return self.CorrBart
        elif Case == 3:
            return self.CorrHann
        elif Case == 4:
            return self.CorrHamm
        elif Case == 5:
            return self.CorrFlat
#-----------------------------------------------------------------------------#
    '''
    '''
    def SetBasicPeriod(self,Value):
        self.BasicPriod = float(Value)
        return
    def GetBasicPeriod(self):
        return self.BasicPriod