Font Utilities
==============

Custom fonts bundled in ``asset/font`` are registered with matplotlib on import,
so they are available without manual configuration. ``fs`` and ``fw`` are small
helpers for offsetting the global rcParams font size/weight, and the gallery
utility ``plot_fonts`` previews every installed family.

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
