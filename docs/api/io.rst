File I/O
========

Thin wrappers around ``matplotlib.Figure.savefig`` for common workflows:
export multiple formats in one call, or save-and-display SVGs sized for
notebooks/reports. These functions accept the same ``savefig`` kwargs you're
used to; the tables highlight the custom arguments.

.. list-table:: ``save_formats`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``fig`` / ``image_stem``
     - Figure to export and the path without extension (e.g., ``\"out/figure\"``).
       Parent directories are created automatically.
   * - ``formats`` (default ``(\"svg\", \"png\", \"pdf\", \"eps\")``)
     - Iterable of extensions to write. Keep a tuple to control order.
   * - ``bbox_inches`` (optional)
     - Forwarded to ``savefig`` when you need ``\"tight\"`` or a custom bbox.

.. list-table:: ``save_and_show`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``fig``
     - Figure to save; closed after saving to avoid double-display in notebooks.
   * - ``image_path`` (default ``None``)
     - Destination file path. When ``None`` a temporary SVG is created.
   * - ``size`` / ``unit`` (defaults ``600`` / ``\"pt\"``)
     - Target display width and unit for Jupyter/HTML rendering. Height keeps the
       SVG aspect ratio.

.. list-table:: ``show`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``image_path``
     - Path to an SVG file. Width and height inside the SVG are updated for inline
       display.
   * - ``size`` / ``unit``
     - Final inline width and its unit (points by default). Height scales to fit.

Example

.. code-block:: python

   fig, ax = plt.subplots()
   ax.plot(x, y)
   dm.save_formats(fig, \"report/figures/example\", formats=(\"png\", \"svg\"), dpi=300)
   dm.save_and_show(fig, \"report/figures/example.svg\", size=520)

.. autofunction:: dartwork_mpl.save_formats
.. autofunction:: dartwork_mpl.save_and_show
.. autofunction:: dartwork_mpl.show
