# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

from .construct_model_from_metabolic_network import *
from .construct_model_from_interaction_network import *
from .construct_model_from_genome_graph import *
from .construct_model_from_sigma_specificity_network import *

from pysb import *
from pysb.core import *
from pysb.util import alias_model_components

def combine_models(model, new_model, verbose = False):
	# find monomers in common and uniques
	monomer_names1 = []
	monomer_names2 = []
	for monomer in model.monomers:
		monomer_names1.append(monomer.name)
	for monomer in new_model.monomers:
		monomer_names2.append(monomer.name)

	commons = list(set(monomer_names1).intersection(monomer_names2))
	uniques = list(set(monomer_names1).symmetric_difference(monomer_names2))

	if verbose:
		print('common Monomers are: ' + ', '.join(commons))
		print('unique Monomers are: ' + ', '.join(uniques))

	new_monomers = []
	for unique in uniques:
		for monomer in model.monomers:
			if unique == monomer.name:
				new_monomers.append(str(monomer))
		for monomer in new_model.monomers:
			if unique == monomer.name:
				new_monomers.append(str(monomer))

	for common in commons:
		for monomer in model.monomers:
			if common == monomer.name:
				sites_in_model = monomer.sites
				names_in_model = monomer.site_states['name']
				if (common == 'dna' or common == 'rna'):
					types_in_model = monomer.site_states['type']
				else:
					loc_in_model = monomer.site_states['loc']
		for monomer in new_model.monomers:
			if common == monomer.name:
				sites_in_new_model = monomer.sites
				names_in_new_model = monomer.site_states['name']
				if (common == 'dna' or common == 'rna'):
					types_in_new_model = monomer.site_states['type']
				else:
					loc_in_new_model = monomer.site_states['loc']

		if (common == 'dna' or common == 'rna'):
			new_monomers.append(
				"Monomer('{:s}', {:s}, {{'name': {:s}, 'type': {:s}}})".format(
					str(common),
					str(sorted(set(sites_in_model + sites_in_new_model))),
					str(sorted(set(names_in_model + names_in_new_model))),
					str(sorted(set(types_in_model + types_in_new_model)))))
		else:
			new_monomers.append(
				"Monomer('{:s}', {:s}, {{'name': {:s}, 'loc': {:s}}})".format(
					str(common),
					str(sorted(set(sites_in_model + sites_in_new_model))),
					str(sorted(set(names_in_model + names_in_new_model))),
					str(sorted(set(loc_in_model + loc_in_new_model)))))

	new_rules = []
	for rule in model.rules:
		new_rules.append(str(rule))
	for rule in new_model.rules:
		new_rules.append(str(rule))

	new_parameters = []
	for parameter in model.parameters:
		new_parameters.append(str(parameter))
	for parameter in new_model.parameters:
		new_parameters.append(str(parameter))

	new_initials = []
	for initial in model.initials:
		new_initials.append(str(initial))
	for initial in new_model.initials:
		new_initials.append(str(initial))

	new_observables = []
	for observable in model.observables:
		new_observables.append(str(observable))
	for observable in new_model.observables:
		new_observables.append(str(observable))

	new_model.monomers = ComponentSet()
	new_model.parameters = ComponentSet()
	new_model.initials = []
	new_model.rules = ComponentSet()
	new_model.observables = ComponentSet()

	for new_monomer in new_monomers:
		if verbose:
			print(new_monomer)
		exec(new_monomer)

	for new_parameter in sorted(set(new_parameters)):
		if verbose:
			print(new_parameter)
		exec(new_parameter)

	alias_model_components(new_model)
	for new_initial in sorted(set(new_initials)):
		if verbose:
			print(new_initial)
		exec(new_initial)

	for new_rule in sorted(set(new_rules)):
		if verbose:
			print(new_rule)
		exec(new_rule)

	for new_observable in sorted(set(new_observables)):
		if verbose:
			print(new_observable)
		exec(new_observable)

	return new_model

def get_rule(model, name, verbose = False):
	for rule in model.rules:
		if name.replace('-','_') == rule.name:
			print(rule)
			break

def get_parameter(model, name, verbose = False):
	print(model.parameters._map[name])
