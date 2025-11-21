Style Management
================

Helpers for discovering and applying the packaged matplotlib styles. The
`Style` manager reads `asset/mplstyle` and preset combinations (scientific,
investment, presentation, and Korean variants) from `presets.json`, resets
`rcParams`, and stacks multiple style files when needed.

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
