import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="worklog-cli",
    version="0.0.3",
    author="Chris Proctor",
    author_email="pypi.org@accounts.chrisproctor.net",
    description="Worklog time-tracking utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cproctor/worklog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "arrow",
    ],
    scripts=["work"],
    python_requires='>=3.6',
)
