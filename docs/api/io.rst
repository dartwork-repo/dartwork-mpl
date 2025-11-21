File I/O
========

Thin wrappers around ``matplotlib.Figure.savefig`` for common workflows:
export multiple formats in one call, or save-and-display SVGs sized for
notebooks/reports.

Example

.. code-block:: python

   fig, ax = plt.subplots()
   ax.plot(x, y)
   dm.save_formats(fig, \"report/figures/example\", formats=(\"png\", \"svg\"), dpi=300)
   dm.save_and_show(fig, \"report/figures/example.svg\", size=520)

.. autofunction:: dartwork_mpl.save_formats
.. autofunction:: dartwork_mpl.save_and_show
.. autofunction:: dartwork_mpl.show
