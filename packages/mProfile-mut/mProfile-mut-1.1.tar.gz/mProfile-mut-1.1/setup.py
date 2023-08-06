from setuptools import setup, find_packages

setup(name='mProfile-mut',
      version='1.1',
      description='nucleotide-resolution mutation calling',
      url='https://github.com/aldob/mProfile',
      download_url = 'https://github.com/aldob/mProfile/archive/v1.1.tar.gz',
      packages=find_packages(),
      author='Aldo Bader',
      entry_points={
        'console_scripts': [
            'callMUT = mProfile.callMUT:main',
            'TransloCapture = mProfile.TransloCapture:main'            
        ],
      },
      zip_safe=False)
 