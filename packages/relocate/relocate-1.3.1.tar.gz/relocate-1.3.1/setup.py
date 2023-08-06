from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='relocate',
      version='1.3.1',
      license='MIT',
      author='Sandip Palit',
      author_email='sandippalit009@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      description='Relocate will organise your files in separate folders, according to month of creation and then according to extensions.',
      packages=['relocate'],
      python_requires='>=3.6',
      zip_safe=False)