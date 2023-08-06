from setuptools import setup, find_packages

classifiers = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Education',
               'Operating System :: MacOS :: MacOS X',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3'
              ]

setup(
    name = "LinkedListModule",
    version = "0.0.1",
    description = "This is a basic implementation of single linked lists in Python.",
    long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = "",
    author = "Abeer Rao",
    author_email = "abeerrao@icloud.com",
    license = "MIT",
    classifiers = classifiers,
    keywords = "LinkedLists",
    packages = find_packages(),
    install_requires = ['']
)