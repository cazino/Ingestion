# -*- coding: utf-8 -*-
import subprocess


class mp3_info:
    """
    Display information about a mp3 file
    """
    
    def __init__(self, file_path):
        self.file_path = file_path
            

    def get_size(self):
        """
        Ecnode the wav file in mp3
        """
        instr = "mp3info -p \'\%%k\' \'%s\'" % self.file_path
        subP = subprocess.Popen(instr,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        returnCode = subP.wait()
        (stdout,stderr) = subP.communicate()
        return (stdout,returnCode)
        

if __name__ == "__main__"   :
    encoder = mp3_info('/home/kazou/dev/mp3/ingestion/tests/data/testfiles/batch2/3300450000368/FR1Q30800001.mp3')
    print encoder.getInfo()
