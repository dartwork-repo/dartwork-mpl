Layout Utilities
================

Utilities for tightening layouts without juggling ``plt.subplots_adjust``.
``simple_layout`` optimizes margins with L-BFGS-B so axes fit inside a bounding
box; ``make_offset`` nudges text/legends in point units; and
``set_decimal``/``get_bounding_box`` provide quick helpers when formatting axes.
Tables below call out the arguments you are most likely to tweak.

.. list-table:: ``simple_layout`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``fig`` (required)
     - Figure to optimize—usually from ``plt.subplots``.
   * - ``gs`` (optional)
     - GridSpec to solve for. Leave ``None`` to target the first axes' GridSpec;
       pass a specific one when the figure has multiple grids.
   * - ``margins`` (default ``(0.05, 0.05, 0.05, 0.05)``)
     - Desired padding in inches ordered ``(left, right, bottom, top)``. Increase
       values to loosen whitespace around axes.
   * - ``bbox`` (default ``(0, 1, 0, 1)``)
     - Fractional bounds of the area to fill in figure coordinates. Shrink from
       ``(0, 1, 0, 1)`` when you need fixed space for headers or legends.
   * - ``importance_weights`` (default ``(1, 1, 1, 1)``)
     - Relative importance of hitting each side of the target box (left, right,
       bottom, top). Increase a side to prioritize it during optimization.
   * - ``bound_margin`` (default ``0.2``)
     - How far the optimizer may move each side away from ``bbox``. Lower values
       lock the layout tighter; higher values allow more experimentation.
   * - ``gtol`` (default ``1e-2``) / ``verbose`` (default ``False``)
     - Convergence tolerance and logging toggle passed to the L-BFGS-B optimizer.

.. list-table:: ``make_offset`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``x``, ``y`` (points)
     - Offsets applied in typographic points. Positive values move right/up;
       negative values move left/down.
   * - ``fig``
     - Figure whose DPI is used when converting points to screen units.

.. list-table:: ``set_decimal`` and ``get_bounding_box`` arguments
   :header-rows: 1
   :widths: 23 60

   * - Parameter
     - Purpose
   * - ``ax`` / ``xn`` / ``yn``
     - Pass an axes and number of decimal places to format ticks without setting
       locators manually.
   * - ``boxes``
     - Sequence of tight bounding boxes; a combined ``(min_x, min_y, width, height)``
       tuple is returned for quick diagnostics.

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
