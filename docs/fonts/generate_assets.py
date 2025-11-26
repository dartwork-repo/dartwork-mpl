"""
Generate high-resolution gallery assets for the fonts documentation.

The entrypoint `build_font_assets()` can be invoked from Sphinx (see docs/conf.py)
so that the gallery stays in sync with every build. You can also run this file
directly:

    python docs/fonts/generate_assets.py
"""

from __future__ import annotations

import math
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Make sure the source tree is importable when running the script directly.
ROOT = Path(__file__).resolve().parents[2]  # docs/fonts -> docs -> project root
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import dartwork_mpl as dm

# Font family metadata
FONT_FAMILIES = {
    "Inter": {
        "description": "Modern, highly legible sans-serif designed for computer screens",
        "use_case": "UI text, presentations, general purpose",
        "variants": 20,
    },
    "InterDisplay": {
        "description": "Display variant of Inter optimized for larger sizes",
        "use_case": "Headings, titles, large text",
        "variants": 20,
    },
    "NotoSans": {
        "description": "Google's versatile sans-serif with excellent language coverage",
        "use_case": "Multi-language documents, body text",
        "variants": 15,
    },
    "NotoSans_Condensed": {
        "description": "Condensed variant of Noto Sans for space-constrained layouts",
        "use_case": "Tables, dense layouts, annotations",
        "variants": 20,
    },
    "NotoSans_SemiCondensed": {
        "description": "Semi-condensed variant balancing readability and compactness",
        "use_case": "Labels, legends, compact text",
        "variants": 20,
    },
    "NotoSans_ExtraCondensed": {
        "description": "Extra condensed for maximum space efficiency",
        "use_case": "Very tight layouts, axis labels",
        "variants": 20,
    },
    "NotoSansMath": {
        "description": "Mathematical symbols and equations font",
        "use_case": "Scientific notation, mathematical expressions",
        "variants": 1,
    },
    "Paperlogy": {
        "description": "Clean, professional font designed for documents",
        "use_case": "Reports, academic papers, professional documents",
        "variants": 9,
    },
    "Roboto": {
        "description": "Google's flagship sans-serif, default font in dartwork-mpl",
        "use_case": "Default body text, general purpose (dartwork-mpl default)",
        "variants": 15,
    },
}

WEIGHT_ORDER = {
    "Thin": 1,
    "ExtraLight": 2,
    "Light": 3,
    "Regular": 4,
    "Medium": 5,
    "SemiBold": 6,
    "Bold": 7,
    "ExtraBold": 8,
    "Black": 9,
}


def _prepare_images_dir(base_dir: Path | None = None) -> Path:
    base = Path(base_dir) if base_dir else Path(__file__).parent
    images_dir = base / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    return images_dir


def _get_font_dir() -> Path:
    return ROOT / "src" / "dartwork_mpl" / "asset" / "font"


def _collect_fonts() -> Dict[str, List[str]]:
    """Collect and group font files by family."""
    font_dir = _get_font_dir()
    font_files = [f for f in os.listdir(font_dir) if f.endswith(".ttf")]

    font_families = defaultdict(list)
    for font in font_files:
        family = font.split("-")[0]
        font_families[family].append(font)

    return dict(sorted(font_families.items()))


def _sort_fonts(fonts: List[str]) -> List[str]:
    """Sort fonts by weight and style."""
    def get_weight_score(font):
        base_weight = 4  # Regular default
        italic_score = 0.5 if "Italic" in font else 0

        for weight, score in WEIGHT_ORDER.items():
            if weight in font:
                base_weight = score
                break

        return (base_weight, italic_score)

    return sorted(fonts, key=get_weight_score)


