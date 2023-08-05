# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np
import copy

class Rescale:
    """
    Rescale is a python 3 class to implement rescaling of values.
    Input:
    - data = an array of data (or at least a list of [min,max])
    - method = rescaling method
    - minmax = new scale [min,max]
    - params = additional parameters required by some rescaling methods
    How to use (example):
    xd = [400.,800.]
    obj = Rescale(data=xd) to instantiate. By default, this will set method = 'linear' and minmax = [-1.,1.]
    obj.compute() to the transformation
    obj.model to show the transformation model
    newxd = [300.,350.]
    obj.transform(newxd) to transform
    newxs = [-2.,-1.,1.,2.]
    obj.invtransform(newxs) to inverse transform
    ##########
    ##### available method
    ##########
    # method = 'linear'
    # minmax = [-1.,1.] by default
    # a simple linear transformation
    ##########
    # method = 'log10'
    # minmax = [0.,1.] by default
    # a log-linear base 10 transformation
    # Note: The transformation changes quickly when xd < minimum, which will likely to produce nan outside the boundary.
    ##########
    """
    def __init__(self,data,method='None',minmax='None',params='None'):
        self.data = np.array(data,dtype=float) # 1d np.array of data, sort not required, nan and inf is ok
        self.method = 'linear' if method is 'None' else method
        self.minmax = minmax # if None, each method will assign default values
        self.params = params # additional parameters specific for each method
        self.model = 'None' # This will be output after using self.compute()
    def transform(self,x):
        x = np.array(x)
        coef = self.model['trans']
        if self.method=='linear':
            return coef[0] + coef[1]*x
        elif self.method=='log10':
            return np.log10(coef[0] + coef[1]*x)
    def invtransform(self,x):
        x = np.array(x)
        coef = self.model['invtrans']
        if self.method=='linear':
            return coef[0] + coef[1]*x
        elif self.method=='log10':
            return coef[0] + coef[1]*np.power(10.,x)
    def compute(self):
        if self.method=='linear':
            self._compute_linear()
        elif self.method=='log10':
            self._compute_log10()
        else:
            print('model = {0} not available'.format(self.model))
    ##########
    ##### log10
    ##########
    def _compute_log10(self):
        # xs = log10(a + b * xd)
        tmpdata = self._clean_data()
        mind,maxd = tmpdata.min(),tmpdata.max()
        mins,maxs = (0.,1.) if self.minmax is 'None' else self.minmax
        print('data_minmax = ({0},{1}) : scale_minmax = ({2},{3}) : method = {4}'.format(mind,maxd,mins,maxs,self.method))
        tmp = self._log10([mind,maxd],[mins,maxs])
        intc,slope = tmp['trans']
        intc_inv,slope_inv = tmp['invtrans']
        tmp['Trans'] = 'xs = log10({0:.3E} + {1:.3E}*xd)'.format(intc,slope)
        tmp['InvTrans'] = 'xd = {0:.3E} + {1:.3E}*10^xs'.format(intc_inv,slope_inv)
        self.model = copy.deepcopy(tmp)
    def _log10(self,d,s):
        mind,maxd = d
        mins,maxs = s
        tmpa = np.power(10.,maxs) - np.power(10.,mins)
        tmpb = maxd-mind
        slope = tmpa / tmpb
        intc = np.power(10.,mins) - slope*mind
        slope_inv,intc_inv = 1./slope,-1.*intc/slope
        tmp = {'xd': (mind,maxd),
               'xs': (mins,maxs),
               'method':self.method,
               'trans':(intc,slope),
               'invtrans':(intc_inv,slope_inv),
              }
        return tmp
    ##########
    ##### linear
    ##########
    def _compute_linear(self):
        tmpdata = self._clean_data()
        mind,maxd = tmpdata.min(),tmpdata.max()
        mins,maxs = (-1.,1.) if self.minmax is 'None' else self.minmax
        print('data_minmax = ({0},{1}) : scale_minmax = ({2},{3}) : method = {4}'.format(mind,maxd,mins,maxs,self.method))
        tmp = self._linear([mind,maxd],[mins,maxs])
        intc,slope = tmp['trans']
        intc_inv,slope_inv = tmp['invtrans']
        tmp['Trans'] = 'xs = {0:.3E} + {1:.3E}*xd'.format(intc,slope)
        tmp['InvTrans'] = 'xd = {0:.3E} + {1:.3E}*xs'.format(intc_inv,slope_inv)
        self.model = copy.deepcopy(tmp)
    def _linear(self,d,s):
        mind,maxd = d
        mins,maxs = s
        slope = (maxs - mins) / (maxd - mind)
        intc = mins - slope*mind
        slope_inv,intc_inv = 1./slope,-1.*intc/slope
        tmp = {'xd': (mind,maxd),
               'xs': (mins,maxs),
               'method':self.method,
               'trans':(intc,slope),
               'invtrans':(intc_inv,slope_inv),
              }
        return tmp
    ##########
    ##########
    ##########
    def _clean_data(self):
        # subset only valid data
        m = np.isfinite(self.data)
        tmpdata = self.data[m]
        tmp = len(self.data) - len(tmpdata)
        print('Exclude {0} invalid data points'.format(tmp))
        return tmpdata
        