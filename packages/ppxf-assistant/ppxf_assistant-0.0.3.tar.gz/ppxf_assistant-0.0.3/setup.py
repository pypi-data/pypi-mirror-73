import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppxf_assistant", # Replace with your own username
    version="0.0.3",
    author="Diego Gonzalez",
    author_email="djgh.117@gmail.com",
    description="A small package that can make using ppxf easier, specially for integrated field spectra.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy',
          'matplotlib',
          'astropy',
          'panel'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)