"""Micro service communication library."""
from pip.req import parse_requirements
from setuptools import setup


dependencies = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in dependencies]
setup(
    name='inet',
    version='0.2.3',
    url='https://github.com/danceasarxx/inet',
    license='BSD',
    author='Arewa Olakunle',
    author_email='arewa.olakunle@gmail.com',
    packages=["inet"],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=reqs,
    long_description=open("README.md").read(),
    entry_points={
        'console_scripts': [
            'inetserver = inet.inetserver:main',
            'inetproxy = inet.proxy:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
