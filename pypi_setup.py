from setuptools import setup, find_packages
from pbm import PBM

with open("README.md", encoding="utf-8") as fh:
    long_description: str = fh.read()

print(f"{PBM.latest_version=}")

setup(
    name="pbm-root",
    version=PBM.latest_version,
    author="elemenom",
    author_email="pixilreal@gmail.com",
    description="Version control at its fullest.",
    long_description=long_description,
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
)