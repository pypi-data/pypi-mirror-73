import setuptools, sys
fileMap = open('src/prot/__init__.py').read().splitlines()
for i, m in enumerate(fileMap):
	if m.startswith('__version__ = '):
		verI, verS = i, m
		break
exec(verS)
vli = list(__version__)
doUpdate = True
doInstall = True
upgrade = False
if '--upgrade' in sys.argv or doUpdate:
	upgrade = True
	if int(vli[4]) == 9:
		upMinor = True
	else:
		upMinor = False
	if int(vli[2]) == 9 and upMinor:
		upMajor = True
	else:
		upMajor = False
	if upMinor:
		if not upMajor:
			vli[2] = str(int(vli[2]) + 1)
		vli[4] = str(0)
	else:
		vli[4] = str(int(vli[4]) + 1)
	if upMajor:
		vli[0] = str(int(vli[0]) + 1)
		vli[2] = str(0)
	try:
		sys.argv.remove('--upgrade')
	except: pass
ver = ''
for v in vli:
	ver += v
print('building prot v' + ver + '...')
if upgrade:
	fileMap[verI] = '__version__ = '+repr(ver)
	ns = ''
	for g in fileMap:
		ns += g+'\n'
	f = open('src/prot/__init__.py', 'w')
	f.write(ns)
	f.flush()
	f.close()
if len(sys.argv) <= 1:
	#sys.argv += ['-q']
	if doInstall:
		sys.argv += ['install']
	sys.argv += ['sdist', 'bdist_wheel', 'clean']

setuptools.setup(
	name="prot", version=ver,
	description='A Simple Tool That Contains Advance Functions.',
	long_description=open('README.md').read(), long_description_content_type='text/markdown',
	author="Alireza Poodineh", author_email='pa789892@gmail.com', url='https://www.pypi.org/user/Ali_p1986',
	packages=setuptools.find_packages(where="src"), package_dir={"": "src"},
	zip_safe=False,
	entry_points={"console_scripts": ["prot=prot:prot", "prot.pip=prot.pip:pip"]})