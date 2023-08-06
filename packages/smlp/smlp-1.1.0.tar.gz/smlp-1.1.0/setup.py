# encoding =utf-8

from setuptools import setup, find_packages

setup(
    name='smlp',
    version='1.1.0',
    description='a shallow machine learning toolkit for text PreProcessing',
    url='https://github.com/cbai066',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Carl Bai',
    author_email='carlbai66@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={
        'smlp': ['data/*'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'jieba',
        'textrank4zh',
        'pandas',
        'tqdm',
        'pytest',  
    ],
    extras_require={
        'http': ['flask', 'flask-compress', 'flask-cors', 'flask-json']
    },
    classifiers=(
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ),
    keywords='shallow_machine_learning_platform nlp machine_learning jieba segment segments encoding serving',
)
