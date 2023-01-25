
import csv
from pathlib import Path
import numpy as np


class Step():
    def __init__(self, fname):
        self.scountx = None
        self.scounty = None
        self.minidx = None
        self.maxidx = None
        self.dx = None
        self.dy = None
        self.dt = None
        self.unit_dist = None
        self.unit_pres = None
        self.unit_time = None

        self.context = None     # Should be either 'R' or 'L'
        
        self.data = None
        data_max = None
    
        with open(fname, "r") as f:
            lines = f.readlines()
    
            # Read the fixed part
            i = 0
            while i < len(lines):
                line = lines[i]

                ##---------------------------------------------------------
                # Read the data dimensions in x, y and t
                #
                if line.startswith('SensCountX'):
                    self.scountx = int(line.split('=')[1])
            
                if line.startswith('SensCountY'):
                    self.scounty = int(line.split('=')[1])
            
                if line.startswith('MinIdx'):
                    self.minidx = int(line.split('=')[1])
            
                if line.startswith('MaxIdx'):
                    self.maxidx = int(line.split('=')[1])

                ##---------------------------------------------------------
                # Read the data resolution in x, y and t
                #
                if line.startswith('LDistX'):
                    self.dx = float(line.split('=')[1])

                if line.startswith('LDistY'):
                    self.dy = float(line.split('=')[1])

                if line.startswith('TimeDiff'):
                    self.dt = float(line.split('=')[1])

                ##---------------------------------------------------------
                # Read the units
                #
                if line.startswith('UnitDistance'):
                    self.unit_dist = (line.split('=')[1]).strip()
                    assert self.unit_dist == 'mm'

                if line.startswith('UnitPressure'):
                    self.unit_pres = (line.split('=')[1]).strip()
                    assert self.unit_pres == 'N/cm2'

                if line.startswith('UnitTime'):
                    self.unit_time = (line.split('=')[1]).strip()
                    assert self.unit_time == 'ms'

                ##---------------------------------------------------------
                # Read the step context (R/L)
                #
                if line.startswith('FootSide'):
                    self.context = (line.split('=')[1]).strip()
                    assert self.context in 'RL'

                ##---------------------------------------------------------
                # Read the pressure data maximum
                #
                if line == '[Data]\n':
                    assert (self.scountx is not None) and (self.scounty is not None)
                    data_max = self.__read_frame(lines, i+1, self.scountx, self.scounty)
                    i += self.scountx
            
                i += 1
        
            assert (self.scountx is not None) and \
                   (self.scounty is not None) and \
                   (self.minidx is not None) and \
                   (self.maxidx is not None)

            assert (self.dx is not None) and \
                   (self.dy is not None) and \
                   (self.dy is not None)

            assert (self.unit_dist is not None) and \
                   (self.unit_pres is not None) and \
                   (self.unit_time is not None)

            assert (self.context is not None) and \
                   (data_max is not None)
            
            # Read the dynamic part
            i = 0
            self.data = np.zeros((self.scountx, self.scounty, self.maxidx-self.minidx+1))
            frame_id = self.minidx
            
            while i < len(lines):
                line = lines[i]
                
                if line == ('[Data%i]\n' % frame_id):
                    self.data[:,:,frame_id-self.minidx] = self.__read_frame(lines, i+1, self.scountx, self.scounty)
                    i += self.scountx
                    frame_id += 1
                    
                i += 1
                
            assert frame_id == self.maxidx+1
            # Make sure that data_max equals the maximum of self.data over all timeframes
            assert not np.any(self.data.max(axis=2) - data_max)

        
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


class Session():
    def __init__(self, fname_prefix):
        self.steps = []
        p = Path(fname_prefix + '*.apd')
        step_pathes = list(p.parent.glob(p.name))
        assert(len(step_pathes) > 0)

        for i in range(len(step_pathes)):
            # Note that we are not simply iterating over step_pathes, but
            # generating then according to the template. This is a more
            # robust approach.
            step_path_templ = Path('%s[LR]%i.apd' % (fname_prefix, i+1))
            step_path_matches = list(step_path_templ.parent.glob(step_path_templ.name))
            assert len(step_path_matches) == 1
            self.steps.append(Step(step_path_matches[0]))

            # Make sure that the context in the file name and within the file itself match
            assert str(step_path_matches[0]) == '%s%s%i.apd' % (fname_prefix, self.steps[-1].context, i + 1)

def zeropad(nr, nc, nf, inp):
    """
    Pad the input sides so that the new size is nr * nc * nf. For the nr and nc
    dimensions split the padding approximately evenly before/after, for the nf
    dimension add all the padding after.
    """
    r, c, f = inp.shape
    dr = nr - r
    dc = nc - c

    r_before = dr // 2
    c_before = dc // 2

    r_after = dr - r_before
    c_after = dc - c_before

    return np.pad(inp, ((r_before, r_after), (c_before, c_after), (0, nf-f)), constant_values=-1)
