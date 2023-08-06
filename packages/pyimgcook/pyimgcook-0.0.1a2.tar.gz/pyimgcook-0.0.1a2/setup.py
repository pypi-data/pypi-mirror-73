from setuptools import setup, find_packages


setup(
    name="pyimgcook",
    version="0.0.1a2",
    author="ibegyourpardon",
    author_email="yiziyint@gmail.com",
    description="图像处理函数集",
    long_description="图像处理函数集",
    long_description_content_type="text/markdown",
    url="https://github.com/ibegyourpardon/pyimgcook",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
