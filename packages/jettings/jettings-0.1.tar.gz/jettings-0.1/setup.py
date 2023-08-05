from distutils.core import setup
setup(
  name = 'jettings',         
  packages = ['jettings'],   
  version = '0.1',      
  license='MIT',        
  description = 'A super simple JSON based settings (jettings) manager for all your python application needs',   
  author = 'zoran ilievski',
  author_email = 'pythonic@clientuser.net',
  url = 'https://github.com/zorani/jettings',
  download_url = 'https://github.com/zorani/jettings/archive/v_01.tar.gz', 
  keywords = ['JSON', 'SETTING', 'SETTINGS', 'CONFIGURATION','MANAGER'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',     
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)