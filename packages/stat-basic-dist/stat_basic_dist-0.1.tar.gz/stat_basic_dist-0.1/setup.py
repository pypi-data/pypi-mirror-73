from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stat_basic_dist",
    version="0.1",
    author="Sammy Kariuki",
    author_email="samkaris75@gmail.com",
    description="Gaussian and Bionomial distributions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam-karis/stat-dist",
    packages=find_packages(),
    install_requires=["matplotlib",],
    zip_safe=False,
)
