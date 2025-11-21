Visualization Tools
===================

Quick visual diagnostics for the assets bundled with dartwork-mpl. Use them to
review palettes, pick colormaps by category, or validate fonts before building
plots. Argument guides below show which knobs to turn.

.. list-table:: ``plot_colormaps`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``cmap_list`` (default ``None``)
     - Iterable of colormap names/objects. When ``None`` all non-reversed maps
       are shown.
   * - ``ncols`` (default ``3``)
     - Columns in the grid. Balance this with your screen width to avoid shrinking.
   * - ``group_by_type`` (default ``True``)
     - When ``True``, colormaps are auto-classified and shown in separate figures
       (Sequential, Diverging, etc.). Set ``False`` for a single grid.
   * - ``group_spacing`` (default ``0.5``)
     - Extra padding between groups in the single-grid view (ignored when
       ``group_by_type`` is ``True``).

.. list-table:: ``plot_colors`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``ncols`` (default ``5``)
     - Columns per color library. Raise to pack more swatches per row.
   * - ``sort_colors`` (default ``True``)
     - Whether to sort within each library by hue/weight for easier scanning.

.. list-table:: ``plot_fonts`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``font_dir`` (default ``None``)
     - Directory of ``.ttf`` files. Defaults to bundled fonts when ``None``.
   * - ``ncols`` (default ``3``)
     - Columns in the font preview grid.
   * - ``font_size`` (default ``11``)
     - Sample text size so you can preview small/large usage.

Example

.. code-block:: python

   dm.plot_colormaps(group_by_type=True)  # Opens grouped figures
   dm.plot_colors(ncols=5)                # Shows named colors by library
   dm.plot_fonts(font_size=10)            # Preview installed font families

.. autofunction:: dartwork_mpl.plot_colormaps
.. autofunction:: dartwork_mpl.plot_colors
.. autofunction:: dartwork_mpl.plot_fonts
