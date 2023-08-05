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

def monomers_from_genome_graph(model, data, verbose = False):
	# find DNA parts
	architecture = list(data.SOURCE) + [data.TARGET.iloc[-1]]

	names = []
	types = []
	for dna_part in architecture:
		if 'BS' in dna_part:
			names.append('_'.join(
				[dna_part.split('-')[0],
				dna_part.split('-')[2],
				dna_part.split('-')[3]]))
		else:
			names.append(dna_part.split('-')[0])
		types.append(dna_part.split('-')[1])

	# dna
	code = "Monomer('dna',\n" \
		"	['name', 'type', 'prot', 'rna', 'up', 'dw'],\n" \
		"	{{ 'name' : [{:s}],\n" \
		"	'type' : [{:s}]}})"

	code = code.format(
		', '.join([ '\'' + x + '\'' for x in sorted(set(names))]),
		', '.join([ '\'' + x + '\'' for x in sorted(set(types + ['BS']))]))

	if verbose:
		print(code)
	exec(code.replace('\n', ''))

	# rna
	code = "Monomer('rna',\n" \
		"	['name', 'type', 'prot', 'rna'],\n" \
		"	{{ 'name' : [{:s}],\n" \
		"	'type' : [{:s}]}})"

	code = code.format(
		', '.join([ '\'' + x + '\'' for x in sorted(set(names))]),
		', '.join([ '\'' + x + '\'' for x in sorted(set(types + ['BS']))]))

	if verbose:
		print(code)
	exec(code.replace('\n', ''))

	# prot
	code = "Monomer('prot',\n" \
		"	['name', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
		"	{{ 'name' : [{:s}],\n" \
		"	'loc' : ['cyt', 'mem', 'per', 'ex']}})"
	names = [ x for x in names if not x.startswith('BS') ]
	code = code.format(', '.join([ '\'' + x + '\'' for x in sorted(set(names))]))

	if verbose:
		print(code)
	exec(code.replace('\n', ''))

	# complexes
	code = "Monomer('cplx',\n" \
		"	['name', 'loc', 'dna', 'prot', 'rna'],\n" \
		"	{ 'name' : ['RNAP', 'Ribosome'],\n" \
		"	'loc' : ['cyt', 'mem', 'per', 'ex']})"
	if verbose:
		print(code)
	exec(code.replace('\n', ''))

