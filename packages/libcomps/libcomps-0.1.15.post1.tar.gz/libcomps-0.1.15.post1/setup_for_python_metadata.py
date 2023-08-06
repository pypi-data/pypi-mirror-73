from distutils.core import setup
import sys

# This is a simple and fragile way of creating python metadata for non
# setuptools-guided installs (RPM builds). It's duplicate because of the
# scikit-build dependency in normal setup.py.
#
# This script has to have the version always specified as last argument.
version = sys.argv.pop()

setup(
    name='libcomps',
    description='Comps XML file manipulation library',
    version=version,
    license='GPLv2+',
    author='RPM Software Management',
    author_email='rpm-ecosystem@lists.rpm.org',
    url='https://github.com/rpm-software-management',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
