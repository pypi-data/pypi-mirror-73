# from distutils.core import setup
import setuptools

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(name='simple-xls2json',
        version='1.0.5',
        description='Convert table data to json format output',
        url='https://github.com/auv1107/xls2json',
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        author='Antiless',
        author_email='antiless.dev@gmail.com',
        keywords="xls json xlrd",
        py_modules=[
            'xls2json.xls2json'
        ],
        packages=setuptools.find_packages()
      )