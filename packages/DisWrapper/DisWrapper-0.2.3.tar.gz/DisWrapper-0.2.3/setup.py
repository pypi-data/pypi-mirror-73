from distutils.core import setup
setup(
  name = 'DisWrapper',         # How you named your package folder (MyLib)
  packages = ['DisWrapper'],   # Chose the same as "name"
  version = '0.2.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Small python wrapper for discord',   # Give a short description about your library
  author = 'Josh Scragg',                   # Type in your name
  author_email = 'josh@scragg.co.nz',      # Type in your E-Mail
  url = 'https://github.com/JoshScragg/DisPy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/JoshScragg/DisWrapper/archive/0.2.3.tar.gz',    # I explain this later on
  keywords = ['Discord', 'Wrapper', 'Bot', 'Selfbot', 'Dis', 'library'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'websocket',
          'requests',
          'websocket-client',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',      #Specify which pyhton versions that you want to support
  ],
)
