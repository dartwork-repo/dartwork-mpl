Color Utilities
===============

Importing ``dartwork_mpl`` registers a large catalog of named colors with
matplotlib (``dm.*`` plus Tailwind ``tw.``, Material ``md.``, Ant Design
``ant.``, Chakra ``chakra.``, and Primer ``primer.`` prefixes). These helpers
expose the color mixing routines used across the package and let you classify
colormaps before plotting. The tables below clarify what to pass where.

.. list-table:: ``mix_colors`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``color1`` / ``color2``
     - Any matplotlib color string or RGB tuple (e.g., ``"dm.blue5"`` or ``(0.1, 0.2, 0.7)``).
   * - ``alpha`` (default ``0.5``)
     - Weight for ``color1``; set to ``0`` for pure ``color2`` or ``1`` for pure
       ``color1``. Values between 0–1 linearly blend the two.

.. list-table:: ``pseudo_alpha`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``color``
     - Foreground color to soften (any matplotlib color spec).
   * - ``alpha`` (default ``1.0``)
     - Opacity-like weight: lower mixes in more of ``background`` without using
       real transparency.
   * - ``background`` (default ``"white"``)
     - Base color to blend toward when faking transparency.

.. list-table:: ``classify_colormap`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``cmap``
     - ``matplotlib.colors.Colormap`` instance or name; returns a readable label
       (Categorical, Sequential Single-Hue, Sequential Multi-Hue, Diverging, or
       Cyclical) for quick palette choices.

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
