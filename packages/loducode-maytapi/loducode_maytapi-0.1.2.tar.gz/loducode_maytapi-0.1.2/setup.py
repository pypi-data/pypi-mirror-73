from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='loducode_maytapi',
    packages=['loducode_maytapi'],  # this must be the same as the name above
    version='0.1.2',
    description='Non official maytapi library python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Cristian Dulcey',
    author_email='cristian@loducode.com',
    url='https://github.com/UnTalDulcey/loducode_maytapi',  # use the URL to the github repo
    download_url='https://github.com/UnTalDulcey/loducode_maytapi/tarball/0.1',
    keywords=['maytapi', 'whatsapp', 'loducode'],
    classifiers=[],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    setup_requires=['wheel']
)
