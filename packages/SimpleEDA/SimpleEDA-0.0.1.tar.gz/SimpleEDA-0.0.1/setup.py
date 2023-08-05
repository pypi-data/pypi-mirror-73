import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleEDA", 
    version="0.0.1",
    author="Muhammad Shahid Sharif",
    author_email="chshahidhamdam@gmail.com",
    description="A wrapper around Pandas to perform Simple EDA with less code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shahid017/SimpleEDA",
    packages=['simple_eda'],
    install_requires = ['matplotlib',
'numpy',
'pandas',
'scikit-learn',
'scipy',
'seaborn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
