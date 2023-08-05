build-package:
	rm -rf build
	rm -rf pleione.egg-info
	rm -rf __pycache__
	python3 setup.py bdist_wheel sdist

clean-package:
	python3 setup.py clean

install-package:
	python3 setup.py clean build install

upstream:
	git remote -v
	git remote add upstream https://github.com/glucksfall/atlas.git

sync:
	git fetch upstream
	git checkout master
	git merge upstream/master
	git push --repo=git@github.com:networkbiolab/atlas.git
