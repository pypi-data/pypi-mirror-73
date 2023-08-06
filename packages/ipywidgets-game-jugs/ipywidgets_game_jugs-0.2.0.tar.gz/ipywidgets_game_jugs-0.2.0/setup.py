import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipywidgets_game_jugs", 
    version="0.2.0",
    author="Edwige GROS",
    author_email="edwige.gros@laposte.net",
    description="The water jug riddle with Jupyter Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.u-psud.fr/edwige.gros/ipywidgets-games.git",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
     install_requires = ['timer', 'ipywidgets', 'ipycanvas', 'valueplayerwidget'],
    python_requires='>=3.6',
)
