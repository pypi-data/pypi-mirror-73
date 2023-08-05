import setuptools

setuptools.setup(
  name = 'update-conan-local',    
  packages = setuptools.find_packages(), 
  version = '0.0.1-6',
  license='MIT',        
  description = 'Update Conan Local Cache',  
  author = 'Wei Wan', 
  author_email = 'emwanwei@gmail.com',
  url = 'https://github.com/weiwan-gmail/update-conan-local',
  download_url = 'https://github.com/user/weiwan-gmail/archive/v_01.tar.gz',
  keywords = ['pypi', 'conan', 'cache'],
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
  python_requires='>=3.6',
)