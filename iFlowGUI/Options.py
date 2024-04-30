"""
File: Options.py
Author: Andrea Bertagnoli
Date: 01/10/2024
Description: Brief description of the purpose of the file
"""

class OPT():
    '''
    '''
    def SetHarmonicFlag(self,Flag):
        self.TFAHarmFlag = Flag
        return
    def GetHarmonicFlag(self):
        return self.TFAHarmFlag

    '''
    '''
    def SetTFAxAxisUnit(self,unit):
        self.TFAxAxisUnit = unit
        return
    def GetTFAxAxisUnit(self):
        return self.TFAxAxisUnit

    '''
    '''
    def SetHarmonics(self,ListHarmonics):
        self.ListHarmonics = ListHarmonics
        return
    def GetHarmonics(self):
        return self.ListHarmonics

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

    '''
    '''
    def SetBasicPeriod(self,Value):
        self.BasicPriod = float(Value)
        return
    def GetBasicPeriod(self):
        return self.BasicPriod
    
    """
    """
    def SetScriptRun(self,value,mode):
        if mode == "WIN":
            self.win_script = value
        elif mode == "LIN":
            self.lin_script = value
        elif mode == "MAC":
            self.mac_script = value
        return
    def GetScriptRun(self,mode):
        if mode == "WIN":
            return self.win_script
        elif mode == "LIN":
            return self.lin_script
        elif mode == "MAC":
            return self.mac_script
    """
    """
    def SetRunMode(self,value,mode):
        if mode == "WIN":
            self.win_mode = value
        elif mode == "LIN":
            self.lin_mode = value
        elif mode == "MAC":
            self.mac_mode = value
        return
    def GetRunMode(self,mode):
        if mode == "WIN":
            return self.win_mode
        elif mode == "LIN":
            return self.lin_mode
        elif mode == "MAC":
            return self.mac_mode