# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

from pysb import *
from pysb.bng import generate_network, generate_equations
from pysb.pathfinder import set_path
from pysb.simulator import ScipyOdeSimulator, BngSimulator, KappaSimulator
from pysb.util import alias_model_components
from pylab import linspace

import pandas
import seaborn
import matplotlib.pyplot as plt

def set_parameter(model, name, new_value):
	for i in model.parameters._elements:
		if name == i.name:
			i.value = new_value
	return model

def set_observable(model, pattern = '', alias = ''):
	model = alias_model_components(model)
	exec('Observable(\'' + alias + '\',' + pattern + ')')
	return model

class set_initial:
	def monomers(model, name, loc = 'cyt', new_value = 0):
		for i in model.parameters._elements:
			if name + '_' + loc.lower() == i.name:
				i.value = new_value
		return model

	def cplx(model, name, loc = 'cyt', new_value = 0):
		return set_initial.monomers(model, 't0_cplx_' + name, loc, new_value)

	def dna(model, name, loc = 'cyt', new_value = 0):
		return set_initial.monomers(model, 't0_dna_' + name, loc, new_value)

	def met(model, name, loc = 'cyt', new_value = 0):
		return set_initial.monomers(model, 't0_met_' + name, loc, new_value)

	def prot(model, name, loc = 'cyt', new_value = 0):
		return set_initial.monomers(model, 't0_prot_' + name, loc, new_value)

	def rna(model, name, loc = 'cyt', new_value = 0):
		return set_initial.monomers(model, 't0_rna_' + name, loc, new_value)

	def pattern(model, pattern, alias = 'alias_pattern', new_value = 0):
		model = alias_model_components(model)
		exec('Initial(' + pattern + ', Parameter(\'t0_' + alias + '\', ' + str(new_value) + '))')
		return model

def ode(model, start = 0, finish = 10, points = 10, path = '/opt/'):
	set_path('bng', path)
	generate_network(model)
	generate_equations(model)

	return BngSimulator(model, linspace(start, finish, points+1)).run(method = 'ode').dataframe

def modes(sims, n_runs):
	data = []
	for i in range(n_runs):
		data.append(sims.xs(i))

	avrg = 0
	for i in range(n_runs):
		avrg += data[i]
	avrg = avrg / n_runs

	stdv = 0
	for i in range(n_runs):
		stdv += (data[i] - avrg)**2
	stdv = (stdv / (n_runs-1))**0.5

	return {'sims' : data, 'avrg' : avrg, 'stdv' : stdv}

def ssa(model, start = 0, finish = 10, points = 10, n_runs = 20, path = '/opt/'):
	set_path('bng', path)
	generate_network(model)
	generate_equations(model)

	sims = BngSimulator(model, linspace(start, finish, points+1)).run(method = 'ssa', n_runs = n_runs).dataframe
	sims = modes(sims, n_runs)
	return {'sims' : sims['sims'], 'avrg' : sims['avrg'], 'stdv' : sims['stdv']}

def kasim(model, start = 0, finish = 10, points = 10, n_runs = 20, path = '/opt/'):
	set_path('kasim', path)
	sims = KappaSimulator(model, linspace(start, finish, points+1)).run(n_runs = n_runs).dataframe
	sims = modes(sims, n_runs)
	return {'sims' : sims['sims'], 'avrg' : sims['avrg'], 'stdv' : sims['stdv']}

class plot:
	def monomer(data, observable, loc = 'cyt', plt_kws = {}, *args, **kwargs):
		kind = kwargs.get('kind', None)

		observable = observable.replace('-', '_')
		if kind == 'plot':
			plt.plot(data.index, data[observable], **plt_kws)
		elif kind == 'scatter':
			plt.scatter(data.index, data[observable], **plt_kws)
		elif kind == 'fill_between':
			plt.fill_between(
				data['avrg'].index,
				data['avrg'][observable] + data['stdv'][observable],
				data['avrg'][observable] - data['stdv'][observable],
				**plt_kws)
		else:
			plt.plot(data.index, data[observable], **plt_kws)

		try:
			plt.legend(frameon = False, loc = 'right')
		except:
			pass

	def dna(data, observable, *args, **kwargs):
		plot.monomer(data, 'obs_dna_' + observable, *args, **kwargs)

	def metabolite(data, observable, loc = 'cyt', *args, **kwargs):
		plot.monomer(data, 'obs_met_' + observable + '_' + loc.lower(), *args, **kwargs)

	def protein(data, observable, loc = 'cyt', *args, **kwargs):
		plot.monomer(data, 'obs_prot_' + observable + '_' + loc.lower(), *args, **kwargs)

	def protein_complex(data, observable, loc = 'cyt', *args, **kwargs):
		plot.monomer(data, observable, loc = loc, *args, **kwargs)

	def rna(data, observable, *args, **kwargs):
		plot.monomer(data, 'obs_rna_' + observable, *args, **kwargs)

	def pattern(data, observable, plt_kws = {}, *args, **kwargs):
		plt.plot(data.index, data[observable], **plt_kws)
		try:
			plt.legend(frameon = False, loc = 'right')
		except:
			pass
