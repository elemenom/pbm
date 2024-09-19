from setuptools import setup, find_packages

from . import version

"""
git add --all
git commit
git push
python pypi_setup.py sdist bdist_wheel
twine upload dist/*
rm -rf dist build pbm.egg-info
"""

setup(
    name="pbm",
    version=str(version),
    author="elemenom",
    author_email="pixilreal@gmail.com",
    description="Version control at it's fullest.",
    long_description=(README:=open("README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/elemenom/pbm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    license="GPLv3",
    include_package_data=True,
    install_requires=[]
)

README.close()