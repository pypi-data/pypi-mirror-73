from setuptools import setup, find_packages

setup(
    name='danplotlib',
    version='0.4',
    author='Daniel Berninghoff',
    url = 'https://github.com/burneyy/danplotlib',
    download_url = 'https://github.com/burneyy/danplotlib/archive/v0.3.tar.gz',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'matplotlib'
    ]
)

