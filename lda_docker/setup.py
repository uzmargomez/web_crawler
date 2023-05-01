from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='lda',
    version='0.0.1',
    description='This microservice gets the News Database from mongo and does the LDA algorithm',
    long_description=readme(),
    classifiers=[
        'License :: OSI Approved :: MIT Licence',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],

    keywords='',
    url='',
    author='Ricardo Quintero & Roberto Rodríguez & Uzmar Gómez',
    author_email='ricardo.quintero@softtek.com & robertoc.rodriguez@softtek.com & uzmar.gomez@softtek.com',
    license='MIT',

    python_requires='>=3.7',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "flask==2.3.2",
        "statistics",
        "pymongo",
        "pandas",
        "collections-extended",
        "matplotlib",
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-lda=lda_docker:lda_app']
    }
)
