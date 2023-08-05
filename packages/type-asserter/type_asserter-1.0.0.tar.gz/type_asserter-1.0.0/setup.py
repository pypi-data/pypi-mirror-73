from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='type_asserter',  # How you named your package folder (MyLib)
    packages=['type_asserter'],  # Chose the same as "name"
    version='1.0.0',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="This package enforces the functions' type hints at runtime, making sure that the types of the actual parameters and the return value match the types specified in the function signature.",  # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Valerio Neri',  # Type in your name
    author_email='valerioneri1997@gmail.com',  # Type in your E-Mail
    url='https://github.com/ValerioNeriGit/type_asserter.git',  # Provide either the link to your github or to your website
    download_url='https://github.com/user/reponame/archive/type-asserter_v1.0.0.tar.gz',  # I explain this later on
    keywords=['TYPE', 'TYPES', 'ASSERTION', 'TYPE ASSERTION', 'TYPE CHECKER', ],  # Keywords that define your package best
    install_requires=[
        'decorator'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