def _save_all_fonts_preview(images_dir: Path) -> Path:
    """Generate a comprehensive preview of all font families."""
    font_families = _collect_fonts()
    font_dir = _get_font_dir()

    # Calculate layout
    ncols = 3
    total_families = len(font_families)
    families_per_column = math.ceil(total_families / ncols)
    max_fonts_in_family = max(len(fonts) for fonts in font_families.values())

    family_spacing = 3
    total_height = families_per_column * (max_fonts_in_family + family_spacing)

    fig, ax = plt.subplots(figsize=(16, total_height * 0.32))
    fig.patch.set_facecolor("#fbfaf7")
    ax.set_facecolor("#ffffff")

    ax.set_xlim(0, ncols * 7)
    ax.set_ylim(0, total_height)
    ax.axis("off")

    fig.suptitle(
        "All Available Font Families",
        fontsize=20,
        fontweight="bold",
        y=0.98,
    )

    sorted_families = list(font_families.items())

    for family_idx, (family, fonts) in enumerate(sorted_families):
        column = family_idx // families_per_column
        family_row = family_idx % families_per_column

        x_pos = column * 7
        base_y_pos = family_row * (max_fonts_in_family + family_spacing)

        title_y = base_y_pos + max_fonts_in_family + 0.5
        ax.text(x_pos, title_y, f"{family}", size=13, weight="bold", color="#333")
        ax.plot(
            [x_pos, x_pos + 5.5],
            [title_y - 0.3, title_y - 0.3],
            color="#e4e2dd",
            linestyle="-",
            linewidth=1,
        )

        sorted_fonts = _sort_fonts(fonts)
        for font_idx, font_file in enumerate(sorted_fonts):
            font_path = font_dir / font_file
            font_name = os.path.splitext(font_file)[0]

            font_prop = fm.FontProperties(fname=str(font_path))
            y_pos = base_y_pos + (max_fonts_in_family - font_idx - 1)

            # Extract variant name
            variant = font_name.split("-")[1] if "-" in font_name else "Regular"
            ax.text(
                x_pos,
                y_pos,
                f"{variant}",
                fontproperties=font_prop,
                size=11,
                color="#444",
            )

    path = images_dir / "fonts_all_families.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_family_preview(family: str, fonts: List[str], images_dir: Path) -> Path:
    """Generate a detailed preview for a single font family."""
    font_dir = _get_font_dir()
    sorted_fonts = _sort_fonts(fonts)

    # Calculate figure size based on number of fonts
    n_fonts = len(sorted_fonts)
    fig_height = max(4, n_fonts * 0.5 + 2)

    fig, ax = plt.subplots(figsize=(12, fig_height))
    fig.patch.set_facecolor("#fbfaf7")
    ax.set_facecolor("#ffffff")

    ax.set_xlim(0, 10)
    ax.set_ylim(0, n_fonts + 1)
    ax.axis("off")

    # Title
    meta = FONT_FAMILIES.get(family, {})
    fig.suptitle(
        f"{family}",
        fontsize=18,
        fontweight="bold",
        y=0.96,
    )

    if meta.get("description"):
        fig.text(
            0.5,
            0.92,
            meta["description"],
            fontsize=11,
            color="#555",
            ha="center",
        )

    # Sample text
    sample_text = "The quick brown fox jumps over the lazy dog. 0123456789"

    for idx, font_file in enumerate(sorted_fonts):
        font_path = font_dir / font_file
        font_name = os.path.splitext(font_file)[0]
        variant = font_name.split("-")[1] if "-" in font_name else "Regular"

        font_prop = fm.FontProperties(fname=str(font_path))
        y_pos = n_fonts - idx - 0.5

        # Variant label
        ax.text(
            0.1,
            y_pos,
            f"{variant}",
            size=10,
            weight="bold",
            color="#666",
            va="center",
        )

        # Sample text
        ax.text(
            2.2,
            y_pos,
            sample_text,
            fontproperties=font_prop,
            size=12,
            color="#333",
            va="center",
        )

    path = images_dir / f"font_{family.lower()}.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_weight_comparison(images_dir: Path) -> Path:
    """Generate a weight comparison chart using Roboto."""
    font_dir = _get_font_dir()

    weights = ["Thin", "Light", "Regular", "Medium", "Bold", "Black"]

    fig, ax = plt.subplots(figsize=(14, 5))
    fig.patch.set_facecolor("#fbfaf7")
    ax.set_facecolor("#ffffff")

    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(weights) + 1)
    ax.axis("off")

    fig.suptitle(
        "Font Weight Comparison (Roboto)",
        fontsize=18,
        fontweight="bold",
        y=0.95,
    )
    fig.text(
        0.5,
        0.88,
        "Use fw(n) to adjust weight relative to base: fw(0)=base, fw(1)=+100, fw(-1)=-100",
        fontsize=11,
        color="#555",
        ha="center",
    )

    for idx, weight in enumerate(weights):
        font_file = f"Roboto-{weight}.ttf"
        font_path = font_dir / font_file

        if font_path.exists():
            font_prop = fm.FontProperties(fname=str(font_path))
            y_pos = len(weights) - idx - 0.5

            ax.text(
                0.2,
                y_pos,
                weight,
                size=11,
                weight="bold",
                color="#666",
                va="center",
            )

            ax.text(
                2.0,
                y_pos,
                "Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk",
                fontproperties=font_prop,
                size=16,
                color="#333",
                va="center",
            )

    path = images_dir / "font_weights.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_utilities_demo(images_dir: Path) -> Path:
    """Generate a demo of font utility functions."""
    dm.use_style("dmpl")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor("#fbfaf7")
    fig.suptitle(
        "Font Utility Functions",
        fontsize=18,
        fontweight="bold",
        y=0.98,
    )

    # fs() demo
    ax1 = axes[0]
    ax1.set_facecolor("#ffffff")
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 6)
    ax1.axis("off")
    ax1.set_title("fs(n) - Font Size Adjustment", fontsize=14, fontweight="bold", pad=10)

    base_size = plt.rcParams["font.size"]
    sizes = [("fs(-2)", dm.fs(-2)), ("fs(0)", dm.fs(0)), ("fs(2)", dm.fs(2)), ("fs(4)", dm.fs(4))]

    for idx, (label, size) in enumerate(sizes):
        y_pos = 5 - idx * 1.2
        ax1.text(0.5, y_pos, label, size=10, color="#666", va="center")
        ax1.text(2.5, y_pos, f"Sample Text (size={size:.1f})", size=size, color="#333", va="center")

    # fw() demo
    ax2 = axes[1]
    ax2.set_facecolor("#ffffff")
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 6)
    ax2.axis("off")
    ax2.set_title("fw(n) - Font Weight Adjustment", fontsize=14, fontweight="bold", pad=10)

    weights = [("fw(-1)", 200), ("fw(0)", 300), ("fw(1)", 400), ("fw(2)", 500), ("fw(4)", 700)]

    for idx, (label, weight) in enumerate(weights):
        y_pos = 5.5 - idx * 1.1
        ax2.text(0.5, y_pos, label, size=10, color="#666", va="center")
        ax2.text(2.5, y_pos, f"Sample Text (weight={weight})", size=12, weight=weight, color="#333", va="center")

    plt.tight_layout()
    path = images_dir / "font_utilities.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


def build_font_assets(base_dir: Path | None = None) -> Dict[str, List[Path]]:
    """Generate all font gallery assets and return their paths."""
    images_dir = _prepare_images_dir(base_dir)
    print(f"[fonts] generating assets to {images_dir}")

    # Generate all fonts preview
    all_fonts_path = _save_all_fonts_preview(images_dir)

    # Generate individual family previews
    font_families = _collect_fonts()
    family_paths = []
    for family, fonts in font_families.items():
        path = _save_family_preview(family, fonts, images_dir)
        family_paths.append(path)

    # Generate weight comparison
    weight_path = _save_weight_comparison(images_dir)

    # Generate utilities demo
    utils_path = _save_utilities_demo(images_dir)

    print(f"[fonts] wrote {len(family_paths) + 3} font preview images")

    return {
        "all_fonts": [all_fonts_path],
        "families": family_paths,
        "weights": [weight_path],
        "utilities": [utils_path],
    }


if __name__ == "__main__":
    build_font_assets()
