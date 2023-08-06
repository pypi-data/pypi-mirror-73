from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='kavanaghdistributions',
    version='1',
    description='Various Functions and Methods for sample distributions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/BAK2K3/kavanaghdistributions',
    author='Benjamin Kavanagh',
    author_email='benjamin.a.kavanagh@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    install_requires=['numpy'],
    python_requires='>=3.7',
    zip_safe=False)