Layout Utilities
================

Utilities for tightening layouts without juggling ``plt.subplots_adjust``.
``simple_layout`` optimizes margins with L-BFGS-B so axes fit inside a bounding
box; ``make_offset`` nudges text/legends in point units; and
``set_decimal``/``get_bounding_box`` provide quick helpers when formatting axes.

``simple_layout(fig, gs=None, margins=(0.05, 0.05, 0.05, 0.05), bbox=(0, 1, 0, 1), verbose=False, gtol=1e-2, bound_margin=0.2, use_all_axes=True, importance_weights=(1, 1, 1, 1))``
   - Parameters:
     - ``fig``: target figure (required).
     - ``gs``: GridSpec to adjust; ``None`` picks the first axes' GridSpec.
     - ``margins``: padding in inches ``(left, right, bottom, top)``.
     - ``bbox``: figure-relative target box; shrink to reserve space for headers.
     - ``importance_weights``: emphasize specific sides during optimization.
     - ``bound_margin``: how far each side may move away from ``bbox``.
     - ``gtol``: optimizer tolerance.
     - ``verbose``: toggle optimizer logging.
     - ``use_all_axes``: ``True`` considers every axes; ``False`` limits to ``gs``.
   - Returns:
     - ``scipy.optimize.OptimizeResult``; layout changes are applied in-place.

``make_offset(x, y, fig)``
   - Parameters:
     - ``x``: horizontal offset in points.
     - ``y``: vertical offset in points.
     - ``fig``: figure providing DPI scaling.
   - Returns:
     - ``matplotlib.transforms.ScaledTranslation`` to add to an axes transform.

``set_decimal(ax, xn=None, yn=None)``
   - Parameters:
     - ``ax``: axes object to update.
     - ``xn``: decimal places for x ticks; ``None`` leaves them unchanged.
     - ``yn``: decimal places for y ticks; ``None`` leaves them unchanged.
   - Returns:
     - ``None``; tick labels are replaced.

``get_bounding_box(boxes)``
   - Parameters:
     - ``boxes``: iterable with ``p0``, ``width``, ``height`` (e.g., from ``get_tightbbox``).
   - Returns:
     - tuple ``(min_x, min_y, width, height)`` covering them all.

Example

.. code-block:: python

   fig, ax = plt.subplots()
   ax.plot(x, y)

   # Keep slightly wider right margin for a legend slot
   simple_layout(
       fig,
       margins=(0.08, 0.12, 0.1, 0.08),
       importance_weights=(1, 2, 1, 1)
   )

   # Pixel-perfect title nudge
   ax.set_title("Clean title", transform=ax.transAxes + make_offset(0, 6, fig))
   set_decimal(ax, xn=2, yn=1)

.. autofunction:: dartwork_mpl.simple_layout
.. autofunction:: dartwork_mpl.make_offset
.. autofunction:: dartwork_mpl.util.get_bounding_box
.. autofunction:: dartwork_mpl.util.set_decimal
