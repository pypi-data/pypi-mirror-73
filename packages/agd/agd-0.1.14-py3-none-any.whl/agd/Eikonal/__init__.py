# Copyright 2020 Jean-Marie Mirebeau, University Paris-Sud, CNRS, University Paris-Saclay
# Distributed WITHOUT ANY WARRANTY. Licensed under the Apache License, Version 2.0, see http://www.apache.org/licenses/LICENSE-2.0

"""
The Eikonal package embeds CPU and GPU numerical solvers of (generalized) eikonal 
equations. These are variants of the fast marching and fast sweeping method, based on 
suitable discretizations of the PDE, and written and C++.

Please see the illustrative notebooks for detailed usage instructions and examples:
https://github.com/Mirebeau/AdaptiveGridDiscretizations

Main object : 
- dictIn : a dictionary-like structure, used to gathers the arguments of the 
eikonal solver, and eventually call it.
"""

import numpy as np
import importlib
import functools

from .LibraryCall import GetBinaryDir
from .run_detail import Cache
from .DictIn import dictIn,dictOut,CenteredLinspace


def VoronoiDecomposition(arr,mode=None,*args,**kwargs):
	"""
	Calls the FileVDQ library to decompose the provided quadratic form(s),
	as based on Voronoi's first reduction of quadratic forms.
	- mode : 'cpu' or 'gpu' or 'gpu_transfer'. 
	 Defaults to VoronoiDecomposition.default_mode if specified, or to gpu/cpu adequately.
	- args,kwargs : passed to gpu decomposition method
	"""
	from ..AutomaticDifferentiation.cupy_generic import cupy_set,cupy_get,from_cupy
	if mode is None: mode = VoronoiDecomposition.default_mode
	if mode is None: mode = 'gpu' if from_cupy(arr) else 'cpu'
	if mode=='gpu':
		from .HFM_CUDA.VoronoiDecomposition import VoronoiDecomposition as VD
		return VD(arr,*args,**kwargs)
	elif mode=='gpu_transfer':
		from .HFM_CUDA.VoronoiDecomposition import VoronoiDecomposition as VD
		return cupy_get(VD(cupy_set(arr),*args,**kwargs),iterables=(tuple,))
	elif mode=='cpu':
		from ..Metrics import misc
		from . import FileIO
		bin_dir = GetBinaryDir("FileVDQ",None)
		vdqIn ={'tensors':np.moveaxis(misc.flatten_symmetric_matrix(arr),0,-1)}
		vdqOut = FileIO.WriteCallRead(vdqIn, "FileVDQ", bin_dir)
		return np.moveaxis(vdqOut['weights'],-1,0),np.moveaxis(vdqOut['offsets'],[-1,-2],[0,1]).astype(int)
	else: raise ValueError(f"VoronoiDecomposition unsupported mode {mode}")

VoronoiDecomposition.default_mode = None