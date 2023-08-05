import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pgex",
    version="0.0.3",
    author="Ivan Foke",
    author_email="ivan.foke@gmail.com",
    description="A Python PyGame package extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IvanFoke/pgex",
    packages=setuptools.find_packages(),
    # package_dir={'': 'pgex'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)

# python setup.py sdist bdist_wheel
