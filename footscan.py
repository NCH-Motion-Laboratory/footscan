
import csv
import numpy as np
import matplotlib.pylab as plt


class Step():
    def __init__(self, fname):
        self.scountx = None
        self.scounty = None
        self.minidx = None
        self.maxidx = None
        
        self.dtis = None
        dti = None
    
        with open(fname, "r") as f:
            lines = f.readlines()
    
            # Read the fixed part
            i = 0
            while i < len(lines):
                line = lines[i]
        
                if line.startswith('SensCountX'):
                    self.scountx = int(line.split('=')[1])
            
                if line.startswith('SensCountY'):
                    self.scounty = int(line.split('=')[1])
            
                if line.startswith('MinIdx'):
                    self.minidx = int(line.split('=')[1])
            
                if line.startswith('MaxIdx'):
                    self.maxidx = int(line.split('=')[1])
            
                if line == '[Data]\n':
                    assert (self.scountx is not None) and (self.scounty is not None)
                    dti = self.__read_frame(lines, i+1, self.scountx, self.scounty)
                    i += self.scountx
            
                i += 1
        
            assert (self.scountx is not None) and \
                    (self.scounty is not None) and \
                    (self.minidx is not None) and \
                    (self.maxidx is not None) and \
                    (dti is not None)
            
            # Read the dynamic part
            i = 0
            self.dtis = np.zeros((self.scountx, self.scounty, self.maxidx-self.minidx+1))
            frame_id = self.minidx
            
            while i < len(lines):
                line = lines[i]
                
                if line == ('[Data%i]\n' % frame_id):
                    self.dtis[:,:,frame_id-self.minidx] = self.__read_frame(lines, i+1, self.scountx, self.scounty)
                    i += self.scountx
                    frame_id += 1
                    
                i += 1
                
            assert frame_id == self.maxidx+1
            assert not np.any(self.dtis.max(axis=2) - dti)

            self.dtis[self.dtis==-1] = 0
        
        
    def __read_frame(self, lines, line_num, scountx, scounty):
        """ Read a single frame starting at the line line_num
        """
        
        dt = []
        r = csv.reader(lines[line_num:line_num+scountx], delimiter='\t', quoting=csv.QUOTE_NONNUMERIC)
        
        for row in r:
            dt.append(row)
            
        res = np.array(dt)
        assert res.shape == (scountx, scounty)
        
        return res 
    