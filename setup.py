from os.path import join, dirname
from setuptools import setup
base_dir = dirname(__file__)

def read(filename):
    f = open(join(base_dir, filename))
    try:
        return f.read()
    except OSError:
        return ''

def get_version(package_name, default='0.1'):
    try:
        f = open(join(base_dir, package_name, 'version.py'))
    except IOError:
        try:
            f = open(join(base_dir, package_name + '.py'))
        except IOError:
            return default
    for line in f:
        parts = line.split()
        if parts[:2] == ['__version__', '=']:
            default = parts[2].strip("'\"")
    return default

setup(
    name = 'django-caspy',
    version = get_version('caspy'),
    packages = ['caspy', 'caspy.api', 'caspy.domain'],
    include_package_data = True,
    install_requires = [
            'pytz',
            'PyYAML',
            'Django>=1.6,<1.9',
            'djangorestframework>=3.0',
        ],
    author = "Aryeh Leib Taurog",
    author_email = "caspy@aryehleib.com",
    description = "Simple double-entry accounting",
    long_description = read("README.rst") + '\n\n' + read("CHANGELOG.rst"),
    license = "BSD",
    keywords = "accounting finance bookkeeping",
    url = "https://bitbucket.org/altaurog/caspy",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
    ],
)
