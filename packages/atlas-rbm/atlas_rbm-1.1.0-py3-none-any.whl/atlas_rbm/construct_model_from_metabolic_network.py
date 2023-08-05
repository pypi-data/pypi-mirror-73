# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

from pysb import *
from pysb.util import *
from pysb.core import *

import re
import pandas

def read_network(infile_path):
	with open(infile_path, 'r') as infile:
		data = pandas.read_csv(infile, delimiter = '\t', header = 0, comment = '#')

	return data

def check_network(data):
	data[data.duplicated(['REACTION'])].to_csv('./conflicting_reactions.txt', sep = '\t', index = False)
	data = data[~data.duplicated(['REACTION'], keep = 'first')]

	return data

def expand_network(infile_path, path = 'expanded.txt'):
	data = read_network(infile_path)

	with open(path, 'w+') as outfile:
		for enzyme, reaction in zip(data.iloc[:,0], data.iloc[:,1]):
			outfile.write('{:s}\tGENE_PROD\t{:s}\tRXN\n'.format(enzyme, reaction))
	with open(path, 'a') as outfile:
		for reaction, substrates in zip(data.iloc[:,1], data.iloc[:,2]):
			for substrate in substrates.split(', '):
				outfile.write('{:s}\tRXN\t{:s}\tMET\n'.format(reaction, substrate))
	with open(path, 'a') as outfile:
		for reaction, products in zip(data.iloc[:,1], data.iloc[:,3]):
			for product in products.split(', '):
				outfile.write('{:s}\tRXN\t{:s}\tMET\n'.format(reaction, product))

	return None

def monomers_from_metabolic_network(model, data, verbose = False):
	# find unique metabolites and correct names
	tmp = list(data.iloc[:, 2].values) + list(data.iloc[:, 3].values)
	tmp = [ ' '.join(x.replace('PER-', '').replace('EX-', '').split(',')) for x in tmp]

	metabolites = list(set(' '.join(tmp).split(' ')))
	for index, met in enumerate(metabolites):
		if met[0].isdigit():
			metabolites[index] = '_' + met

	code = "Monomer('met',\n" \
		"	['name', 'loc', 'prot'],\n" \
		"	{{ 'name' : [ {:s} ],\n" \
		"	'loc' : ['cyt', 'per', 'ex']}})"

	code = code.format(', '.join([ '\'' + x.replace('-', '_') + '\'' for x in sorted(metabolites)]))

	if verbose:
		print(code)
	exec(code.replace('\t', ' ').replace('\n', ' '))

	# find unique proteins, protein complexes and correct names
	tmp = list(data.iloc[:, 0].values)
	tmp = [ x.replace('[', '').replace(']', '').split(',') if x.startswith('[') else [x] for x in tmp ]
	tmp = [ i for j in tmp for i in j ]
	tmp = [ ' '.join(x.replace('PER-', '').replace('MEM-', '').split(', ')) for x in tmp]

	complexes = []
	p_monomers = []
	proteins = list(set(' '.join(tmp).split(' ')))
	for index, protein in enumerate(proteins):
		if protein[0].isdigit():
			protein[index] = '_' + protein
		if 'CPLX' in protein:
			complexes.append(protein)
		else:
			if 'spontaneous' != protein:
				p_monomers.append(protein)

	code = "Monomer('prot',\n" \
		"	['name', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
		"	{{ 'name' : [ {:s} ],\n" \
		"	'loc' : ['cyt', 'mem', 'per', 'ex']}})"

	code = code.format(', '.join([ '\'' + x.replace('-', '_') + '\'' for x in sorted(p_monomers)]))

	if verbose:
		print(code)
	exec(code.replace('\t', ' ').replace('\n', ' '))

	if len(complexes) > 0:
		code = "Monomer('cplx',\n" \
			"	['name', 'loc', 'met', 'prot', 'up', 'dw'],\n" \
			"	{{ 'name' : [ {:s} ],\n" \
			"	'loc' : ['cyt', 'mem', 'per', 'ex']})"

		code = code.format(', '.join([ '\'' + x.replace('-', '_') + '\'' for x in sorted(complexes)]))

		if verbose:
			print(code)
		exec(code.replace('\t', ' ').replace('\n', ' '))

	return metabolites, p_monomers, complexes

