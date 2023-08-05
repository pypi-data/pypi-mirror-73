import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="valueplayerwidget",
    version="0.1.2",
    author="Edwige Gros",
    author_email="edwige.gros@laposte.net",
    description="The water jug riddle with Jupyter Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.u-psud.fr/edwige.gros/ValuePlayerWidget.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["timer", "ipywidgets"],
    dependency_links=["DelpyWidget@git+https://github.com/Edwauline/DelpyWidget.git"],
    python_requires=">=3.6",
)
