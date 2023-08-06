from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='mcLib',
  version='0.0.5',
  description='This is just a base package for logging and other handy functions',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Michael Robinson',
  author_email='michael.robinson@kochind.com',
  license='MIT',
  py_modules=['AppConfiguration', 'mcr_mclib'],
  package_dir={'':'src'},
  install_requires=[ 'json_minify', 'pandas', 'numpy' ]
  
)
 