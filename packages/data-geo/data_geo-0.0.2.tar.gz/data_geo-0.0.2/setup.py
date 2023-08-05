from setuptools import setup, find_packages

setup(name='data_geo',
      version='0.0.2',
      description='DataDBS for geojson',
      url='http://www.gitlab.com/dpineda/data_geo',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['data_geo'],
      install_requires=find_packages(),
      package_dir={'data_geo': 'data_geo'},
      package_data={
          'data_geo': ['../doc', '../docs', '../requeriments.txt']},
      zip_safe=False)
