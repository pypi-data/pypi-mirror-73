from os.path import dirname, join, abspath, pardir
from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

with open(join(dirname(__file__), 'clinicadl/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

this_directory = abspath(dirname(__file__))
with open(join(this_directory, pardir,  'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_reqs = parse_requirements(join(this_directory, pardir, 'requirements.txt'), session='hack')
reqs = [str(ir.req) for ir in install_reqs]

setup(
        name = 'clinicadl',
        version = version,
        description = 'Deep learning classification with clinica',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url = 'https://github.com/aramis-lab/AD-DL',
        license = 'MIT license',
        author = 'ARAMIS Lab',
        maintainer = 'Mauricio DIAZ',
        maintainer_email = 'mauricio.diaz@inria.fr',
        packages = ['clinicadl', ],
        include_package_data=True,
        zip_safe=False,
        entry_points = {
            'console_scripts': [
                'clinicadl = clinicadl.main:main',
                ],
            },
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Operating System :: OS Independent',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            ],
        install_requires=reqs
        )
