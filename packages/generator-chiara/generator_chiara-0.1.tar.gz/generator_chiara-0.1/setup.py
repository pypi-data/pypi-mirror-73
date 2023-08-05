import setuptools

with open("README.md" , "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='generator_chiara',  # Replace with your own username e.g example-pkg-name
    version='0.01',
    author='Chiara N',
    author_email='chiaranic88@gmail.com',
    description='A small example of package from Chiara',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    license=license,
    packages=setuptools.find_packages(exclude=('tests*', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ],
    python_requires='>=3.6',
)

