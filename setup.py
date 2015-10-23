from setuptools import setup, find_packages

setup(
    name = 'United Project',
    version = '0.0',
    tests_require = ['pytest'],
    install_requires = ['PyPDF2>1.25', 'pytest>2.8'],
    package_dir = {'': 'src'},
    packages = find_packages('src')
    )
    

