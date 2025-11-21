Font Utilities
==============

Custom fonts bundled in ``asset/font`` are registered with matplotlib on import,
so they are available without manual configuration. ``fs`` and ``fw`` are small
helpers for offsetting the global rcParams font size/weight, and the gallery
utility ``plot_fonts`` previews every installed family.

``fs(n)``
   - Parameters:
     - ``n``: number of points to add to ``plt.rcParams["font.size"]``.
   - Returns:
     - new font size (float) for use in labels/titles.

``fw(n)``
   - Parameters:
     - ``n``: integer weight step multiplied by 100 and added to ``plt.rcParams["font.weight"]``.
   - Returns:
     - integer font weight.

``plot_fonts(font_dir=None, ncols=3, font_size=11)``
   - Parameters:
     - ``font_dir``: optional directory of ``.ttf`` files (defaults to bundled fonts).
     - ``ncols``: number of columns in the preview grid.
     - ``font_size``: sample size used in the preview.
   - Returns:
     - ``matplotlib.figure.Figure`` containing the preview grid.

Example

.. code-block:: python

   import matplotlib.pyplot as plt
   import dartwork_mpl as dm

   fig, ax = plt.subplots()
   ax.set_title("Paper-ready", fontsize=dm.fs(2), fontweight=dm.fw(1))
   dm.plot_fonts(ncols=4, font_size=12)  # inspect available families

.. automodule:: dartwork_mpl.font
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: dartwork_mpl.fs
.. autofunction:: dartwork_mpl.fw
