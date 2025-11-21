Style Management
================

Helpers for discovering and applying the packaged matplotlib styles. The
`Style` manager reads `asset/mplstyle` and preset combinations (scientific,
investment, presentation, and Korean variants) from `presets.json`, resets
`rcParams`, and stacks multiple style files when needed. Use the helpers below
to pick a single style, layer several, or inspect what a preset changes before
you commit it to a figure.

Quick reference

.. list-table:: ``use_style`` arguments
   :header-rows: 1
   :widths: 22 60

   * - Parameter
     - Purpose
   * - ``name`` (default ``"dmpl"``)
     - Style file stem in ``asset/mplstyle``. Resets ``rcParams`` first, so pass
       a single name if you want a clean slate or stack multiple via
       ``Style.use``.

.. list-table:: ``Style.use_preset`` arguments
   :header-rows: 1
   :widths: 22 60

   * - Parameter
     - Purpose
   * - ``preset_name``
     - Key from ``presets.json`` such as ``"scientific"``, ``"investment"``,
       ``"presentation"``, or ``"korean.*"``. Each preset expands to an ordered
       list of style files applied in sequence.

.. list-table:: ``load_style_dict`` arguments
   :header-rows: 1
   :widths: 22 60

   * - Parameter
     - Purpose
   * - ``name``
     - Style file stem to inspect. Returns a ``dict`` of rcParams for quick
       diffing or programmatic tweaks.

Typical usage

.. code-block:: python

   import dartwork_mpl as dm

   # Single style or bundled presets
   dm.use_style("dmpl_light")
   dm.style.use_preset("scientific")

   # Inspect what a style will set
   available = dm.list_styles()
   style_dict = dm.load_style_dict("font-presentation")

.. automodule:: dartwork_mpl.style
   :members:
   :undoc-members:
   :show-inheritance:
