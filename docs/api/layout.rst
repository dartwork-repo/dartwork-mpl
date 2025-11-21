Layout Utilities
================

Utilities for tightening layouts without juggling ``plt.subplots_adjust``.
``simple_layout`` optimizes margins with L-BFGS-B so axes fit inside a bounding
box; ``make_offset`` nudges text/legends in point units; and
``set_decimal``/``get_bounding_box`` provide quick helpers when formatting axes.

Example

.. code-block:: python

   fig, ax = plt.subplots()
   ax.plot(x, y)
   simple_layout(fig, margins=(0.08, 0.08, 0.1, 0.08))
   ax.set_title(\"Clean title\", transform=ax.transAxes + make_offset(0, 6, fig))

.. autofunction:: dartwork_mpl.simple_layout
.. autofunction:: dartwork_mpl.make_offset
.. autofunction:: dartwork_mpl.util.get_bounding_box
.. autofunction:: dartwork_mpl.util.set_decimal
