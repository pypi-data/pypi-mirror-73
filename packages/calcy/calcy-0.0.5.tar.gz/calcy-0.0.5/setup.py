from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='calcy',
    version='0.0.5',
    description='A basic calculator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='',
    author='Deepak Jha',
    author_email='deepakjha18598@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)