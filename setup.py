import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_collector",
    version="0.0.21",
    author="Michael Watson-Fore",
    author_email="michael-fore@sbcglobal.net",
    description="A small data collection package for small to medium data collection efforts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Michael-fore/py_collector",
    project_urls={
        "Bug Tracker": "https://github.com/Michael-fore/py_collector/issues",
    },
     keywords='dataharvesting, datascraping, scraping, datacollection',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.2",
)