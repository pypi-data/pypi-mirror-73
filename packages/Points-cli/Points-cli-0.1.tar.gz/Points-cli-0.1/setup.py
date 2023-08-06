import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Points-cli",
    version="0.1",
    author="Ridhiwan Ramadhan Mseya",
    author_email="ridhiwanmseya@gmail.com",
    description="Plots and measures angles and distances between points in 3-Dimensions",
    long_description=long_description,
    license="MIT",
    py_modules=["Points_cli.Points_cli"],
    scripts=["Points_cli/Points_cli.py"],
    long_description_content_type="text/markdown",
    url="https://github.com/Ridhiwan/Points-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "Points-cli=Points_cli:main"
        ]
    }
)
