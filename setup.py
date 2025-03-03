from setuptools import setup, find_packages  # setuptools is used to package the whole project so that it can be installed like a library.

# This is the setup function that defines basic information about the package
setup(
    name="src",  # Name of your package (project folder name)
    version="0.0.1",  # Version of your project (starting version)
    author="Ayaz Rabbani",  # Your name as the author of this project
    author_email="ayazr425@gmail.com",  # Your email ID
    packages=find_packages()  # This automatically detects all folders containing __init__.py files and treats them as packages
)
