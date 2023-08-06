import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="code_aster_win",  # Replace with your own username
    version="0.0.5",
    author="Daniel Steinegger",
    author_email="steinegger.daniel@gmail.com",
    description="Installs code_aster and makes it easy accessible via python and shell/cmd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    py_modules=["code_aster_win"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
          'pathlib'
    ],
    include_package_data=True,
    #scripts=['bin/py_as_run'],
    entry_points = {
        'console_scripts': ['py_as_run=code_aster.command_line:py_as_run','py_run_astk=code_aster.command_line:py_run_astk'],
    },
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
)
