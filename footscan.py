
import csv
from pathlib import Path
import numpy as np


class Step():
    def __init__(self, fname):
        """
        Note that footscan's xy axis differ from the matplotlib's convention
        (footscan's x is matplotlib's y and vice versa), so we swap these
        when reading from file.
        """
        self.sizex = None
        self.sizey = None
        self.dx = None
        self.dy = None
        self.dt = None
        self.unit_dist = None
        self.unit_pres = None
        self.unit_time = None

        self.context = None     # Should be either 'R' or 'L'
        self.data = None

        # Used for plotting, compatible with matshow()
        self.origin = 'upper'
        self.extent = None

        # center of pressure coords
        self.cop_x = None
        self.cop_y = None

        minidx = None
        maxidx = None
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
                    self.sizey = int(line.split('=')[1])
            
                if line.startswith('SensCountY'):
                    self.sizex = int(line.split('=')[1])
            
                if line.startswith('MinIdx'):
                    minidx = int(line.split('=')[1])
            
                if line.startswith('MaxIdx'):
                    maxidx = int(line.split('=')[1])

                ##---------------------------------------------------------
                # Read the data resolution in x, y and t
                #
                if line.startswith('LDistX'):
                    self.dy = float(line.split('=')[1])

                if line.startswith('LDistY'):
                    self.dx = float(line.split('=')[1])

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
                    assert (self.sizey is not None) and (self.sizex is not None)
                    data_max = self.__read_frame(lines, i+1, self.sizey, self.sizex)
                    i += self.sizey
            
                i += 1
        
            assert (self.sizex is not None) and \
                   (self.sizey is not None) and \
                   (minidx is not None) and \
                   (maxidx is not None)

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
            self.data = np.zeros((self.sizey, self.sizex, maxidx-minidx+1))
            frame_id = minidx
            
            while i < len(lines):
                line = lines[i]
                
                if line == ('[Data%i]\n' % frame_id):
                    self.data[:,:,frame_id-minidx] = self.__read_frame(lines, i+1, self.sizey, self.sizex)
                    i += self.sizey
                    frame_id += 1
                    
                i += 1
                
            assert frame_id == maxidx+1
            # Make sure that data_max equals the maximum of self.data over all timeframes
            assert not np.any(self.data.max(axis=2) - data_max)

            self.extent = (-self.dx*0.5, self.dx*(self.sizex-0.5), self.dy*(self.sizey-0.5), -self.dy*0.5)

            # Compute the center-of-pressure trajectory
            z_data = self.data.copy()
            z_data[z_data==-1] = 0

            mx, my = np.meshgrid(self.dx * np.arange(self.sizex), self.dy * np.arange(self.sizey))
            # extend mx, my to 3D
            mx = np.repeat(mx[:, :, np.newaxis], z_data.shape[2], axis=2)
            my = np.repeat(my[:, :, np.newaxis], z_data.shape[2], axis=2)

            self.cop_x = np.sum(z_data * mx, axis=(0, 1)) / np.sum(z_data, axis=(0, 1))
            self.cop_y = np.sum(z_data * my, axis=(0, 1)) / np.sum(z_data, axis=(0, 1))


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
