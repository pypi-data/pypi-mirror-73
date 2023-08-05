from setuptools import setup, find_packages

setup(
   name="kangaroo-build",
   version="1.0.10",
   description="keep track of your build number, that's it.",
   long_description="a build tracker",
   author="Marco Marchesi",
   author_email="marchesimarco@gmail.com",
   packages=find_packages(),
   install_requires=[
       'PyYAML',
   ],
)