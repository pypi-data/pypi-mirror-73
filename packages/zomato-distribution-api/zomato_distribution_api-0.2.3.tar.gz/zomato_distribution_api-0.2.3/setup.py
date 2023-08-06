from setuptools import setup, find_packages

with open("README.md", "r") as f:
      long_description = f.read()

setup(name='zomato_distribution_api',
      version='0.2.3',
      description='provides wrapper for the zomato web api',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      author='Chetan Raj Rupakheti',
      author_email='chetanrrk@gmail.com',
      python_requires='>=3',
      zip_safe=False)



