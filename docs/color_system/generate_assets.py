"""
Generate high-resolution gallery assets for the color system docs.

The entrypoint `build_gallery_assets()` is invoked from Sphinx (see docs/conf.py)
so that the gallery stays in sync with every build. You can also run this file
directly:

    python docs/color_system/generate_assets.py
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
ROOT = Path(__file__).resolve().parents[2]  # docs/color -> docs -> project root
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
        values.sort(
            key=lambda cmap: (0 if cmap.name.startswith("dm.") else 1, cmap.name)
        )

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
    fig.subplots_adjust(
        left=0.06, right=0.97, top=0.9, bottom=0.05, hspace=0.38, wspace=0.22
    )
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
    figs = dm.plot_colors(ncols=4, sort_colors=True)
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


def _save_color_space_creation(images_dir: Path) -> Path:
    """Generate example showing different ways to create Color objects."""
    dm.style.use("scientific")

    fig, axes = plt.subplots(2, 3, figsize=(dm.cm2in(14), dm.cm2in(6)), dpi=300)
    fig.patch.set_facecolor("#fbfaf7")
    fig.subplots_adjust(
        left=0.05, right=0.98, top=0.88, bottom=0.12, hspace=0.4, wspace=0.25
    )
    fig.suptitle("Creating Color Objects", fontsize=16, fontweight="bold", y=0.95)

    # Examples
    examples = [
        ("OKLab", dm.oklab(0.7, 0.1, 0.2), "dm.oklab(0.7, 0.1, 0.2)"),
        ("OKLCH", dm.oklch(0.7, 0.2, 120), "dm.oklch(0.7, 0.2, 120)"),
        ("RGB", dm.rgb(0.8, 0.2, 0.3), "dm.rgb(0.8, 0.2, 0.3)"),
        ("Hex", dm.hex("#ff5733"), "dm.hex('#ff5733')"),
        ("Named", dm.named("oc.blue5"), "dm.named('oc.blue5')"),
        ("RGB 255", dm.rgb(200, 50, 75), "dm.rgb(200, 50, 75)"),
    ]

    axes_flat = axes.ravel()
    for idx, (label, color, code) in enumerate(examples):
        ax = axes_flat[idx]
        ax.set_facecolor("#ffffff")
        rgb_val = color.to_rgb()
        ax.add_patch(
            plt.Rectangle(
                (0, 0), 1, 1, facecolor=rgb_val, edgecolor="#e4e2dd", linewidth=1.5
            )
        )
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(
            0.5,
            -0.15,
            label,
            ha="center",
            va="top",
            transform=ax.transAxes,
            fontsize=10,
            fontweight="bold",
        )
        ax.text(
            0.5,
            -0.3,
            code,
            ha="center",
            va="top",
            transform=ax.transAxes,
            fontsize=8,
            family="monospace",
            color="#555",
        )

    dm.simple_layout(fig, use_all_axes=True)
    path = images_dir / "color_space_creation.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_color_space_conversion(images_dir: Path) -> Path:
    """Generate example showing color space conversions."""
    dm.style.use("scientific")

    fig = plt.figure(figsize=(dm.cm2in(14), dm.cm2in(5)), dpi=300)
    fig.patch.set_facecolor("#fbfaf7")
    gs = fig.add_gridspec(
        1, 5, left=0.05, right=0.98, top=0.85, bottom=0.15, wspace=0.15
    )
    fig.suptitle("Color Space Conversion", fontsize=16, fontweight="bold", y=0.92)

    # Start with one color
    color = dm.hex("#ff5733")

    # Convert to different spaces
    L, a, b = color.to_oklab()
    L_ch, C, h = color.to_oklch()
    r, g, b_rgb = color.to_rgb()
    hex_str = color.to_hex()

    conversions = [
        ("Original\n(Hex)", hex_str, f"'{hex_str}'"),
        ("OKLab", f"L={L:.3f}\na={a:.3f}\nb={b:.3f}", f"({L:.3f}, {a:.3f}, {b:.3f})"),
        (
            "OKLCH",
            f"L={L_ch:.3f}\nC={C:.3f}\nh={h:.1f}°",
            f"({L_ch:.3f}, {C:.3f}, {h:.1f}°)",
        ),
        (
            "RGB",
            f"r={r:.3f}\ng={g:.3f}\nb={b_rgb:.3f}",
            f"({r:.3f}, {g:.3f}, {b_rgb:.3f})",
        ),
        ("Hex", hex_str, f"'{hex_str}'"),
    ]

    for idx, (label, values, code) in enumerate(conversions):
        ax = fig.add_subplot(gs[0, idx])
        ax.set_facecolor("#ffffff")
        rgb_val = color.to_rgb()
        ax.add_patch(
            plt.Rectangle(
                (0, 0.3), 1, 0.4, facecolor=rgb_val, edgecolor="#e4e2dd", linewidth=1.5
            )
        )
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(
            0.5,
            0.85,
            label,
            ha="center",
            va="bottom",
            transform=ax.transAxes,
            fontsize=11,
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.1,
            values,
            ha="center",
            va="top",
            transform=ax.transAxes,
            fontsize=9,
            family="monospace",
        )
        ax.text(
            0.5,
            -0.05,
            code,
            ha="center",
            va="top",
            transform=ax.transAxes,
            fontsize=7,
            family="monospace",
            color="#555",
        )

    dm.simple_layout(fig, gs=gs, use_all_axes=True)
    path = images_dir / "color_space_conversion.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_color_space_interpolation(images_dir: Path) -> Path:
    """Generate example comparing interpolation in different color spaces."""
    dm.style.use("scientific")

    fig, axes = plt.subplots(3, 1, figsize=(dm.cm2in(14), dm.cm2in(6)), dpi=300)
    fig.patch.set_facecolor("#fbfaf7")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.12, hspace=0.35)
    fig.suptitle(
        "Color Interpolation Comparison", fontsize=16, fontweight="bold", y=0.94
    )

    start_color = dm.hex("#1a237e")
    end_color = dm.hex("#ff6f00")
    n = 20

    spaces = [
        ("OKLCH (perceptually uniform)", "oklch"),
        ("OKLab (perceptually uniform)", "oklab"),
        ("RGB", "rgb"),
    ]

    for ax, (label, space) in zip(axes, spaces):
        colors = dm.cspace(start_color, end_color, n=n, space=space)
        gradient = np.array([c.to_rgb() for c in colors])
        gradient = gradient[np.newaxis, :, :]

        ax.set_facecolor("#ffffff")
        ax.imshow(gradient, aspect="auto", extent=[0, 1, 0, 1])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        ax.text(
            -0.02,
            0.5,
            label,
            ha="right",
            va="center",
            transform=ax.transAxes,
            fontsize=11,
            fontweight="bold",
        )
        ax.text(
            0.5,
            -0.15,
            f"space='{space}'",
            ha="center",
            va="top",
            transform=ax.transAxes,
            fontsize=9,
            family="monospace",
            color="#555",
        )

    dm.simple_layout(fig, use_all_axes=True)
    path = images_dir / "color_space_interpolation.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_color_space_colormap(images_dir: Path) -> Path:
    """Generate example showing custom colormap creation."""
    dm.style.use("scientific")

    fig = plt.figure(figsize=(dm.cm2in(14), dm.cm2in(7)), dpi=300)
    fig.patch.set_facecolor("#fbfaf7")
    gs = fig.add_gridspec(
        2, 2, left=0.08, right=0.98, top=0.92, bottom=0.1, hspace=0.35, wspace=0.25
    )
    fig.suptitle(
        "Custom Colormaps with cspace()", fontsize=16, fontweight="bold", y=0.96
    )

    # Sequential colormap
    colors_seq = dm.cspace("#1a237e", "#ff6f00", n=256, space="oklch")
    cmap_seq = mpl.colors.ListedColormap([c.to_rgb() for c in colors_seq])

    # Diverging colormap
    colors1 = dm.cspace("#1a237e", "#ffffff", n=128, space="oklch")
    colors2 = dm.cspace("#ffffff", "#c62828", n=128, space="oklch")
    colors_div = colors1[:-1] + colors2
    cmap_div = mpl.colors.ListedColormap([c.to_rgb() for c in colors_div])

    # Generate sample data
    data = np.random.randn(100, 100)

    # Sequential example
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor("#ffffff")
    im1 = ax1.imshow(data, cmap=cmap_seq, aspect="auto")
    ax1.set_title("Sequential Colormap", fontsize=12, fontweight="bold", pad=10)
    ax1.set_xticks([])
    ax1.set_yticks([])
    plt.colorbar(im1, ax=ax1, label="Value", fraction=0.046, pad=0.04)

    # Diverging example
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor("#ffffff")
    im2 = ax2.imshow(data, cmap=cmap_div, aspect="auto", vmin=-3, vmax=3)
    ax2.set_title("Diverging Colormap", fontsize=12, fontweight="bold", pad=10)
    ax2.set_xticks([])
    ax2.set_yticks([])
    plt.colorbar(im2, ax=ax2, label="Value", fraction=0.046, pad=0.04)

    # Code examples
    code1 = """# Sequential
