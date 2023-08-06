from setuptools import setup, find_packages

setup(name='business_id_nik',
      version='0.93.1',
      url='https://github.com/perlancar/python-business_id_nik',
      license='MIT',
      author='perlancar',
      author_email='perlancar@gmail.com',
      description='Parse Indonesian citizenship registration number (NIK)',
      classifiers=[
          # Trove classifiers
          # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Intended Audience :: Developers',
          'Natural Language :: Indonesian',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      keywords='indonesia',
      #packages=find_packages(exclude=['test']),
      packages=['business_id_nik'],
      long_description=open('README.md').read(),
      # setuptools > 38.6.0 needed for markdown README.md
      setup_requires=['setuptools>=38.6.0'],
      zip_safe=False)
