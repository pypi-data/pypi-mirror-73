#!/usr/bin/python3
import setuptools

with open('README.rst') as readme:
    long_desc = readme.read()

setuptools.setup(
    name             = 'PGPy2',
    version          = '0.0.1',
    description      = 'Pretty Good Privacy for Python (forked from PGPy)',
    long_description = long_desc,
    author           = 'Daniel Kahn Gillmor',
    author_email     = "dkg@fifthhorseman.net",
    license          = "BSD",
    classifiers      = ['Development Status :: 1 - Planning',
                        'Operating System :: POSIX :: Linux',
                        'Operating System :: MacOS :: MacOS X',
                        'Operating System :: Microsoft :: Windows',
                        'Intended Audience :: Developers',
                        'Programming Language :: Python',
                        'Programming Language :: Python :: 3.7',
                        'Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 3.5',
                        'Programming Language :: Python :: Implementation :: CPython',
                        'Topic :: Security',
                        'Topic :: Security :: Cryptography',
                        'Topic :: Software Development :: Libraries',
                        'Topic :: Software Development :: Libraries :: Python Modules',
                        'License :: OSI Approved :: BSD License'],
    keywords        = ["OpenPGP",
                       "PGP",
                       "Pretty Good Privacy",
                       "GPG",
                       "GnuPG",
                       "openpgp",
                       "pgp",
                       "gnupg",
                       "gpg",
                       "encryption",
                       "signature", ],
    install_requires = [],
    url              = "https://github.com/dkg/PGPy2",
    download_url     = "https://github.com/dkg/PGPy2/archive/0.0.1.tar.gz",
    bugtrack_url     = "https://github.com/dkg/PGPy2/issues",
    packages = [
        "pgpy2",
    ],
)
