from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name = 'nse50bse30',
    version='0.0.2',
    description= 'Python Package to scrap NSE 50 and BSE 30 tickers',
    py_modules = ['scrapTickers'],
    package_dir= {'': 'src'},
    classifiers = [
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    long_description= long_description,
    long_description_content_type= "text/markdown",
    install_requires = [
        "requests > 2.20.1",
    ],
    extras_require= {
        "dev": [
            "pytest>=3.7",
        ],

    },
    url= 'https://github.com/Git4Manohar/NSE50BSE30',
    author= 'Radha Manohar Jonnalagadda',
    author_email= 'email4manohar@gmail.com',
)