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

def polymerase_docking_rules(model, data, data_arq, verbose = False):
	description = []
	RULE_LHS = []
	for i in data.index:
		# data
		agents = (data.iloc[i, 0] + ',' + data.iloc[i, 1])
		names = agents.split(',')

		## form the LHS
		LHS = []
		next_in_complex = False
		for name in names:
			if name[0] == '[': # we are dealing with the first monomer of a complex
				molecule = name[1:]
				next_in_complex = True
			elif name[-1] == ']': # we are dealing with the last monomer of a complex
				molecule = name[:-1]
				next_in_complex = False
			elif next_in_complex: # we are dealing with a monomer part of a complex
				molecule = name
			else:
				molecule = name
				linked = 'None'

			if 'BS' in name:
				if 'pro' in name:
					molecule = '{:s}\', type = \'{:s}'.format(molecule.split('-')[-2], molecule.split('-')[-1])
				LHS.append('dna(name = \'{:s}\', prot = dna_link, up = bs_link, dw = bs_link)' \
						.format(molecule))
			elif 'SMALL' in name:
				LHS.append('met(name = \'{:s}\', prot = met_link)' \
						.format(molecule.replace('SMALL-', '')))
			else:
				LHS.append('prot(name = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)' \
						.format(molecule))

		## look for where starts and ends a complex in the LHS
		complexes = [(m.start()+1, m.end()-1) for m in re.finditer(r'\[[A-Za-z0-9-_,]+\]', agents)]
		monomers = [(m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9-_]+', agents)]

		positions = []
		for cplx_pos in reversed(complexes):
			pos_i = None
			pos_f = None
			for index, kmer_pos in enumerate(monomers):
				if cplx_pos[0] == kmer_pos[0]:
					pos_i = index
				if cplx_pos[1] == kmer_pos[1]:
					pos_f = index
					positions.append((pos_i, pos_f))
					break

		## join complexes following start and end positions
		for position in positions:
			## join agents and remove from LHS list because they were joined into one position
			LHS[position[0]] = ' %\n	'.join(LHS[position[0]:position[1]+1])
			for index in reversed(range(position[0]+1, position[1]+1)):
				LHS.pop(index)

		## create numbered links
		starter_link = 1
		for index, agent in enumerate(LHS):
			count_monomers = len(agent.split('%'))
			count_small = agent.count('met(')
			count_prots = agent.count('prot(')
			count_dnas = agent.count('dna(')

			if count_prots > 1:
				dw = [None] * count_prots
				for prot_index in range(count_prots-1):
					dw[prot_index] = starter_link
					starter_link += 1
				up = dw[-1:] + dw[:-1]
				## and replace indexes
				c = list(zip(up, dw))
				c = [elt for sublist in c for elt in sublist]
				LHS[index] = LHS[index].replace('prot_link', '{}').format(*c)

			if count_small >= 1 and count_prots >= 1:
				dw = [None] * (count_small + count_prots)
				for met_index in numpy.arange(0, count_small + count_prots, 2):
					dw[met_index] = starter_link
					dw[met_index-1] = starter_link
					starter_link += 1
				## and replace indexes
				LHS[index] = LHS[index].replace('met_link', '{}').format(*tuple(dw))

			if count_dnas > 1:
				dw = ['WILD'] * count_dnas
	#			 for dna_index in range(count_dnas-1):
	#				 dw[dna_index] = starter_link
	#				 starter_link += 1
				up = dw[-1:] + dw[:-1]
				## and replace indexes
				c = list(zip(up, dw))
				c = [elt for sublist in c for elt in sublist]
				LHS[index] = LHS[index].replace('bs_link', '{}').format(*c)

			if count_dnas >= 1 and count_prots >= 1: # a protein is complexed with the dna
				dw = [None] * (count_prots + count_dnas)
				for dna_index in range(count_prots + count_dnas):
					if dna_index == count_prots:
						dw[dna_index] = starter_link
						dw[dna_index-1] = starter_link
						starter_link += 1
				## and replace indexes
				LHS[index] = LHS[index].replace('True', 'False').replace('dna_link', '{}').format(*dw)

			## final replace
			LHS[index] = LHS[index].replace('prot_link', 'None')
			LHS[index] = LHS[index].replace('met_link', 'None')
			LHS[index] = LHS[index].replace('bs_link', 'WILD')
			LHS[index] = LHS[index].replace('dna_link', 'None')

		## LHS final join
		LHS = ' +\n	'.join(LHS)
		RULE_LHS.append(LHS)

		description.append('# ' + data.iloc[i, 0] + ' interacts with ' + data.iloc[i, 1])

	RULE_RHS = []
	for i in data.index:
		## data
		agents = (data.iloc[i, 0] + ',' + data.iloc[i, 1]).replace('[', '').replace(']', '')
		names = agents.split(',')

		## write the RHS
		RHS = []
		for index, name in enumerate(names):
			if name[0] == '[': # we are dealing with the first monomer of a complex
				molecule = name[1:]
				next_in_complex = True
			elif name[-1] == ']': # we are dealing with the last monomer of a complex
				molecule = name[:-1]
				next_in_complex = False
			elif next_in_complex: # we are dealing with a monomer part of a complex
				molecule = name
			else:
				molecule = name

			if 'BS' in name:
				if 'pro' in name:
					molecule = '{:s}\', type = \'{:s}'.format(molecule.split('-')[-2], molecule.split('-')[-1])
				RHS.append('dna(name = \'{:s}\', prot = dna_link, up = bs_link, dw = bs_link)' \
						.format(molecule))
			elif 'SMALL' in name:
				RHS.append('met(name = \'{:s}\', prot = met_link)' \
						.format(molecule.replace('SMALL-', '')))
			else:
				RHS.append('prot(name = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)' \
						.format(molecule))

		## join complexes
		RHS = ' %\n	'.join(RHS)

		## create numbered links
		agent = RHS
		count_monomers = len(agent.split('%'))
		count_small = agent.count('met(')
		count_prots = agent.count('prot(')
		count_dnas = agent.count('dna(')

		starter_link = 1
		if count_prots > 1:
			dw = [None] * count_prots
			for prot_index in range(count_prots-1):
				dw[prot_index] = starter_link
				starter_link += 1
			up = dw[-1:] + dw[:-1]
			## and replace indexes
			c = list(zip(up, dw))
			c = [elt for sublist in c for elt in sublist]
			RHS = RHS.replace('prot_link', '{}').format(*c)

		if count_small >= 1:
			dw = [None] * (count_small + count_prots)
			for met_index in numpy.arange(0, count_small + count_prots, 2):
				dw[met_index] = starter_link
				dw[met_index-1] = starter_link
				starter_link += 1
			## and replace indexes
			RHS = RHS.replace('met_link', '{}').format(*tuple(dw))

		if count_dnas > 1:
			dw = ['WILD'] * count_dnas
	#		 for dna_index in range(count_dnas-1):
	#			dw[dna_index] = starter_link
	#			starter_link += 1
			up = dw[-1:] + dw[:-1]
			## and replace indexes
			c = list(zip(up, dw))
			c = [elt for sublist in c for elt in sublist]
			RHS = RHS.replace('bs_link', '{}').format(*c)

		## always
		dw = [None] * (count_prots + count_dnas)
		for dna_index in range(count_prots + count_dnas):
			if dna_index == count_prots:
				dw[dna_index] = starter_link
				dw[dna_index-1] = starter_link
				starter_link += 1
		up = dw[-1:] + dw[:-1]
		## and replace indexes
		RHS = RHS.replace('dna_link', '{}').format(*dw)

		## final replace
		RHS = RHS.replace('prot_link', 'None')
		RHS = RHS.replace('met_link', 'None')
		RHS = RHS.replace('bs_link', 'WILD')
		RHS = RHS.replace('dna_link', 'None')

		RULE_RHS.append(RHS)

	index = 0
	for i in data.index:
		for dna_part1, dna_part2 in zip(data_arq.iloc[:,0], data_arq.iloc[:,1]):
			if data.iloc[i, 1][3:] == dna_part1:
				## complete rule
				code = 'Rule(\'docking_{:d}_{:s}\',\n' \
					'	{:s} |\n' \
					'	{:s},\n' \
					'	Parameter(\'fwd_docking_{:d}_{:s}\', {:f}),\n' \
					'	Parameter(\'rvs_docking_{:d}_{:s}\', {:f}))'

				code = code.format(
					index+1, dna_part1, RULE_LHS[index], RULE_RHS[index], index+1, dna_part1,
					data.iloc[i, 2], index+1, dna_part1, data.iloc[i, 3])

				code = code.replace('-', '_')
				if verbose:
					print(code)
				exec(code)

				index += 1

def polymerase_sliding_from_promoters_rules(model, data, data_arq, verbose):
	description = []
	RULE_LHS = []

	for i in data.index:
		for dna_part1, dna_part2 in zip(data_arq.iloc[:,0], data_arq.iloc[:,1]):
			if data.iloc[i, 1][3:] == dna_part1:
				# data
				agents = (data.iloc[i, 0][:-1] + ',' + data.iloc[i, 1]) + ']' + ',BS-' + dna_part2
				names = agents.split(',')

				## form the LHS
				LHS = []
				next_in_complex = False
				for name in names:
					if name[0] == '[': # we are dealing with the first monomer of a complex
						molecule = name[1:]
						next_in_complex = True
					elif name[-1] == ']': # we are dealing with the last monomer of a complex
						molecule = name[:-1]
						next_in_complex = False
					elif next_in_complex: # we are dealing with a monomer part of a complex
						molecule = name
					else:
						molecule = name

					if 'BS' in name:
						if 'pro' in name or 'rbs' in name:
							molecule = '{:s}\', type = \'{:s}'.format(molecule.split('-')[-2], molecule.split('-')[-1])
						LHS.append('dna(name = \'{:s}\', prot = dna_link, up = bs_link, dw = bs_link)' \
								   .format(molecule))
					elif 'SMALL' in name:
						LHS.append('met(name = \'{:s}\', prot = met_link)' \
								   .format(molecule.replace('SMALL-', '')))
					else:
						LHS.append('prot(name = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)' \
								   .format(molecule))

				## look for where starts and ends a complex in the LHS
				complexes = [(m.start()+1, m.end()-1) for m in re.finditer(r'\[[A-Za-z0-9-_, ]+\]', agents)]
				monomers = [(m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9-_]+', agents)]

				positions = []
				for cplx_pos in reversed(complexes):
					pos_i = None
					pos_f = None
					for index, kmer_pos in enumerate(monomers):
						if cplx_pos[0] == kmer_pos[0]:
							pos_i = index
						if cplx_pos[1] == kmer_pos[1]:
							pos_f = index
							positions.append((pos_i, pos_f))
							break

				## join complexes following start and end positions
				for position in positions:
					## join agents and remove from LHS list because they were joined into one position
					LHS[position[0]] = ' %\n	'.join(LHS[position[0]:position[1]+1])
					for index in reversed(range(position[0]+1, position[1]+1)):
						LHS.pop(index)

				## create numbered links
				starter_link = 1
				for index, agent in enumerate(LHS):
					count_monomers = len(agent.split('%'))
					count_small = agent.count('met(')
					count_prots = agent.count('prot(')
					count_dnas = agent.count('dna(')

					if count_prots > 1:
						dw = [None] * count_prots
						for prot_index in range(count_prots-1):
							dw[prot_index] = starter_link
							starter_link += 1
						up = dw[-1:] + dw[:-1]
						## and replace indexes
						c = list(zip(up, dw))
						c = [elt for sublist in c for elt in sublist]
						LHS[index] = LHS[index].replace('prot_link', '{}').format(*c)

					if count_small >= 1 and count_prots >= 1:
						dw = [None] * (count_small + count_prots)
						for met_index in numpy.arange(0, count_small + count_prots, 2):
							dw[met_index] = starter_link
							dw[met_index-1] = starter_link
							starter_link += 1
						## and replace indexes
						LHS[index] = LHS[index].replace('met_link', '{}').format(*tuple(dw))

					if count_dnas > 1:
						dw = ['WILD'] * count_dnas
			#			 for dna_index in range(count_dnas-1):
			#				 dw[dna_index] = starter_link
			#				 starter_link += 1
						up = dw[-1:] + dw[:-1]
						## and replace indexes
						c = list(zip(up, dw))
						c = [elt for sublist in c for elt in sublist]
						LHS[index] = LHS[index].replace('bs_link', '{}').format(*c)

					if count_dnas >= 1 and count_prots >= 1: # a protein is complexed with the dna
						dw = [None] * (count_prots + count_dnas)
						for dna_index in range(count_prots + count_dnas):
							if dna_index == count_prots:
								dw[dna_index] = starter_link
								dw[dna_index-1] = starter_link
								starter_link += 1
						## and replace indexes
						LHS[index] = LHS[index].replace('True', 'False').replace('dna_link', '{}').format(*dw)

					## final replace
					LHS[index] = LHS[index].replace('prot_link', 'None')
					LHS[index] = LHS[index].replace('met_link', 'None')
					LHS[index] = LHS[index].replace('bs_link', 'WILD')
					LHS[index] = LHS[index].replace('dna_link', 'None')

				## LHS final join
				LHS = ' +\n	'.join(LHS) + ' + None'
				RULE_LHS.append(LHS)

				description.append('# ' + data.iloc[i, 0] + ' slides to ' + dna_part2)

	RULE_RHS = []
	for i in data.index:
		for dna_part1, dna_part2 in zip(data_arq.iloc[:,0], data_arq.iloc[:,1]):
			if data.iloc[i, 1][3:] == dna_part1:
				# data
				agents = (','.join(data.iloc[i, 0].split(',')[:-1]) + ',BS-' + dna_part2) + '],' + data.iloc[i, 0].split(',')[-1][:-1] + ',BS-' + dna_part1
				names = agents.split(',')

				## form the RHS
				RHS = []
				next_in_complex = False
				for name in names:
					if name[0] == '[': # we are dealing with the first monomer of a complex
						molecule = name[1:]
						next_in_complex = True
					elif name[-1] == ']': # we are dealing with the last monomer of a complex
						molecule = name[:-1]
						next_in_complex = False
					elif next_in_complex: # we are dealing with a monomer part of a complex
						molecule = name
					else:
						molecule = name

					if 'BS' in name:
						if 'pro' in name or 'rbs' in name or 'cds' in name:
							molecule = '{:s}\', type = \'{:s}'.format(molecule.split('-')[-2], molecule.split('-')[-1])
						RHS.append('dna(name = \'{:s}\', prot = dna_link, up = bs_link, dw = bs_link)' \
								.format(molecule))
					elif 'SMALL' in name:
						RHS.append('met(name = \'{:s}\', prot = met_link)' \
								.format(molecule.replace('SMALL-', '')))
					else:
						RHS.append('prot(name = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)' \
								.format(molecule))

				molecule = '{:s}\', type = \'{:s}'.format(dna_part2.split('-')[0], dna_part2.split('-')[1])
				RHS.append('rna(name = \'{:s}\', prot = None)'.format(molecule))

				## look for where starts and ends a complex in the RHS
				complexes = [(m.start()+1, m.end()-1) for m in re.finditer(r'\[[A-Za-z0-9-_, ]+\]', agents)]
				monomers = [(m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9-_]+', agents)]

				positions = []
				for cplx_pos in reversed(complexes):
					pos_i = None
					pos_f = None
					for index, kmer_pos in enumerate(monomers):
						if cplx_pos[0] == kmer_pos[0]:
							pos_i = index
						if cplx_pos[1] == kmer_pos[1]:
							pos_f = index
							positions.append((pos_i, pos_f))
							break

				## join complexes following start and end positions
				for position in positions:
					## join agents and remove from RHS list because they were joined into one position
					RHS[position[0]] = ' %\n	'.join(RHS[position[0]:position[1]+1])
					for index in reversed(range(position[0]+1, position[1]+1)):
						RHS.pop(index)

				## create numbered links
				starter_link = 1
				for index, agent in enumerate(RHS):
					count_monomers = len(agent.split('%'))
					count_small = agent.count('met(')
					count_prots = agent.count('prot(')
					count_dnas = agent.count('dna(')

					if count_prots > 1:
						dw = [None] * count_prots
						for prot_index in range(count_prots-1):
							dw[prot_index] = starter_link
							starter_link += 1
						up = dw[-1:] + dw[:-1]
						## and replace indexes
						c = list(zip(up, dw))
						c = [elt for sublist in c for elt in sublist]
						RHS[index] = RHS[index].replace('prot_link', '{}').format(*c)

					if count_small >= 1 and count_prots >= 1:
						dw = [None] * (count_small + count_prots)
						for met_index in numpy.arange(0, count_small + count_prots, 2):
							dw[met_index] = starter_link
							dw[met_index-1] = starter_link
							starter_link += 1
						## and replace indexes
						RHS[index] = RHS[index].replace('met_link', '{}').format(*tuple(dw))

					if count_dnas > 1:
						dw = ['WILD'] * count_dnas
			#			 for dna_index in range(count_dnas-1):
			#				 dw[dna_index] = starter_link
			#				 starter_link += 1
						up = dw[-1:] + dw[:-1]
						## and replace indexes
						c = list(zip(up, dw))
						c = [elt for sublist in c for elt in sublist]
						RHS[index] = RHS[index].replace('bs_link', '{}').format(*c)

					if count_dnas >= 1 and count_prots >= 1: # a protein is complexed with the dna
						dw = [None] * (count_prots + count_dnas)
						for dna_index in range(count_prots + count_dnas):
							if dna_index == count_prots:
								dw[dna_index] = starter_link
								dw[dna_index-1] = starter_link
								starter_link += 1
						## and replace indexes
						RHS[index] = RHS[index].replace('True', 'False').replace('dna_link', '{}').format(*dw)

					## final replace
					RHS[index] = RHS[index].replace('prot_link', 'None')
					RHS[index] = RHS[index].replace('met_link', 'None')
					RHS[index] = RHS[index].replace('bs_link', 'WILD')
					RHS[index] = RHS[index].replace('dna_link', 'None')

				## RHS final join
				RHS = ' +\n	'.join(RHS)
				RHS = RHS.split('	')
				RHS[4], RHS[5] = RHS[5], RHS[4]
				RHS[4] = RHS[4][:-2] + '%\n'
				RHS = '	'.join(RHS)
				RULE_RHS.append(RHS)

				msg = '# ' + data.iloc[i, 0] + ' slides to ' + data.iloc[i, 1]
				description.append(msg)

	index = 0
	for i in data.index:
		for dna_part1, dna_part2 in zip(data_arq.iloc[:,0], data_arq.iloc[:,1]):
			if data.iloc[i, 1][3:] == dna_part1:
				## complete rule
				code = 'Rule(\'sliding_{:d}_{:s}\',\n' \
					'	{:s} >>\n' \
					'	{:s},\n' \
					'	Parameter(\'fwd_sliding_{:d}_{:s}\', {:f}))' \

				code = code.format(index+1, dna_part1 + '_' + dna_part2.split('-')[-1],
							RULE_LHS[index], RULE_RHS[index], index+1, dna_part1 + '_' + dna_part2.split('-')[-1], data.iloc[i, 4])

				code = code.replace('-', '_')
				if verbose:
					print(code)
				exec(code)

		index += 1

def polymerase_sliding_from_others_rules(model, data, data_arq, verbose):
	description = []
	RULE_LHS = []

	for dna_part1, dna_part2 in zip(data_arq.iloc[:,0], data_arq.iloc[:,1]):
		for i in data.index:
			if 'pro' not in dna_part1:
				# data
				agents = (','.join(data.iloc[i, 0].split(',')[0:4]) + ',BS-' + dna_part1).replace(']', '') + ']' + ',BS-' + dna_part2
				names = agents.split(',')

				## form the LHS
				LHS = []
				next_in_complex = False
				for name in names:
					if name[0] == '[': # we are dealing with the first monomer of a complex
						molecule = name[1:]
						next_in_complex = True
					elif name[-1] == ']': # we are dealing with the last monomer of a complex
						molecule = name[:-1]
						next_in_complex = False
					elif next_in_complex: # we are dealing with a monomer part of a complex
						molecule = name
					else:
						molecule = name

					if 'BS' in name:
						molecule = '{:s}\', type = \'{:s}'.format(molecule.split('-')[-2], molecule.split('-')[-1])
						LHS.append('dna(name = \'{:s}\', prot = dna_link, up = bs_link, dw = bs_link)' \
								.format(molecule))
					elif 'SMALL' in name:
						LHS.append('met(name = \'{:s}\', prot = met_link)' \
								.format(molecule.replace('SMALL-', '')))
					else:
						LHS.append('prot(name = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)' \
								.format(molecule))

				if 'ter' not in dna_part2:
					LHS.append('None')

				## look for where starts and ends a complex in the LHS
				complexes = [(m.start()+1, m.end()-1) for m in re.finditer(r'\[[A-Za-z0-9-_, ]+\]', agents)]
				monomers = [(m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9-_]+', agents)]

				positions = []
				for cplx_pos in reversed(complexes):
					pos_i = None
					pos_f = None
					for index, kmer_pos in enumerate(monomers):
						if cplx_pos[0] == kmer_pos[0]:
							pos_i = index
						if cplx_pos[1] == kmer_pos[1]:
							pos_f = index
							positions.append((pos_i, pos_f))
							break

				## join complexes following start and end positions
				for position in positions:
					## join agents and remove from LHS list because they were joined into one position
					LHS[position[0]] = ' %\n    '.join(LHS[position[0]:position[1]+1])
					for index in reversed(range(position[0]+1, position[1]+1)):
						LHS.pop(index)

				## create numbered links
				starter_link = 1
				for index, agent in enumerate(LHS):
					count_monomers = len(agent.split('%'))
					count_small = agent.count('met(')
					count_prots = agent.count('prot(')
					count_dnas = agent.count('dna(')

					if count_prots > 1:
						dw = [None] * count_prots
						for prot_index in range(count_prots-1):
							dw[prot_index] = starter_link
							starter_link += 1
						up = dw[-1:] + dw[:-1]
						## and replace indexes
						c = list(zip(up, dw))
						c = [elt for sublist in c for elt in sublist]
						LHS[index] = LHS[index].replace('prot_link', '{}').format(*c)

					if count_small >= 1 and count_prots >= 1:
						dw = [None] * (count_small + count_prots)
						for met_index in numpy.arange(0, count_small + count_prots, 2):
							dw[met_index] = starter_link
							dw[met_index-1] = starter_link
							starter_link += 1
						## and replace indexes
						LHS[index] = LHS[index].replace('met_link', '{}').format(*tuple(dw))

					if count_dnas > 1:
						dw = ['WILD'] * count_dnas
			#             for dna_index in range(count_dnas-1):
			#                 dw[dna_index] = starter_link
			#                 starter_link += 1
						up = dw[-1:] + dw[:-1]
						## and replace indexes
						c = list(zip(up, dw))
						c = [elt for sublist in c for elt in sublist]
						LHS[index] = LHS[index].replace('bs_link', '{}').format(*c)

					if count_dnas >= 1 and count_prots >= 1: # a protein is complexed with the dna
						dw = [None] * (count_prots + count_dnas)
						for dna_index in range(count_prots + count_dnas):
							if dna_index == count_prots:
								dw[dna_index] = starter_link
								dw[dna_index-1] = starter_link
								starter_link += 1
						## and replace indexes
						LHS[index] = LHS[index].replace('True', 'False').replace('dna_link', '{}').format(*dw)

					## final replace
					LHS[index] = LHS[index].replace('prot_link', 'None')
					LHS[index] = LHS[index].replace('met_link', 'None')
					LHS[index] = LHS[index].replace('bs_link', 'WILD')
					LHS[index] = LHS[index].replace('dna_link', 'None')

				## LHS final join
				LHS = ' +\n    '.join(LHS)
				RULE_LHS.append(LHS)

				description.append('# ' + ', '.join(data.iloc[i, 0].split(', ')[0:4]) + '] slides to ' + dna_part2)

			break # do not remove

	description = []
	RULE_RHS = []

	for dna_part1, dna_part2 in zip(data_arq.iloc[:,0], data_arq.iloc[:,1]):
		for i in data.index:
			if 'pro' not in dna_part1:
				# data
				agents = (','.join(data.iloc[i, 0].split(',')[0:4]) + ',BS-' + dna_part2).replace(']', '') + ']' + ',BS-' + dna_part1
				names = agents.split(',')

				## form the RHS
				RHS = []
				next_in_complex = False
				for name in names:
					if name[0] == '[': # we are dealing with the first monomer of a complex
						molecule = name[1:]
						next_in_complex = True
					elif name[-1] == ']': # we are dealing with the last monomer of a complex
						molecule = name[:-1]
						next_in_complex = False
					elif next_in_complex: # we are dealing with a monomer part of a complex
						molecule = name
					else:
						molecule = name

					if 'BS' in name:
						molecule = '{:s}\', type = \'{:s}'.format(molecule.split('-')[-2], molecule.split('-')[-1])
						RHS.append('dna(name = \'{:s}\', prot = dna_link, up = bs_link, dw = bs_link)' \
								.format(molecule))
					elif 'SMALL' in name:
						RHS.append('met(name = \'{:s}\', prot = met_link)' \
								.format(molecule.replace('SMALL-', '')))
					else:
						RHS.append('prot(name = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)' \
								.format(molecule))

				if 'ter' not in dna_part2:
					molecule = '{:s}\', type = \'{:s}'.format(dna_part2.split('-')[0], dna_part2.split('-')[1])
					RHS.append('rna(name = \'{:s}\', prot = None)'.format(molecule))

				## look for where starts and ends a complex in the RHS
				complexes = [(m.start()+1, m.end()-1) for m in re.finditer(r'\[[A-Za-z0-9-_, ]+\]', agents)]
				monomers = [(m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9-_]+', agents)]

				positions = []
				for cplx_pos in reversed(complexes):
					pos_i = None
					pos_f = None
					for index, kmer_pos in enumerate(monomers):
						if cplx_pos[0] == kmer_pos[0]:
							pos_i = index
						if cplx_pos[1] == kmer_pos[1]:
							pos_f = index
							positions.append((pos_i, pos_f))
							break

				## join complexes following start and end positions
				for position in positions:
					## join agents and remove from RHS list because they were joined into one position
					RHS[position[0]] = ' %\n    '.join(RHS[position[0]:position[1]+1])
					for index in reversed(range(position[0]+1, position[1]+1)):
						RHS.pop(index)

				## create numbered links
				starter_link = 1
				for index, agent in enumerate(RHS):
					count_monomers = len(agent.split('%'))
					count_small = agent.count('met(')
					count_prots = agent.count('prot(')
					count_dnas = agent.count('dna(')

					if count_prots > 1:
						dw = [None] * count_prots
						for prot_index in range(count_prots-1):
							dw[prot_index] = starter_link
							starter_link += 1
						up = dw[-1:] + dw[:-1]
						## and replace indexes
						c = list(zip(up, dw))
						c = [elt for sublist in c for elt in sublist]
						RHS[index] = RHS[index].replace('prot_link', '{}').format(*c)

					if count_small >= 1 and count_prots >= 1:
						dw = [None] * (count_small + count_prots)
						for met_index in numpy.arange(0, count_small + count_prots, 2):
							dw[met_index] = starter_link
							dw[met_index-1] = starter_link
							starter_link += 1
						## and replace indexes
						RHS[index] = RHS[index].replace('met_link', '{}').format(*tuple(dw))

					if count_dnas > 1:
						dw = ['WILD'] * count_dnas
			#             for dna_index in range(count_dnas-1):
			#                 dw[dna_index] = starter_link
			#                 starter_link += 1
						up = dw[-1:] + dw[:-1]
						## and replace indexes
						c = list(zip(up, dw))
						c = [elt for sublist in c for elt in sublist]
						RHS[index] = RHS[index].replace('bs_link', '{}').format(*c)

					if count_dnas >= 1 and count_prots >= 1: # a protein is complexed with the dna
						dw = [None] * (count_prots + count_dnas)
						for dna_index in range(count_prots + count_dnas):
							if dna_index == count_prots:
								dw[dna_index] = starter_link
								dw[dna_index-1] = starter_link
								starter_link += 1
						## and replace indexes
						RHS[index] = RHS[index].replace('True', 'False').replace('dna_link', '{}').format(*dw)

					## final replace
					RHS[index] = RHS[index].replace('prot_link', 'None')
					RHS[index] = RHS[index].replace('met_link', 'None')
					RHS[index] = RHS[index].replace('bs_link', 'WILD')
					RHS[index] = RHS[index].replace('dna_link', 'None')

				## RHS final join
				RHS = ' +\n\t'.join(RHS)
				RULE_RHS.append(RHS)

				description.append('# ' + ', '.join(data.iloc[i, 0].split(', ')[0:4]) + '] slides to ' + dna_part2)

			break # do not remove

	index = 0
	for idx, (dna_part1, dna_part2) in enumerate(zip(data_arq.iloc[:,0], data_arq.iloc[:,1])):
		dna_part1, dna_part2 = (dna_part1, dna_part2)
		if 'pro' not in dna_part1:
			## complete rule
			code = 'Rule(\'sliding_{:s}\',\n' \
				'	{:s} >>\n' \
				'	{:s},\n' \
				'	Parameter(\'fwd_sliding_{:s}\', {:f}))'

			code = code.format(dna_part2, RULE_LHS[index], RULE_RHS[index], dna_part2, data_arq.iloc[idx, 4])

			code = code.replace('-', '_')
			if verbose:
				print(code)
			exec(code)
			index += 1

def polymerase_falloff_rules(model, data, data_arq, verbose):
	description = []
	RULE_LHS = []

	for dna_part1, dna_part2 in zip(data_arq.iloc[:,0], data_arq.iloc[:,1]):
		if 'ter' in dna_part2:
			# data
			agents = (','.join(data.iloc[i, 0].split(',')[0:4])).replace(']', '') + ',BS-' + dna_part2 + ']'
			names = agents.split(',')

			## form the LHS
			LHS = []
			next_in_complex = False
			for name in names:
				if name[0] == '[': # we are dealing with the first monomer of a complex
					molecule = name[1:]
					next_in_complex = True
				elif name[-1] == ']': # we are dealing with the last monomer of a complex
					molecule = name[:-1]
					next_in_complex = False
				elif next_in_complex: # we are dealing with a monomer part of a complex
					molecule = name
				else:
					molecule = name

				if 'BS' in name:
					if 'ter' in name:
						molecule = '{:s}\', type = \'{:s}'.format(molecule.split('-')[-2], molecule.split('-')[-1])
					LHS.append('dna(name = \'{:s}\', prot = dna_link, free = \'True\', up = bs_link, dw = bs_link)' \
							.format(molecule))
				elif 'SMALL' in name:
					LHS.append('met(name = \'{:s}\', prot = met_link)' \
							.format(molecule.replace('SMALL-', '')))
				else:
					LHS.append('prot(name = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)' \
							.format(molecule))

			## look for where starts and ends a complex in the LHS
			complexes = [(m.start()+1, m.end()-1) for m in re.finditer(r'\[[A-Za-z0-9-_, ]+\]', agents)]
			monomers = [(m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9-_]+', agents)]

			positions = []
			for cplx_pos in reversed(complexes):
				pos_i = None
				pos_f = None
				for index, kmer_pos in enumerate(monomers):
					if cplx_pos[0] == kmer_pos[0]:
						pos_i = index
					if cplx_pos[1] == kmer_pos[1]:
						pos_f = index
						positions.append((pos_i, pos_f))
						break

			## join complexes following start and end positions
			for position in positions:
				## join agents and remove from LHS list because they were joined into one position
				LHS[position[0]] = ' %\n    '.join(LHS[position[0]:position[1]+1])
				for index in reversed(range(position[0]+1, position[1]+1)):
					LHS.pop(index)

			## create numbered links
			starter_link = 1
			for index, agent in enumerate(LHS):
				count_monomers = len(agent.split('%'))
				count_small = agent.count('met(')
				count_prots = agent.count('prot(')
				count_dnas = agent.count('dna(')

				if count_prots > 1:
					dw = [None] * count_prots
					for prot_index in range(count_prots-1):
						dw[prot_index] = starter_link
						starter_link += 1
					up = dw[-1:] + dw[:-1]
					## and replace indexes
					c = list(zip(up, dw))
					c = [elt for sublist in c for elt in sublist]
					LHS[index] = LHS[index].replace('prot_link', '{}').format(*c)

				if count_small >= 1 and count_prots >= 1:
					dw = [None] * (count_small + count_prots)
					for met_index in numpy.arange(0, count_small + count_prots, 2):
						dw[met_index] = starter_link
						dw[met_index-1] = starter_link
						starter_link += 1
					## and replace indexes
					LHS[index] = LHS[index].replace('met_link', '{}').format(*tuple(dw))

				if count_dnas > 1:
					dw = ['WILD'] * count_dnas
		#             for dna in range(count_dnas-1):
		#                 dw[dna] = starter_link
		#                 starter_link += 1
					up = dw[-1:] + dw[:-1]
					## and replace indexes
					c = list(zip(up, dw))
					c = [elt for sublist in c for elt in sublist]
					LHS[index] = LHS[index].replace('bs_link', '{}').format(*c)

				if count_dnas >= 1 and count_prots >= 1: # a protein is complexed with the dna
					dw = [None] * (count_prots + count_dnas)
					for dna_index in range(count_prots + count_dnas):
						if dna_index == count_prots:
							dw[dna_index] = starter_link
							dw[dna_index-1] = starter_link
							starter_link += 1
					## and replace indexes
					LHS[index] = LHS[index].replace('True', 'False').replace('dna_link', '{}').format(*dw)

				## final replace
				LHS[index] = LHS[index].replace('prot_link', 'None')
				LHS[index] = LHS[index].replace('met_link', 'None')
				LHS[index] = LHS[index].replace('bs_link', 'WILD')
				LHS[index] = LHS[index].replace('dna_link', 'None')

			## LHS final join
			LHS = ' +\n    '.join(LHS)
			RULE_LHS.append(LHS)

			description.append('# ' + data.iloc[i, 0] + ' falloff from ' + dna_part2)

	description = []
	RULE_RHS = []

	for dna_part1, dna_part2 in zip(data_arq.iloc[:,0], data_arq.iloc[:,1]):
		if 'ter' in dna_part2:
			# data
			agents = ','.join(data.iloc[i, 0].split(',')[0:4]) + '],BS-' + dna_part2
			names = agents.split(',')

			## form the RHS
			RHS = []
			next_in_complex = False
			for name in names:
				if name[0] == '[': # we are dealing with the first monomer of a complex
					molecule = name[1:]
					next_in_complex = True
				elif name[-1] == ']': # we are dealing with the last monomer of a complex
					molecule = name[:-1]
					next_in_complex = False
				elif next_in_complex: # we are dealing with a monomer part of a complex
					molecule = name
				else:
					molecule = name

				if 'BS' in name:
					if 'ter' in name:
						molecule = '{:s}\', type = \'{:s}'.format(molecule.split('-')[-2], molecule.split('-')[-1])
					RHS.append('dna(name = \'{:s}\', prot = dna_link, free = \'True\', up = bs_link, dw = bs_link)' \
							.format(molecule))
				elif 'SMALL' in name:
					RHS.append('met(name = \'{:s}\', prot = met_link)' \
							.format(molecule.replace('SMALL-', '')))
				else:
					RHS.append('prot(name = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)' \
							.format(molecule))

			## look for where starts and ends a complex in the RHS
			complexes = [(m.start()+1, m.end()-1) for m in re.finditer(r'\[[A-Za-z0-9-_, ]+\]', agents)]
			monomers = [(m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9-_]+', agents)]

			positions = []
			for cplx_pos in reversed(complexes):
				pos_i = None
				pos_f = None
				for index, kmer_pos in enumerate(monomers):
					if cplx_pos[0] == kmer_pos[0]:
						pos_i = index
					if cplx_pos[1] == kmer_pos[1]:
						pos_f = index
						positions.append((pos_i, pos_f))
						break

			## join complexes following start and end positions
			for position in positions:
				## join agents and remove from RHS list because they were joined into one position
				RHS[position[0]] = ' %\n    '.join(RHS[position[0]:position[1]+1])
				for index in reversed(range(position[0]+1, position[1]+1)):
					RHS.pop(index)

			## create numbered links
			starter_link = 1
			for index, agent in enumerate(RHS):
				count_monomers = len(agent.split('%'))
				count_small = agent.count('met(')
				count_prots = agent.count('prot(')
				count_dnas = agent.count('dna(')

				if count_prots > 1:
					dw = [None] * count_prots
					for prot_index in range(count_prots-1):
						dw[prot_index] = starter_link
						starter_link += 1
					up = dw[-1:] + dw[:-1]
					## and replace indexes
					c = list(zip(up, dw))
					c = [elt for sublist in c for elt in sublist]
					RHS[index] = RHS[index].replace('prot_link', '{}').format(*c)

				if count_small >= 1 and count_prots >= 1:
					dw = [None] * (count_small + count_prots)
					for met_index in numpy.arange(0, count_small + count_prots, 2):
						dw[met_index] = starter_link
						dw[met_index-1] = starter_link
						starter_link += 1
					## and replace indexes
					RHS[index] = RHS[index].replace('met_link', '{}').format(*tuple(dw))

				if count_dnas > 1:
					dw = ['WILD'] * count_dnas
		#             for dna in range(count_dnas-1):
		#                 dw[dna] = starter_link
		#                 starter_link += 1
					up = dw[-1:] + dw[:-1]
					## and replace indexes
					c = list(zip(up, dw))
					c = [elt for sublist in c for elt in sublist]
					RHS[index] = RHS[index].replace('bs_link', '{}').format(*c)

				if count_dnas >= 1 and count_prots >= 1: # a protein is complexed with the dna
					dw = [None] * (count_prots + count_dnas)
					for dna_index in range(count_prots + count_dnas):
						if dna_index == count_prots:
							dw[dna_index] = starter_link
							dw[dna_index-1] = starter_link
							starter_link += 1
					## and replace indexes
					RHS[index] = RHS[index].replace('True', 'False').replace('dna_link', '{}').format(*dw)

				## final replace
				RHS[index] = RHS[index].replace('prot_link', 'None')
				RHS[index] = RHS[index].replace('met_link', 'None')
				RHS[index] = RHS[index].replace('bs_link', 'WILD')
				RHS[index] = RHS[index].replace('dna_link', 'None')

			## RHS final join
			RHS = ' +\n    '.join(RHS)
			RULE_RHS.append(RHS)

			description.append('# ' + data.iloc[i, 0] + ' falloff from ' + dna_part2)

	index = 0
	for idx, (dna_part1, dna_part2) in enumerate(zip(data_arq.iloc[:,0], data_arq.iloc[:,1])):
		dna_part1, dna_part2 = (dna_part1, dna_part2)
		if 'ter' in dna_part2:
			## complete rule
			code = 'Rule(\'falloff_{:s}\', \n' \
				'	{:s} >> \n' \
				'	{:s}, \n' \
				'	Parameter(\'fwd_falloff_{:s}\', {:f}))'

			code = code.format(dna_part2, RULE_LHS[index], RULE_RHS[index], dna_part2, data_arq.iloc[idx, 5])
			code = code.replace('-', '_')
			if verbose:
				print(code)
			exec(code)
			index += 1

def construct_model_from_sigma_specificity_network(promoters = '', architecture = '', verbose = False):
	data_promoters = read_network(promoters)
	data_architecture = read_network(architecture)

	model = Model()
	monomers_from_genome_graph(model, data_architecture, verbose)
	polymerase_docking_rules(model, data_promoters, data_architecture, verbose)
	polymerase_sliding_from_promoters_rules(model, data_promoters, data_architecture, verbose)
	polymerase_sliding_from_others_rules(model, data_promoters, data_architecture, verbose)

	return model
