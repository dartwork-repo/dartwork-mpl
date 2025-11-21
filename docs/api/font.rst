Font Utilities
==============

Custom fonts bundled in ``asset/font`` are registered with matplotlib on import,
so they are available without manual configuration. ``fs`` and ``fw`` are small
helpers for offsetting the global rcParams font size/weight, and the gallery
utility ``plot_fonts`` previews every installed family. Use the quick
references below to pick sensible arguments.

.. list-table:: ``fs`` and ``fw`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``n`` (size offset)
     - For ``fs``: adds ``n`` to the current ``plt.rcParams["font.size"]``; use a
       small integer like ``2`` to bump titles or ``-1`` to shrink annotations.
   * - ``n`` (weight offset)
     - For ``fw``: increments the base font weight by ``100 * n``. Values like
       ``1`` map Regular → Medium, ``2`` to SemiBold/Bold; negative values lighten.

.. list-table:: ``plot_fonts`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``font_dir`` (default ``None``)
     - Folder of ``.ttf`` files to preview. Defaults to the package's bundled
       fonts when left ``None``.
   * - ``ncols`` (default ``3``)
     - Number of columns in the preview grid; increase for wider monitors.
   * - ``font_size`` (default ``11``)
     - Sample text size. Raise to gauge display uses; lower to preview dense layouts.

Example

.. code-block:: python

   import matplotlib.pyplot as plt
   import dartwork_mpl as dm

   fig, ax = plt.subplots()
   ax.set_title(\"Paper-ready\", fontsize=dm.fs(2), fontweight=dm.fw(1))

.. automodule:: dartwork_mpl.font
   :members:
   :undoc-members:
   :show-inheritance:

.. autofunction:: dartwork_mpl.fs
.. autofunction:: dartwork_mpl.fw
