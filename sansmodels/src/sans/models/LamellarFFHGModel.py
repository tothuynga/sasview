#!/usr/bin/env python
"""
	This software was developed by the University of Tennessee as part of the
	Distributed Data Analysis of Neutron Scattering Experiments (DANSE)
	project funded by the US National Science Foundation.

	If you use DANSE applications to do scientific research that leads to
	publication, we ask that you acknowledge the use of the software with the
	following sentence:

	"This work benefited from DANSE software developed under NSF award DMR-0520547."

	copyright 2008, University of Tennessee
"""

""" Provide functionality for a C extension model

	WARNING: THIS FILE WAS GENERATED BY WRAPPERGENERATOR.PY
 	         DO NOT MODIFY THIS FILE, MODIFY ..\c_extensions\lamellarFF_HG.h
 	         AND RE-RUN THE GENERATOR SCRIPT

"""

from sans.models.BaseComponent import BaseComponent
from sans_extension.c_models import CLamellarFFHGModel
import copy    
    
class LamellarFFHGModel(CLamellarFFHGModel, BaseComponent):
    """ Class that evaluates a LamellarFFHGModel model. 
    	This file was auto-generated from ..\c_extensions\lamellarFF_HG.h.
    	Refer to that file and the structure it contains
    	for details of the model.
    	List of default parameters:
         scale           = 1.0 
         t_length        = 15.0 [A]
         h_thickness     = 10.0 [A]
         sld_tail        = 4e-007 [1/A^(2)]
         sld_head        = 3e-006 [1/A^(2)]
         sld_solvent     = 6e-006 [1/A^(2)]
         background      = 0.0 [1/cm]

    """
        
    def __init__(self):
        """ Initialization """
        
        # Initialize BaseComponent first, then sphere
        BaseComponent.__init__(self)
        CLamellarFFHGModel.__init__(self)
        
        ## Name of the model
        self.name = "LamellarFFHGModel"
        ## Model description
        self.description =""" Parameters: t_length = tail length, h_thickness = head thickness,
		scale = Scale factor,
		background = incoherent Background
		sld_tail = tail scattering length density ,
		sld_solvent = solvent scattering length density.
		NOTE: The total bilayer thickness
		= 2(h_thickness+ t_length).
		"""
       
		## Parameter details [units, min, max]
        self.details = {}
        self.details['scale'] = ['', None, None]
        self.details['t_length'] = ['[A]', None, None]
        self.details['h_thickness'] = ['[A]', None, None]
        self.details['sld_tail'] = ['[1/A^(2)]', None, None]
        self.details['sld_head'] = ['[1/A^(2)]', None, None]
        self.details['sld_solvent'] = ['[1/A^(2)]', None, None]
        self.details['background'] = ['[1/cm]', None, None]

		## fittable parameters
        self.fixed=['t_length.width', 'h_thickness.width']
        
        ## parameters with orientation
        self.orientation_params =[]
   
    def clone(self):
        """ Return a identical copy of self """
        return self._clone(LamellarFFHGModel())   
   
    def run(self, x = 0.0):
        """ Evaluate the model
            @param x: input q, or [q,phi]
            @return: scattering function P(q)
        """
        
        return CLamellarFFHGModel.run(self, x)
   
    def runXY(self, x = 0.0):
        """ Evaluate the model in cartesian coordinates
            @param x: input q, or [qx, qy]
            @return: scattering function P(q)
        """
        
        return CLamellarFFHGModel.runXY(self, x)
        
    def evalDistribition(self, x = []):
        """ Evaluate the model in cartesian coordinates
            @param x: input q[], or [qx[], qy[]]
            @return: scattering function P(q[])
        """
        return CLamellarFFHGModel.evalDistribition(self, x)
        
    def calculate_ER(self):
        """ Calculate the effective radius for P(q)*S(q)
            @return: the value of the effective radius
        """       
        return CLamellarFFHGModel.calculate_ER(self)
        
    def set_dispersion(self, parameter, dispersion):
        """
            Set the dispersion object for a model parameter
            @param parameter: name of the parameter [string]
            @dispersion: dispersion object of type DispersionModel
        """
        return CLamellarFFHGModel.set_dispersion(self, parameter, dispersion.cdisp)
        
   
# End of file
