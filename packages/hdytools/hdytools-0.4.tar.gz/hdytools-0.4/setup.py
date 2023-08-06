import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='hdytools',
    version='0.4',
    description='Machine Learning Libraries',
    author='horngderyang',
    author_email='horngderyang@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/horngderyang/hdytools',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',)