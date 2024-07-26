from setuptools import setup, find_packages

setup(
    name='queupy',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'peewee>=3.14.0',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    author='Enzo Lebrun',
    author_email='enzo.the@gmail.com',
    description='A queuing library based on Peewee',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EnzoTheBrown/queupy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
    ],
    python_requires='>=3.6',
)

