import setuptools


with open("requirements/base.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    install_requires=requirements,
    include_package_data=True,
    packages=setuptools.find_packages(exclude=("*.tests.*",)),
    package_data={
        "bopbot": ["static/*"]
    }
)