def rules_from_metabolic_network(model, data, verbose = False):
	for rxn in data.values:
		# first, determine enzyme composition
		if 'CPLX' in rxn[0]: # the enzyme is a complex alias
			enzyme = 'cplx(name = \'{:s}\', loc = \'cyt\')'.format(rxn[0].replace('-', '_'))

		elif rxn[0].startswith('['): # an enzymatic complex described by its monomers
			monomers = rxn[0][1:-1].split(',')
			enzyme = []

			## create link indexes
			dw = [None] * len(monomers)
			start_link = 1
			for index in range(len(monomers)-1):
				dw[index] = start_link
				start_link += 1
			up = dw[-1:] + dw[:-1]

			for index, monomer in enumerate(monomers):
				if monomer.startswith('MEM-'):
					enzyme.append('prot(name = \'{:s}\', loc = \'mem\', up = {:s}, dw = {:s})'.format(monomer.replace('MEM-', ''), str(up[index]), str(dw[index])))
				else:
					enzyme.append('prot(name = \'{:s}\', loc = \'cyt\', up = {:s}, dw = {:s})'.format(monomer, str(up[index]), str(dw[index])))
			enzyme = ' %\n	'.join(enzyme)

		else: # the enzyme is a monomer
			if rxn[0].startswith('MEM-'):
				enzyme = 'prot(name = \'{:s}\', loc = \'mem\')'.format(rxn[0].replace('MEM-', '').replace('-', '_'))
			else:
				enzyme = 'prot(name = \'{:s}\', loc = \'cyt\')'.format(rxn[0].replace('-', '_'))

		# second, correct reaction names starting with a digit
		name = rxn[1].replace('-', '_')
		if name[0].isdigit():
			name = '_' + name

		# third, correct metabolite names with dashes and create a list
		substrates = rxn[2].replace('-', '_').split(',')
		products = rxn[3].replace('-', '_').split(',')

		# fourth, write LHS and RHS
		LHS = []
		RHS = []

		for subs in substrates:
			if subs[0].isdigit():
				subs = '_' + subs

			if 'PER' in subs:
				LHS.append('met(name = \'{:s}\', loc = \'per\', prot = None)'.format(subs.replace('PER_', '')))
			else:
				LHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = None)'.format(subs))

		for prod in products:
			if prod[0].isdigit():
				prod = '_' + prod

			if 'PER' in prod: # inverse transport reaction
				RHS.append('met(name = \'{:s}\', loc = \'per\', prot = None)'.format(prod.replace('PER_', '')))
			else:
				RHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = None)'.format(prod))

		# fifth, match number of agents at both sides of the Rule
		if len(substrates) < len(products):
			for index in range(len(substrates), len(products)):
				LHS.append('None')
		elif len(products) < len(substrates):
			for index in range(len(products), len(substrates)):
				RHS.append('None')

		# pretty print Rule
		LHS = ' +\n	'.join(LHS)
		RHS = ' +\n	'.join(RHS)

		if rxn[0] == 'spontaneous':
			code = 'Rule(\'{:s}\',\n' \
				'	{:s} |\n'\
				'	{:s},\n' \
				'	Parameter(\'fwd_{:s}\', {:f}), \n' \
				'	Parameter(\'rvs_{:s}\', {:f}))'
			code = code.format(name, LHS, RHS, name, float(rxn[4]), name, float(rxn[5]))

		else: # need an enzyme
			code = 'Rule(\'{:s}\',\n' \
				'	{:s} +\n	{:s} | \n' \
				'	{:s} +\n	{:s}, \n' \
				'	Parameter(\'fwd_{:s}\', {:f}), \n' \
				'	Parameter(\'rvs_{:s}\', {:f}))'
			code = code.format(name, enzyme, LHS, enzyme, RHS, name, float(rxn[4]), name, float(rxn[5])).replace('-', '_')

		if verbose:
			print(code)
		exec(code.replace('\t', ' ').replace('\n', ' '))

def observables_from_metabolic_network(model, data, monomers, verbose = False):
	for name in sorted(monomers[0]):
		name = name.replace('-','_')
		for loc in ['cyt', 'per', 'ex']:
			code = 'Observable(\'obs_met_{:s}_{:s}\', met(name = \'{:s}\', loc = \'{:s}\', prot = None))'
			code = code.format(name, loc, name, loc)
			if verbose:
				print(code)
			exec(code.replace('\t', ' ').replace('\n', ' '))

	for name in sorted(monomers[0]):
		name = name.replace('-','_')
		for loc in ['cyt', 'per', 'ex']:
			code = 'Initial(met(name = \'{:s}\', loc = \'{:s}\', prot = None), Parameter(\'t0_met_{:s}_{:s}\', 0))'
			code = code.format(name, loc, name, loc)
			if verbose:
				print(code)
			exec(code.replace('\t', ' ').replace('\n', ' '))

	for name in sorted(monomers[1]):
		name = name.replace('-','_')
		for loc in ['cyt', 'mem', 'per', 'ex']:
			code = 'Initial(prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), Parameter(\'t0_prot_{:s}_{:s}\', 0))'
			code = code.format(name, loc, name, loc)
			if verbose:
				print(code)
			exec(code.replace('\t', ' ').replace('\n', ' '))

	for name in sorted(monomers[2]):
		name = name.replace('-','_')
		for loc in ['cyt', 'mem', 'per', 'ex']:
			code = 'Initial(cplx(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), Parameter(\'t0_cplx_{:s}_{:s}\', 0))'
			code = code.format(name, loc, name, loc)
			if verbose:
				print(code)
			exec(code.replace('\t', ' ').replace('\n', ' '))

def construct_model_from_metabolic_network(network, verbose = False):
	if isinstance(network, str):
		data = read_network(network)
	elif isinstance(network, pandas.DataFrame)
		data = network
	elif isinstance(network, numpy.array)
		data = pandas.DataFrame(data = network)
	else:
		raise Exception("The network format is not yet supported.")
	data = check_network(data)

	model = Model()
	[metabolites, p_monomers, complexes] = \
		monomers_from_metabolic_network(model, data, verbose)
	observables_from_metabolic_network(model, data, [metabolites, p_monomers, complexes], verbose)
	rules_from_metabolic_network(model, data, verbose = verbose)

	return model
