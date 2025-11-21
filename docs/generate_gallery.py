"""
Generate high-resolution gallery assets for the color system docs.

The entrypoint `build_gallery_assets()` is invoked from Sphinx (see docs/conf.py)
so that the gallery stays in sync with every build. You can also run this file
directly:

    python docs/generate_gallery.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, Iterable, List

import matplotlib

matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Make sure the source tree is importable when running the script directly.
ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import dartwork_mpl as dm

# Sane defaults for how we display things.
CATEGORY_ORDER = [
    "Sequential Single-Hue",
    "Sequential Multi-Hue",
    "Diverging",
    "Cyclical",
    "Categorical",
]

CATEGORY_BLURBS: Dict[str, str] = {
    "Sequential Single-Hue": "One hue that ramps value cleanly. Great for magnitude and density.",
    "Sequential Multi-Hue": "Colorful ramps that stay perceptually smooth. Ideal for heatmaps.",
    "Diverging": "Two anchored hues split around a midpoint. Perfect for anomalies or signed values.",
    "Cyclical": "Start equals end. Use for angles, phases, or anything periodic.",
    "Categorical": "Distinct steps with little interpolation. Use for discrete classes.",
}

COLOR_LIBRARY_ORDER = ["opencolor", "tw", "md", "ant", "chakra", "primer", "other"]
COLOR_LIBRARY_LABELS = {
    "opencolor": "OpenColor",
    "tw": "Tailwind",
    "md": "Material Design",
    "ant": "Ant Design",
    "chakra": "Chakra UI",
    "primer": "Primer",
    "other": "Other & Matplotlib",
}


def _prepare_images_dir(base_dir: Path | None = None) -> Path:
    base = Path(base_dir) if base_dir else Path(__file__).parent
    images_dir = base / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    return images_dir


def _collect_colormaps() -> Dict[str, List[mpl.colors.Colormap]]:
    """Bucket colormaps by category."""
    cmap_list: Iterable[str] = (
        name for name in mpl.colormaps if not str(name).endswith("_r")
    )
    cmaps = [mpl.colormaps[name] for name in cmap_list]

    categories: Dict[str, List[mpl.colors.Colormap]] = {
        category: [] for category in CATEGORY_ORDER
    }
    for cmap in cmaps:
        category = dm.classify_colormap(cmap)
        if category in categories:
            categories[category].append(cmap)

    for values in categories.values():
        values.sort(key=lambda cmap: (0 if cmap.name.startswith("dm.") else 1, cmap.name))

    return {k: v for k, v in categories.items() if v}


def _gradient(resolution: int = 720, height: int = 28) -> np.ndarray:
    grad = np.linspace(0, 1, resolution)
    return np.repeat(grad[np.newaxis, :], height, axis=0)


def _save_colormap_category(
    category: str, cmaps: List[mpl.colors.Colormap], images_dir: Path
) -> Path:
    """Draw a wide, high-DPI panel for a single category."""
    ncols = 2
    nrows = math.ceil(len(cmaps) / ncols)
    fig_width = 14
    fig_height = 1.4 + nrows * 1.45

    fig, axes = plt.subplots(nrows, ncols, figsize=(fig_width, fig_height))
    fig.patch.set_facecolor("#fbfaf7")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.9, bottom=0.05, hspace=0.38, wspace=0.22)
    fig.suptitle(
        f"{category}",
        fontsize=18,
        fontweight="bold",
        x=0.07,
        ha="left",
        va="center",
    )
    fig.text(
        0.07,
        0.93,
        CATEGORY_BLURBS.get(category, ""),
        fontsize=11,
        color="#555",
        ha="left",
    )

    gradient = _gradient()
    axes_flat = axes.ravel() if hasattr(axes, "ravel") else [axes]
    for idx, ax in enumerate(axes_flat):
        if idx >= len(cmaps):
            ax.axis("off")
            continue

        cmap = cmaps[idx]
        ax.set_facecolor("#ffffff")
        ax.imshow(gradient, aspect="auto", cmap=cmap)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)

        tag = "dartwork" if cmap.name.startswith("dm.") else None
        ax.text(
            0,
            1.15,
            cmap.name,
            fontsize=11.5,
            fontweight="bold",
            ha="left",
            va="bottom",
            transform=ax.transAxes,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="#ffffff",
                edgecolor="#e4e2dd",
                linewidth=0.8,
            ),
        )
        if tag:
            ax.text(
                1.0,
                1.15,
                tag,
                fontsize=9,
                ha="right",
                va="bottom",
                transform=ax.transAxes,
                color="#03675f",
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    facecolor="#e1f4f1",
                    edgecolor="#b9e2dc",
                    linewidth=0.8,
                ),
            )

    filename = f"colormaps_{category.lower().replace(' ', '_')}.png"
    path = images_dir / filename
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_colormap_panels(images_dir: Path) -> List[Path]:
    categories = _collect_colormaps()
    output: List[Path] = []

    for category in CATEGORY_ORDER:
        colormaps = categories.get(category)
        if not colormaps:
            continue
        output.append(_save_colormap_category(category, colormaps, images_dir))
    return output


def _scale_figure(fig: plt.Figure, scale: float) -> None:
    width, height = fig.get_size_inches()
    fig.set_size_inches(width * scale, height * scale)


def _save_color_sheets(images_dir: Path) -> List[Path]:
    figs = dm.plot_colors(ncols=7, sort_colors=True)
    paths: List[Path] = []

    for fig, library_name in zip(figs, COLOR_LIBRARY_ORDER):
        _scale_figure(fig, 1.08)
        fig.patch.set_facecolor("#fbfaf7")
        for ax in fig.get_axes():
            ax.set_facecolor("#ffffff")
        path = images_dir / f"colors_{library_name}.png"
        fig.savefig(path, dpi=220, bbox_inches="tight")
        plt.close(fig)
        paths.append(path)

    return paths


def build_gallery_assets(base_dir: Path | None = None) -> Dict[str, List[Path]]:
    """Generate all gallery assets and return their paths."""
    images_dir = _prepare_images_dir(base_dir)
    print(f"[gallery] generating assets to {images_dir}")
    colormap_paths = _save_colormap_panels(images_dir)
    color_paths = _save_color_sheets(images_dir)
    print(f"[gallery] wrote {len(color_paths)} color sheets and {len(colormap_paths)} colormap panels")
    return {"colors": color_paths, "colormaps": colormap_paths}


if __name__ == "__main__":
    build_gallery_assets()
