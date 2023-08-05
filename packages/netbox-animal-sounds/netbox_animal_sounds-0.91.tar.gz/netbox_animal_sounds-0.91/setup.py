from setuptools import setup, find_packages


setup(
    name='netbox_animal_sounds',
    version='0.91',
    description='An example NetBox plugin',
    url='https://github.com/netbox-community/netbox-animal-sounds',
    author='Jeremy Stretch',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    package_data={'mypackages': ['templates/*.html']},
    include_package_data=True,
)

