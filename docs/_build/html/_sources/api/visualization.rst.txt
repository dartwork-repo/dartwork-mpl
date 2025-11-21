Visualization Tools
===================

Quick visual diagnostics for the assets bundled with dartwork-mpl. Use them to
review palettes, pick colormaps by category, or validate fonts before building
plots. Parameters and return values are spelled out so you can skim and run.

``plot_colormaps(cmap_list=None, ncols=3, group_by_type=True, group_spacing=0.5)``
   - Parameters:
     - ``cmap_list``: optional names/objects (defaults to all non-reversed maps).
     - ``ncols``: grid width.
     - ``group_by_type``: split into Sequential/Diverging/etc. figures when ``True``.
     - ``group_spacing``: extra padding when showing a single grid.
   - Returns:
     - ``(fig, axs)`` from the last rendered figure.

``plot_colors(ncols=5, sort_colors=True)``
   - Parameters:
     - ``ncols``: number of columns per grid.
     - ``sort_colors``: order by hue/weight within each library.
   - Returns:
     - list of ``matplotlib.figure.Figure`` objects (one per library).

``plot_fonts(font_dir=None, ncols=3, font_size=11)``
   - Parameters:
     - ``font_dir``: optional font directory.
     - ``ncols``: number of columns in the preview grid.
     - ``font_size``: sample size used in the preview.
   - Returns:
     - ``matplotlib.figure.Figure`` previewing the bundled or provided fonts.

Example

.. code-block:: python

   dm.plot_colormaps(group_by_type=True)  # Opens grouped figures
   dm.plot_colors(ncols=5)                # Shows named colors by library
   dm.plot_fonts(font_size=10)            # Preview installed font families

.. autofunction:: dartwork_mpl.plot_colormaps
.. autofunction:: dartwork_mpl.plot_colors
.. autofunction:: dartwork_mpl.plot_fonts
