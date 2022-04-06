from setuptools import setup

setup(
    name='TeX2LMS',
    url='https://github.com/viper2642/TeX2LMS',
    author='David Pfefferle',
    author_email='pfefferle.david@gmail.com',
    packages=['tex2lms'],
    install_requires=['pandas','sympy','csv','os'],
    version='0.0.2',
    license='GPL-3.0',
    description="Create pools of questions for Blackboard LMS from spreadsheet with LaTeX statements",
    long_description=open('README.md').read(),
)
