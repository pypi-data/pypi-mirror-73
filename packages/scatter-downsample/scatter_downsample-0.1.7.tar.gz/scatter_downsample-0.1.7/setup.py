import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scatter_downsample", 
    version="0.1.7",
    author="jaqueline_lu",
    author_email="jellalu21@gmail.com",
    description="A module used for downsampling high resolution images using the scattering transform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={'console_scripts':['scatter_downsample=scatter_downsample.__main__:main']},
    url="https://github.com/twardlab/ScatteringDownsample",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)