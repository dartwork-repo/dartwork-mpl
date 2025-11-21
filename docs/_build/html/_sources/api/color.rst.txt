Color Utilities
===============

Importing ``dartwork_mpl`` registers a large catalog of named colors with
matplotlib (``dm.*`` plus Tailwind ``tw.``, Material ``md.``, Ant Design
``ant.``, Chakra ``chakra.``, and Primer ``primer.`` prefixes). These helpers
expose the color mixing routines used across the package and let you classify
colormaps before plotting.

Example

.. code-block:: python

   import matplotlib.pyplot as plt
   import dartwork_mpl as dm

   plt.plot(x, y, color=\"dm.blue5\", label=\"Series A\")
   lighter = dm.mix_colors(\"dm.blue5\", \"white\", alpha=0.35)
   plt.fill_between(x, y, color=lighter)
   dm.classify_colormap(plt.colormaps[\"viridis\"])  # -> \"Sequential Multi-Hue\"

.. automodule:: dartwork_mpl.color
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: dartwork_mpl.mix_colors
.. autofunction:: dartwork_mpl.pseudo_alpha
.. autofunction:: dartwork_mpl.classify_colormap
