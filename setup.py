from setuptools import find_packages, setup


def read_requirements(filename):
	with open(filename) as file:
		return [r.strip() for r in file.readlines()]


setup(
	name='helpinghand',
	packages=find_packages(),
	version='0.0.1',
	description='Some functions that help.',
	license='MIT',
	install_requires=read_requirements('requirements.txt'),
	test_require=read_requirements('dev_requirements.txt')
)
