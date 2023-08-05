try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A LMTP server class',
    'long_description': 'A LMTP counterpart to smtpd in the Python standard library',
    'author': 'Matt Molyneaux',
    'url': 'https://github.com/moggers87/lmtpd',
    'download_url': 'http://pypi.python.org/pypi/lmtpd',
    'author_email': 'moggers87+git@moggers87.co.uk',
    'version': '6.2.0',
    'license': 'MIT', # apparently nothing searches classifiers :(
    'packages': ['lmtpd'],
    'data_files': [('share/lmtpd', ['LICENSE', 'PY-LIC'])],
    'name': 'lmtpd',
    'classifiers': [
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: Python Software Foundation License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email'],
    'test_suite': 'lmtpd.tests'
}

setup(**config)
