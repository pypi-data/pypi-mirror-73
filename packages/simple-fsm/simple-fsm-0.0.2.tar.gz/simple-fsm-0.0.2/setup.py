import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='simple-fsm',
    version='0.0.2',
    author='Frey Waid"',
    author_email='logophage1@gmail.com',
    description='Pythonic FSM',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/freywaid/fsm',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)
