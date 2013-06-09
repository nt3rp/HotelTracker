from distutils.core import setup

setup(
    name='HotelTracker',
    version='0.1dev',
    author='Nicholas Terwoord',
    author_email='nterwoord@alumni.uwaterloo.ca',
    packages=['hoteltracker', 'hoteltracker.hotels', 'hoteltracker.test',],
    scripts=['bin/tracker.py'],
    url='http://pypi.python.org/pypi/HotelTracker/', #TODO: Change to github
    license='LICENSE.txt',
    description='Tools for checking hotel availability',
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4 == 4.1.3",
        "cssselect == 0.7.1",
        "httplib2 == 0.7.6",
        "lxml == 3.0.1",
        "mock == 1.0.1",
        "oauth2 == 1.5.211",
        "python-twitter == 0.8.2",
        "simplejson == 2.6.2",
        "wsgiref == 0.1.2"
    ],
)