from os import system

system('rmdir /s /q build dist ipars.egg-info')
system('python setup.py sdist bdist_wheel')
system('twine upload dist/*')
