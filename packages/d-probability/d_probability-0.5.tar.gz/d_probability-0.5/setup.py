
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='d_probability',
      version='0.5',
      description='Gaussian distributions',
      packages=['d_probability'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      author = "Nilayan Bose",
      zip_safe=False,

      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)