'''
Used to build an app using py2app and py2exe
Open the terminal, and use cd to get to the proper folder
Then, at the command line, enter the following:

  python setup.py py2app

The resulting file will be in the dist folder.  And you can throw away the build folder

'''

from setuptools import setup

APP = ['OO Lines And Boxes.py']
DATA_FILES = [('', ['images']), ('', ['sounds'])]
OPTIONS = {'iconfile' : 'LinesAndBoxes.icns',}

setup(
        app = APP,
        data_files = DATA_FILES,
        options = {'py2app' : OPTIONS},
        setup_requires = ['py2app'],
        )
