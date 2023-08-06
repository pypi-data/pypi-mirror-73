from setuptools import find_packages, setup


VERSION = "0.1.12"
DESCRIPTION = open("README.md", encoding="utf-8").read()


setup(
    name="biopartitioner",
    version=VERSION,
    packages=find_packages(exclude=["tests"]),
    url="https://github.com/pennlabs/github-project",
    project_urls={
        "Changelog": ("https://github.com/pennlabs/github-project/blob/master/CHANGELOG.md")
    },
    license="MIT",
    author="Penn Labs",
    author_email="admin@pennlabs.org",
    description="Penn Labs example description",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=["django>=2.0.0"],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6"
)