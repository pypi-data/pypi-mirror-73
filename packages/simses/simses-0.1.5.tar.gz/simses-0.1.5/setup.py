from setuptools import setup, find_packages

setup(
    name='simses',
    packages=find_packages(),
    include_package_data=True,
    version='0.1.5',
    description='Simulation for Stationary Storage Systems (SimSES)',
    long_description='Simulation for Stationary Storage Systems (SimSES). SimSES enables a detailed '
                     'simulation and evaluation of stationary energy storage systems with the '
                     'current main focus on lithium-ion batteries.',
    url='https://gitlab.lrz.de/open-ees-ses/simses',
    download_url='https://gitlab.lrz.de/open-ees-ses/simses/-/archive/simses_v015/simses-simses_v015.tar.gz',
    author='Daniel Kucevic, Marc Möller',
    author_email='simses.ees@ei.tum.de',
    license='BSD 3-Clause "New" or "Revised" License',
    install_requires=['scipy',
                      'numpy',
                      'pandas',
                      'plotly',
                      'matplotlib',
                      'pytest',
                      'pytz'
                      ],


    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],
)