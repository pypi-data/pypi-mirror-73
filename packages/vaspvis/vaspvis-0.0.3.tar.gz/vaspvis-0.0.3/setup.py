from setuptools import setup

with open('./README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='vaspvis',
    version='0.0.3',
    description='A highly flexible and customizable library for visualizing electronic structure data from VASP calculations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['vaspvis'],
    install_requires = ['pymatgen', 'matplotlib', 'numpy', 'pandas'],
    url='https://github.com/DerekDardzinski/vaspvis',
    autour='Derek Dardzinski',
    autour_email='dardzinski.derek@gmail.com',
)
