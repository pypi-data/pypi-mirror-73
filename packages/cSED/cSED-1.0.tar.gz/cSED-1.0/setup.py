import setuptools
from setuptools.extension import Extension

module1 = Extension("cSED", sources=['sed.c'])

setuptools.setup(
    name="cSED",
    version="1.0",
    license='MIT',
    author="sykwon",
    author_email="sykwon@kdd.snu.ac.kr",
    description="substring edit distance by c",
    ext_modules=[module1],
    package_data={
        'sedcode': [
            'sed.c',
        ]},
    classifiers= [
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)