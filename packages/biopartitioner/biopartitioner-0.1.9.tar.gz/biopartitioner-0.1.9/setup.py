try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
from distutils.core import setup
readme = open("README.md", "r").read()

setup(
    name = 'biopartitioner',
    packages = ['biopartitioner'],
    package_data={'biopartitioner':['*.*', 'partitioner/*']},
    version = '0.1.9',
    python_requires="==3.*,>=3.7.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/david30907d/bio-partitioner',
    download_url = 'https://github.com/david30907d/bio-partitioner',
    license="Apache License 2.0",
    keywords = ['bio-informatics', 'partition'],
    classifiers = [],
    install_requires=["pyvcf==0.*,>=0.6.8", "requests==2.*,>=2.23.0"],
    extras_require={
        "dev": [
            "bandit==1.*,>=1.6.2",
            "black==19.*,>=19.10.0.b0",
            "isort==4.*,>=4.3.21",
            "mypy==0.*,>=0.770.0",
            "pylint==2.*,>=2.4.4",
            "pytest==5.*,>=5.4.1",
            "pytest-cov==2.*,>=2.8.1",
            "safety==1.*,>=1.8.7",
        ]
    },
    zip_safe=True
)