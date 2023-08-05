from setuptools import setup, find_packages

package = 'PyYAML'
try:
    print(__import__(package))
except ImportError:
    print("Please install PyYAML before kangaroo-build")

setup(
   name="kangaroo-build",
   version="1.0.13.23",
   description="keep track of your build number, that's it.",
   long_description="a build tracker",
   author="Marco Marchesi",
   author_email="marchesimarco@gmail.com",
   packages=find_packages(),
   install_requires=[
       'PyYAML',
   ],
)