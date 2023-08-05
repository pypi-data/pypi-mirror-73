from distutils.core import setup
setup(
  name = 'pgplot',
  packages = ['pgplot'],
  version = '0.1',
  license='MIT',
  description = 'Graphing functionality, integrated with pygame!',
  author = 'Jack Sanders',
  author_email = 'jacksanders404@gmail.com',
  url = 'https://github.com/JSanders02/pgplot',
  download_url = 'https://github.com/JSanders02/pgplot/archive/v_01.tar.gz',
  keywords = ['Graphs', 'Pygame', 'plotting'],
  install_requires=[
          'pygame',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)