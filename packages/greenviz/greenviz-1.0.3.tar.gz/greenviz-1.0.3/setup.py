from setuptools import setup
from distutils.core import setup
import os
cwd=os.getcwd()
setup(
      name="greenviz",
      version="1.0.3",
      description="welcome",
      author="R.raja subramanian",
      url="https://github.com/RRajaSubramanian/Greenviz",
      author_email="rajasubramanian.r1@gmail.com",
      py_modules=["greenviz"],
      package_dir={"":"src"},
      data_files=[("",["shiridi pic rezied.jpeg","bg1.jpg","raja12.jpeg","resized achuth pic.jpeg"])],
      include_package_data=True,
      install_requires=["pillow","matplotlib","sklearn","dnspython","pandas","pymongo","numpy","IPython","graphviz"]
      )

