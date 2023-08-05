# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

import argparse, os, pkg_resources, re, shutil, subprocess, sys
try:
	import importlib.resources # python3.7 stdlib
except:
	import importlib_resources # not part of the stdlib

def argsparser():
	parser = argparse.ArgumentParser(description = 'Reconstruction of Rule-Based Models from biological networks.', \
		epilog = '',
		formatter_class = argparse.RawTextHelpFormatter)

	# required arguments
	parser.add_argument('--network', metavar = 'str', type = str, required = True , help = 'a biolical network')
	# other options
	parser.add_argument('--output' , metavar = 'str', type = str, required = False, default = 'model.ipynb', help = 'model name (jupyter notebook)')
	parser.add_argument('--type_of', metavar = 'str', type = str, required = False, default = 'metabolic'  , help = 'type of biological network.')

	args = parser.parse_args()

	return args

def opts():
	return {
		'network' : args.network,
		'model'   : args.output + '.ipynb',
		'type'    : args.type_of,
		# non-user defined options
		'atlas'   : 'atlas_rbm',
		'dirpath1': 'notebooks/',
		'dirpath2': 'templates/',
		'mets'    : 'Rules from metabolic network.ipynb',
		'monomers': 'Monomer+Initials+Observables from metabolic network.ipynb',
		'template': 'model_template.ipynb',
		}

def xnb(filepath):
	cmd = os.path.expanduser('jupyter nbconvert --ClearOutputPreprocessor.enabled=True \
		--ExecutePreprocessor.timeout=None --allow-errors --to notebook --execute --inplace {:s}'.format(filepath))
	cmd = re.findall(r'(?:[^\s,"]|"+(?:=|\\.|[^"])*"+)+', cmd)
	out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
	#print(out, err)

if __name__ == '__main__':
	args = argsparser()
	opts = opts()

	if opts['type'] == 'metabolic':
		filepath = opts['network']
		shutil.copy2(filepath, './data_metabolism.txt')

		for ipynb in [opts['mets'], opts['monomers']]:
			filepath = opts['dirpath1'] + ipynb
			filepath = pkg_resources.resource_filename(opts['atlas'], filepath)
			shutil.copy2(filepath, './' + ipynb.replace(' ', '_'))

			xnb(ipynb.replace(' ', '_'))

	else:
		sys.exit()

	# execute model
	filepath = opts['dirpath2'] + opts['template']
	filepath = pkg_resources.resource_filename(opts['atlas'], filepath)
	shutil.copy2(filepath, './' + opts['model'].replace(' ', '_'))

	xnb(opts['model'])
