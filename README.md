# dLux Tutorials

This repo contains tutorial notebooks for using [dLux](https://github.com/LouisDesdoigts/dLux) and related tools. The notebooks are designed to be run locally, and this package provides a convenient way to install the necessary dependencies. It also allows for the easy addition of new tutorials and examples from users without needing to update the core library!

Minimal install setup for running the tutorial notebooks locally.

## Quickstart

```bash
git clone https://github.com/LouisDesdoigts/dLux_tutorials.git
cd dLux_tutorials
pip install .
```

Then you should be able to open and run the tutorials yourself directly!

## Exporting Notebooks to docs

This repo also allows the easy export of jupyter notebooks to markdown files for hosting on the [dLux docs](https://dlux.readthedocs.io/en/latest/). To export the notebooks, simply run:

```bash
python export_notebooks.py tutorials/<notebook_of_choice>.ipynb 
```

This will export the notebook to `tutorials/<notebook_of_choice>.md`, and populate the `tutorials/assets/<notebook_of_choice>/` directory with any images or other assets, which can then be added to the docs of the main repo directly!