def polymerase_docking_rules(model, data, verbose = False):
	architecture = list(data.SOURCE) + [data.TARGET.iloc[-1]]

	for idx, dna_part in enumerate(architecture):
		if 'pro' in dna_part: # docking rules
			name = dna_part.split('-')[0]
			type = dna_part.split('-')[1]

			code = 'Rule(\'docking_{:s}\',\n' \
				'	cplx(name = \'RNAP\', dna = None) +\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', prot = None) |\n' \
				'	cplx(name = \'RNAP\', dna = 1) %\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', prot = 1),\n' \
				'	Parameter(\'fwd_docking_{:s}\', {:f}),\n' \
				'	Parameter(\'rvs_docking_{:s}\', {:f}))'
			code = code.format(dna_part, name, type, name, type, dna_part, float(data.iloc[idx, 2]), dna_part, float(data.iloc[idx, 3]))

			code = code.replace('-', '_')
			if verbose:
				print(code)
			exec(code)

def polymerase_sliding_rules(model, data, verbose = False):
	for idx, (dna_part1, dna_part2) in enumerate(zip(data.SOURCE, data.TARGET)):
		dna_part1, dna_part2 = (dna_part1, dna_part2)
		name1 = dna_part1.split('-')[0]
		type1 = dna_part1.split('-')[1]
		name2 = dna_part2.split('-')[0]
		type2 = dna_part2.split('-')[1]

		if 'BS' in dna_part1:  # catch binding sites to add to sliding rules
			name1 = '_'.join(
				[dna_part1.split('-')[0],
				dna_part1.split('-')[2],
				dna_part1.split('-')[3]])
			type1 = dna_part1.split('-')[0]
		elif 'BS' in dna_part2:
			name2 = '_'.join(
				[dna_part2.split('-')[0],
				dna_part2.split('-')[2],
				dna_part2.split('-')[3]])
			type2 = dna_part2.split('-')[0]

		code = 'Rule(\'sliding_{:s}\',\n' \
			'	cplx(name = \'RNAP\', dna = 1) %\n' \
			'	dna(name = \'{:s}\', type = \'{:s}\', prot = 1) +\n' \
			'	None +\n' \
			'	dna(name = \'{:s}\', type = \'{:s}\', prot = None) >>\n' \
			'	cplx(name = \'RNAP\', dna = 1) %\n' \
			'	dna(name = \'{:s}\', type = \'{:s}\', prot = 1) +\n' \
			'	rna(name = \'{:s}\', type = \'{:s}\', prot = None, rna = None) +\n' \
			'	dna(name = \'{:s}\', type = \'{:s}\', prot = None),\n' \
			'	Parameter(\'fwd_sliding_{:s}\', {:f}))'
		code = code.format(dna_part1, name1, type1, name2, type2, name2, type2, name2, type2, name1, type1, dna_part1, float(data.iloc[idx, 4]))

		code = code.replace('-', '_')
		if verbose:
			print(code)
		exec(code)

def polymerase_falloff_rules(model, data, verbose = False):
	architecture = list(data.SOURCE) + [data.TARGET.iloc[-1]]

	for idx, dna_part in enumerate(architecture):
		if 'ter' in dna_part: # falloff rules
			name = dna_part.split('-')[0]
			type = dna_part.split('-')[1]

			code = 'Rule(\'falloff_{:s}\',\n' \
				'	cplx(name = \'RNAP\', dna = 1) %\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', prot = 1) >>\n' \
				'	cplx(name = \'RNAP\', dna = None) +\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', prot = None),\n' \
				'	Parameter(\'fwd_falloff_{:s}\', {:f}))'
			code = code.format(dna_part, name, type, name, type, dna_part, float(data.iloc[idx-1, 5]))

			code = code.replace('-', '_')
			if verbose:
				print(code)
			exec(code)

def ribosome_docking_rules(model, data, verbose = False):
	architecture = list(data.SOURCE) + [data.TARGET.iloc[-1]]

	for idx, dna_part in enumerate(architecture):
		if 'rbs' in dna_part: # docking rules
			name = dna_part.split('-')[0]
			type = dna_part.split('-')[1]

			code = 'Rule(\'dr_{:s}\',\n' \
				'	cplx(name = \'Ribosome\', rna = None) +\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', prot = None) |\n' \
				'	cplx(name = \'Ribosome\', rna = 1) %\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', prot = 1),\n' \
				'	Parameter(\'fwd_dr_{:s}\', {:f}),\n' \
				'	Parameter(\'rvs_dr_{:s}\', {:f}))'
			code = code.format(dna_part, name, type, name, type, dna_part, float(data.iloc[idx, 6]), dna_part, float(data.iloc[idx, 7]))

			code = code.replace('-', '_')
			if verbose:
				print(code)
			exec(code)

def ribosome_sliding_rules(model, data, verbose = False):
	for idx, (dna_part1, dna_part2) in enumerate(zip(data.SOURCE, data.TARGET)):
		dna_part1, dna_part2 = (dna_part1, dna_part2)

		if 'BS' in dna_part1:  # catch binding sites to add to sliding rules
			name1 = '_'.join(
				[dna_part1.split('-')[0],
				dna_part1.split('-')[2],
				dna_part1.split('-')[3]])
			type1 = dna_part1.split('-')[0]
		elif 'BS' in dna_part2:
			name2 = '_'.join(
				[dna_part2.split('-')[0],
				dna_part2.split('-')[2],
				dna_part2.split('-')[3]])
			type2 = dna_part2.split('-')[0]
		else:
			name1 = dna_part1.split('-')[0]
			type1 = dna_part1.split('-')[1]
			name2 = dna_part2.split('-')[0]
			type2 = dna_part2.split('-')[1]

		if 'pro' in type1: # slide from the first CDS
			forward = False
		if 'rbs' in type1:
			forward = True

		if forward:
			if 'cds' in type2:
				code = 'Rule(\'sr_{:s}\',\n' \
					'	cplx(name = \'Ribosome\', rna = 1) %\n' \
					'	rna(name = \'{:s}\', type = \'{:s}\', prot = 1) +\n' \
					'	None +\n' \
					'	rna(name = \'{:s}\', type = \'{:s}\', prot = None) >> \n' \
					'	cplx(name = \'Ribosome\', rna = 1) %\n' \
					'	rna(name = \'{:s}\', type = \'{:s}\', prot = 1) +\n' \
					'	prot(name = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None) +\n' \
					'	rna(name = \'{:s}\', type = \'{:s}\', prot = None),\n' \
					'	Parameter(\'fwd_sr_{:s}\', {:f}))'
				code = code.format(dna_part1, name1, type1, name2, type2, name2, type2, name2, name2, type2, dna_part1, float(data.iloc[idx, 8]))

			else: # sliding without protein synthesis
				code = 'Rule(\'sr_{:s}\',\n' \
					'	cplx(name = \'Ribosome\', rna = 1) %\n' \
					'	rna(name = \'{:s}\', type = \'{:s}\', prot = 1) +\n' \
					'	rna(name = \'{:s}\', type = \'{:s}\', prot = None) >>\n' \
					'	cplx(name = \'Ribosome\', rna = 1) %\n' \
					'	rna(name = \'{:s}\', type = \'{:s}\', prot = 1) +\n' \
					'	rna(name = \'{:s}\', type = \'{:s}\', prot = None),\n' \
					'	Parameter(\'fwd_sr_{:s}\', {:f}))'
				code = code.format(dna_part1, name1, type1, name2, type2, name2, type2, name1, type1, dna_part1, float(data.iloc[idx, 8]))

			code = code.replace('-', '_')
			if verbose:
				print(code)
			exec(code)

def ribosome_falloff_rules(model, data, verbose = False):
	architecture = list(data.SOURCE) + [data.TARGET.iloc[-1]]

	for idx, dna_part in enumerate(architecture):
		if 'ter' in dna_part: # falloff rules
			name = dna_part.split('-')[0]
			type = dna_part.split('-')[1]

			code = 'Rule(\'fr_{:s}\',\n' \
				'	cplx(name = \'Ribosome\', rna = 1) %\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', prot = 1) >>\n' \
				'	cplx(name = \'Ribosome\', rna = None) +\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', prot = None),\n' \
				'	Parameter(\'fwd_fr_{:s}\', 0))'
			code = code.format(dna_part, name, type, name, type, dna_part, float(data.iloc[idx-1, 9]))

			code = code.replace('-', '_')
			if verbose:
				print(code)
			exec(code)

def construct_model_from_genome_graph(network, verbose = False):
	data = read_network(network)

	model = Model()
	monomers_from_genome_graph(model, data, verbose)
	polymerase_docking_rules(model, data, verbose)
	polymerase_sliding_rules(model, data, verbose)
	polymerase_falloff_rules(model, data, verbose)
	ribosome_docking_rules(model, data, verbose)
	ribosome_sliding_rules(model, data, verbose)
	ribosome_falloff_rules(model, data, verbose)

	return model
