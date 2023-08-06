import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipywidgets_game_wolf_goat_cabbage", 
    version="0.2.0",
    author="Edwige GROS",
    author_email="edwige.gros@laposte.net",
    description="The 'Wolf-Goat-Cabbage' game with Jupyter Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.u-psud.fr/edwige.gros/ipywidgets-games/tree/master/Wolf-Goat-Cabbage",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
