File I/O
========

Thin wrappers around ``matplotlib.Figure.savefig`` for common workflows:
export multiple formats in one call, or save-and-display SVGs sized for
notebooks/reports. They accept the usual ``savefig`` keyword arguments; the
custom ones are called out below.

``save_formats(fig, image_stem, formats=("svg", "png", "pdf", "eps"), bbox_inches=None, **kwargs)``
   - Parameters: ``fig`` to export; ``image_stem`` path without extension
     (parent folders are created); iterable ``formats`` to write; optional
     ``bbox_inches`` forwarded to ``savefig``; extra ``**kwargs`` go straight to
     ``savefig``.
   - Returns: ``None`` after writing one file per requested format.

``save_and_show(fig, image_path=None, size=600, unit="pt", **kwargs)``
   - Parameters: ``fig`` to save (closed after saving); ``image_path`` file path
     or ``None`` to use a temporary SVG; ``size`` and ``unit`` for the inline
     display width; ``**kwargs`` forwarded to ``savefig``.
   - Returns: ``None``; displays the SVG inline (Jupyter/HTML).

``show(image_path, size=600, unit="pt")``
   - Parameters: ``image_path`` to an SVG; desired ``size`` and ``unit`` for the
     display width.
   - Returns: ``None``; shows the scaled SVG inline.

Example

.. code-block:: python

   fig, ax = plt.subplots()
   ax.plot(x, y)
   dm.save_formats(fig, "report/figures/example", formats=("png", "svg"), dpi=300)
   dm.save_and_show(fig, "report/figures/example.svg", size=520)

.. autofunction:: dartwork_mpl.save_formats
.. autofunction:: dartwork_mpl.save_and_show
.. autofunction:: dartwork_mpl.show
