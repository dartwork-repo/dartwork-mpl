Color Utilities
===============

Importing ``dartwork_mpl`` registers a large catalog of named colors with
matplotlib (``dm.*`` plus Tailwind ``tw.``, Material ``md.``, Ant Design
``ant.``, Chakra ``chakra.``, and Primer ``primer.`` prefixes). These helpers
expose the color mixing routines used across the package and let you classify
colormaps before plotting. Each helper lists its parameters and return value
before jumping into examples.

``mix_colors(color1, color2, alpha=0.5)``
   - Parameters: two matplotlib-compatible colors (named strings or RGB tuples);
     ``alpha`` weights ``color1`` between 0 (all ``color2``) and 1 (all ``color1``).
   - Returns: blended RGB tuple.

``pseudo_alpha(color, alpha=1.0, background="white")``
   - Parameters: foreground ``color`` to soften, ``alpha`` for how transparent it
     should feel, and ``background`` color to mix toward when you cannot rely on
     real transparency (e.g., PDF export).
   - Returns: RGB tuple mixed against ``background``.

``classify_colormap(cmap)``
   - Parameters: colormap instance or name.
   - Returns: string label: ``"Categorical"``, ``"Sequential Single-Hue"``,
     ``"Sequential Multi-Hue"``, ``"Diverging"``, or ``"Cyclical"``.

Example

.. code-block:: python

   import matplotlib.pyplot as plt
   import dartwork_mpl as dm

   plt.plot(x, y, color="dm.blue5", label="Series A")
   lighter = dm.mix_colors("dm.blue5", "white", alpha=0.35)
   plt.fill_between(x, y, color=lighter)
   dm.classify_colormap(plt.colormaps["viridis"])  # -> "Sequential Multi-Hue"
   muted_line = dm.pseudo_alpha("dm.blue7", alpha=0.6, background="white")
   plt.plot(x, z, color=muted_line, label="Muted series")

.. automodule:: dartwork_mpl.color
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: dartwork_mpl.mix_colors
.. autofunction:: dartwork_mpl.pseudo_alpha
.. autofunction:: dartwork_mpl.classify_colormap
