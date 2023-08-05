# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

from pysb.bng import generate_network, generate_equations
from pysb.export import export
from pysb.pathfinder import set_path

def to_kappa(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'kappa'))

def to_bngl(model, outfile, path):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'bngl'))
