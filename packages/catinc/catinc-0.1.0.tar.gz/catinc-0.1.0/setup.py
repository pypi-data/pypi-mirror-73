from setuptools import find_packages, setup


setup(
    name="catinc",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False
)