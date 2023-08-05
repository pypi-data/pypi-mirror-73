# Rescale

pip install rescalex

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
