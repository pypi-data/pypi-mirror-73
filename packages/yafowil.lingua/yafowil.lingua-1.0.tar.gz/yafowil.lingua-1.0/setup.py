import os
from setuptools import (
    setup,
    find_packages,
)


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '1.0'
shortdesc = 'YAFOWIL - Lingua message extrator for yafowil.yaml based forms.'
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'CHANGES.rst',
    'LICENSE.rst'
]])


setup(
    name='yafowil.lingua',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='html input widgets form compound',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url=u'http://pypi.python.org/pypi/yafowil.lingua',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['yafowil'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'PyYAML',
        'lingua>=2.5',
    ],
    test_suite="yafowil.lingua.tests",
    entry_points="""
    [lingua.extractors]
    yafowil_yaml = yafowil.lingua.extractor:YafowilYamlExtractor
    """
)
