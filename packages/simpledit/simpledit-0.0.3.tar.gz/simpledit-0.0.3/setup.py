from setuptools import setup

setup(name='simpledit',
    version='0.0.3',
    description='',
    url='https://gitlab.com/torresed/simpledit',
    author='Programmers',
    author_email='noreply@ufl.edu',
    license='GPL3',
    packages=['simpledit'],
    install_requires=['Pillow', 'PyQt5', 'PyQt5-sip'],
    include_package_data=True,
    scripts=['simpledit/SimplEdit'])