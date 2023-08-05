from setuptools import setup, find_packages

setup(
   name="kangaroo-build",
   version="1.0.9",
   description="keep track of your build number, that's it.",
   author="Marco Marchesi",
   author_email="marchesimarco@gmail.com",
   packages=find_packages(),
   install_requires=[
       'PyYAML',
   ],
)