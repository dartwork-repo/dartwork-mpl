File I/O
========

Thin wrappers around ``matplotlib.Figure.savefig`` for common workflows:
export multiple formats in one call, or save-and-display SVGs sized for
notebooks/reports. They accept the usual ``savefig`` keyword arguments; the
custom ones are called out below.

``save_formats(fig, image_stem, formats=("svg", "png", "pdf", "eps"), bbox_inches=None, **kwargs)``
   - Parameters:
     - ``fig``: figure to export.
     - ``image_stem``: path without extension; parent folders are created.
     - ``formats``: iterable of formats to write.
     - ``bbox_inches``: optional value forwarded to ``savefig``.
     - ``**kwargs``: any extra arguments passed to ``savefig``.
   - Returns:
     - ``None`` after writing one file per requested format.

``save_and_show(fig, image_path=None, size=600, unit="pt", **kwargs)``
   - Parameters:
     - ``fig``: figure to save (closed after saving).
     - ``image_path``: destination path or ``None`` to use a temporary SVG.
     - ``size``: inline display width.
     - ``unit``: unit for ``size`` (defaults to points).
     - ``**kwargs``: forwarded to ``savefig``.
   - Returns:
     - ``None``; displays the SVG inline (Jupyter/HTML).

``show(image_path, size=600, unit="pt")``
   - Parameters:
     - ``image_path``: SVG file to display.
     - ``size``: display width.
     - ``unit``: unit for ``size``.
   - Returns:
     - ``None``; shows the scaled SVG inline.

Example

.. code-block:: python

   fig, ax = plt.subplots()
   ax.plot(x, y)
   dm.save_formats(fig, "report/figures/example", formats=("png", "svg"), dpi=300)
   dm.save_and_show(fig, "report/figures/example.svg", size=520)

.. autofunction:: dartwork_mpl.save_formats
.. autofunction:: dartwork_mpl.save_and_show
.. autofunction:: dartwork_mpl.show
