from distutils.core import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    # Application name:
    name="inet",

    # Version number (initial):
    version="0.1.1",

    # Application author details:
    author="Arewa Olakunle",
    author_email="arewa.olakunle@gmail.com",

    # Packages
    packages=["inet"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/inet_v011/",

    #
    # license="LICENSE.txt",
    description="Micro service messaging using zeromq",
    long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=reqs,
)