colors = dm.cspace(
    "#1a237e", "#ff6f00",
    n=256, space="oklch"
)
cmap = mpl.colors.ListedColormap(
    [c.to_rgb() for c in colors]
)"""

    code2 = """# Diverging
colors1 = dm.cspace(
    "#1a237e", "#ffffff",
    n=128, space="oklch"
)
colors2 = dm.cspace(
    "#ffffff", "#c62828",
    n=128, space="oklch"
)
colors = colors1[:-1] + colors2
cmap = mpl.colors.ListedColormap(
    [c.to_rgb() for c in colors]
)"""

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor("#ffffff")
    ax3.text(
        0.05,
        0.95,
        code1,
        transform=ax3.transAxes,
        fontsize=8,
        family="monospace",
        va="top",
        ha="left",
        bbox=dict(boxstyle="round", facecolor="#f8f8f8", edgecolor="#e4e2dd"),
    )
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_frame_on(False)

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor("#ffffff")
    ax4.text(
        0.05,
        0.95,
        code2,
        transform=ax4.transAxes,
        fontsize=8,
        family="monospace",
        va="top",
        ha="left",
        bbox=dict(boxstyle="round", facecolor="#f8f8f8", edgecolor="#e4e2dd"),
    )
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.set_xticks([])
    ax4.set_yticks([])
    ax4.set_frame_on(False)

    dm.simple_layout(fig, gs=gs, use_all_axes=True)
    path = images_dir / "color_space_colormap.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_color_space_examples(images_dir: Path) -> List[Path]:
    """Generate all Color Space example images."""
    paths = [
        _save_color_space_creation(images_dir),
        _save_color_space_conversion(images_dir),
        _save_color_space_interpolation(images_dir),
        _save_color_space_colormap(images_dir),
    ]
    return paths


def build_gallery_assets(base_dir: Path | None = None) -> Dict[str, List[Path]]:
    """Generate all gallery assets and return their paths."""
    images_dir = _prepare_images_dir(base_dir)
    print(f"[gallery] generating assets to {images_dir}")
    colormap_paths = _save_colormap_panels(images_dir)
    color_paths = _save_color_sheets(images_dir)
    color_space_paths = _save_color_space_examples(images_dir)
    print(
        f"[gallery] wrote {len(color_paths)} color sheets, {len(colormap_paths)} colormap panels, and {len(color_space_paths)} color space examples"
    )
    return {
        "colors": color_paths,
        "colormaps": colormap_paths,
        "color_space": color_space_paths,
    }


if __name__ == "__main__":
    build_gallery_assets()
