from distutils.core import setup

setup(name='simple-xls2json',
        version='1.0.1',
        description='Convert table data to json format output',
        author='Antiless',
        author_email='antiless.dev@gmail.com',
        keywords="xls json xlrd",
        py_modules=[
            'xls2json.xls2json'
        ],
        install_requires=[
            'xlrd'
        ]
      )