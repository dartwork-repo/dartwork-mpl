Style Management
================

Helpers for discovering and applying the packaged matplotlib styles. The
`Style` manager reads `asset/mplstyle` and preset combinations (scientific,
investment, presentation, and Korean variants) from `presets.json`, resets
`rcParams`, and stacks multiple style files when needed. Use the helpers below
to pick a single style, layer several, or inspect what a preset changes before
you commit it to a figure.

``use_style(name="dmpl")``
Loads one style file from ``asset/mplstyle`` after resetting ``rcParams``.

- Parameters:
  - ``name``: style stem (e.g., ``"dmpl_light"``, ``"font-presentation"``).
- Returns:
  - ``None``; updates matplotlib state.

``Style.use(style_names)``
Stack multiple style files in order.

- Parameters:
  - ``style_names``: list/tuple of style stems; later styles override earlier ones.
- Returns:
  - ``None``.

``Style.use_preset(preset_name)``
Applies a preset key from ``presets.json`` (e.g., ``"scientific"``,
``"investment"``, ``"presentation"``, ``"korean.presentation"``).

- Parameters:
  - ``preset_name``: string looked up in the presets mapping.
- Returns:
  - ``None``.

``list_styles()``
Lists every ``*.mplstyle`` file bundled with the package.

- Parameters:
  - none.
- Returns:
  - ``list[str]`` sorted by filename.

``load_style_dict(name)``
Reads a single style file into a ``dict`` so you can inspect or tweak rcParams
programmatically.

- Parameters:
  - ``name``: style stem.
- Returns:
  - ``dict`` mapping rcParam keys to values.

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
