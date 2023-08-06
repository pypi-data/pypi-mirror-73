from setuptools import setup

setup(name='patronous',
      version='0.6',
      description='aws lambda function deployer',
      url='http://github.com/zkrhm/patronous',
      author='zkrhm',
      # author_email='"Zaky Rahim" <zaky.rahim@gmail>',
      license='MIT',
      packages=['patronous'],
    #   scripts=['patronous/cli']
      entry_points={
          'console_scripts': [
            'expecto=patronous.cli:main',
            'lumos=patronous.cli:lumos',
            'nox=patronous.cli:nox',
          ]
      },

      zip_safe=False)