from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='swarm-cg',
    version='1.0.0',
    description='Tools for automatic parametrization of bonded terms in coarse-grained molecular models',
	author='Charly Empereur-mot',
	author_email='charly.empereur@gmail.com',
    long_description_content_type="text/markdown",
    long_description=README,
    packages=find_packages(include=['swarmcg', 'swarmcg.*']),
    install_requires=[
        'numpy>=1.16.4',
        'scipy>=1.2.2',
        'pyemd>=0.5.1',
        'matplotlib>=2.2.4',
        'fst-pso>=1.4.12',
        'MDAnalysis>=1.0.0'
    ],
    entry_points={
        'console_scripts': [
        	'scg_model_opti=swarmcg.optimize_model:main',
        	'scg_model_eval=swarmcg.evaluate_model:main'
        	# 'scg_opti_check=swarmcg.analyze_optimization:main'
        ]
    }
)