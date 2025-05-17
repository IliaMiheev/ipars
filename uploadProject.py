from os import system

system('python setup.py sdist bdist_wheel')
system('twine upload dist/*')
system('rmdir /s /q build dist ipars.egg-info')
