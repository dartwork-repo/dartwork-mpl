# AI-Assisted Graph Development

dartwork-mpl is designed to work seamlessly with AI coding assistants like Cursor, GitHub Copilot, and Claude Code. This guide explains best practices for efficiently creating publication-quality graphs with AI assistance.

## Overview

When working with AI assistants to create graphs, follow these three key principles:

1. **Use context prompts** to provide AI with dartwork-mpl guidelines
2. **Create plot functions** with configurable arguments instead of modifying code directly
3. **Work in an autoreload-enabled notebook** for rapid iteration

Following these practices will dramatically speed up your workflow and reduce errors.

## 1. Using Context Prompts

AI assistants need context about dartwork-mpl's conventions and best practices. dartwork-mpl provides several ways to make prompt guides available to your AI assistant.

### Available Prompt Guides

dartwork-mpl includes two comprehensive prompt guides:

- **`general-guide`**: Complete library usage guide covering styles, colors, layout utilities, and workflows
- **`layout-guide`**: Detailed guide for using `simple_layout` and handling complex layouts

### Method 1: Copy to Cursor Rules (Recommended for Cursor IDE)

The easiest way to provide context to Cursor IDE is to copy prompt guides to your `.cursor/rules/` directory:

```python
import dartwork_mpl as dm
from pathlib import Path

# Copy layout guide to Cursor rules
layout_path = dm.copy_prompt('layout-guide', '.cursor/rules/')

# Copy general guide to Cursor rules
general_path = dm.copy_prompt('general-guide', '.cursor/rules/')

# Note: Cursor rules use .mdc extension, but copy_prompt copies as .md
# Rename to .mdc if needed for Cursor IDE compatibility
if layout_path.suffix == '.md':
    layout_path.rename(layout_path.with_suffix('.mdc'))
if general_path.suffix == '.md':
    general_path.rename(general_path.with_suffix('.mdc'))
```

**Note**: The `copy_prompt()` function copies files with `.md` extension. If you're using Cursor IDE, you may want to rename them to `.mdc` extension for better compatibility. Alternatively, you can copy directly to `.mdc` files:

```python
import dartwork_mpl as dm

# Copy directly to .mdc files
dm.copy_prompt('layout-guide', '.cursor/rules/layout-guide.mdc')
dm.copy_prompt('general-guide', '.cursor/rules/general-guide.mdc')
```

After copying, Cursor will automatically have access to these guides when generating code. The AI will understand dartwork-mpl conventions and generate appropriate code.

### Method 2: Programmatic Access

You can also access prompt guides programmatically to include in your own prompts:

```python
import dartwork_mpl as dm

# Get prompt guide content as string
layout_guide = dm.get_prompt('layout-guide')
general_guide = dm.get_prompt('general-guide')

# List all available prompts
available_prompts = dm.list_prompts()
# ['general-guide', 'layout-guide']

# Get file path for custom processing
prompt_path = dm.prompt_path('layout-guide')
```

This is useful when:
- Building custom AI workflows
- Creating project-specific documentation
- Integrating with other AI tools

### Method 3: Direct File Access

Prompt guides are stored in the package assets and can be accessed directly:

```python
from pathlib import Path
import dartwork_mpl as dm

# Get the path to a prompt guide
prompt_path = dm.prompt_path('layout-guide')
print(prompt_path)
# /path/to/dartwork_mpl/asset/prompt/layout-guide.md

# Read directly
content = prompt_path.read_text(encoding='utf-8')
```

### Best Practice: Set Up Once

For Cursor IDE users, we recommend setting up prompt guides once at the start of your project:

```python
import dartwork_mpl as dm

# One-time setup: copy both guides to Cursor rules as .mdc files
dm.copy_prompt('layout-guide', '.cursor/rules/layout-guide.mdc')
dm.copy_prompt('general-guide', '.cursor/rules/general-guide.mdc')

print("✅ Prompt guides installed for Cursor IDE")
```

**Note**: Cursor IDE uses `.mdc` extension for rule files. The `copy_prompt()` function defaults to `.md` extension, so specify `.mdc` explicitly in the destination path (as shown above) for Cursor compatibility.

After this setup, Cursor will automatically use these guides when generating matplotlib code.

## 2. Create Plot Functions with Arguments

One of the most important principles for AI-assisted development is to **structure your code as functions with configurable arguments** rather than modifying code directly.

### Why Functions?

When you ask AI to "change the color slightly" or "make the line a bit thicker," the AI must:
1. Parse your vague description
2. Find the relevant code
3. Guess what "slightly" or "a bit" means
4. Modify the code
5. Risk breaking other parts

This process is slow and error-prone. Instead, use functions with clear arguments:

### ✅ Good: Function-Based Approach

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

def plot_signal(
    data: np.ndarray,
    color: str = 'oc.blue5',
    linewidth: float = 0.7,
    figsize: tuple[float, float] | None = None,
    dpi: int = 200
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a signal with configurable styling.
    
    Parameters
    ----
    data : np.ndarray
        Signal data to plot.
    color : str, optional
        Line color. Default is 'oc.blue5'.
    linewidth : float, optional
        Line width. Default is 0.7.
    figsize : tuple[float, float] | None, optional
        Figure size in inches. If None, uses (9cm, 7cm).
    dpi : int, optional
        Figure resolution. Default is 200.
    
    Returns
    ----
    fig : matplotlib.figure.Figure
        The created figure.
    ax : matplotlib.axes.Axes
        The axes containing the plot.
    """
    dm.style.use('scientific')
    
    if figsize is None:
        figsize = (dm.cm2in(9), dm.cm2in(7))
    
    fig = plt.figure(figsize=figsize, dpi=dpi)
    gs = fig.add_gridspec(
        nrows=1, ncols=1,
        left=0.17, right=0.95,
        top=0.95, bottom=0.17
    )
    ax = fig.add_subplot(gs[0, 0])
    
    x = np.arange(len(data))
    ax.plot(x, data, color=color, linewidth=linewidth)
    ax.set_xlabel('Time [s]', fontsize=dm.fs(0))
    ax.set_ylabel('Amplitude', fontsize=dm.fs(0))
    
    dm.simple_layout(fig)
    
    return fig, ax

# Usage: Easy to modify by changing arguments
data = np.random.randn(100).cumsum()
fig, ax = plot_signal(data, color='oc.red5', linewidth=1.2)
dm.save_and_show(fig)
```

**Benefits:**
- Clear, explicit changes: `color='oc.red5'` instead of "change color slightly"
- Fast iteration: just change arguments
- No code modification needed
- AI can easily understand and suggest changes

### ❌ Bad: Direct Code Modification

```python
# Don't do this!
fig = plt.figure(figsize=(dm.cm2in(9), dm.cm2in(7)), dpi=200)
ax = fig.add_subplot(111)
ax.plot(data, color='oc.blue5', linewidth=0.7)  # Hard to modify
# ... more code ...
```

When you ask AI to "make it a bit redder," it must:
- Find this specific line
- Guess what "a bit redder" means
- Modify the code
- Risk breaking something

### Function Design Best Practices

1. **Make all visual parameters configurable**:
   ```python
   def plot_comparison(
       data1: np.ndarray,
       data2: np.ndarray,
       color1: str = 'oc.red5',
       color2: str = 'oc.blue5',
       linewidth: float = 0.7,
       figsize: tuple[float, float] | None = None,
       title: str | None = None,
       # ... more parameters
   ):
       pass
   ```

2. **Provide sensible defaults**:
   ```python
   # Good defaults that work out of the box
   def plot_data(data, color='oc.blue5', linewidth=0.7):
       pass
   ```

3. **Use type hints**:
   ```python
   # Helps AI understand what values are acceptable
   def plot_data(
       data: np.ndarray,
       color: str = 'oc.blue5',
       linewidth: float = 0.7
   ) -> tuple[plt.Figure, plt.Axes]:
       pass
   ```

4. **Document parameters**:
   ```python
   """
   Parameters
   ----
   color : str, optional
       Line color. Use dartwork-mpl color names like 'oc.red5' or 'tw.blue500'.
       Default is 'oc.blue5'.
   """
   ```

### Working with AI: Argument-Based Changes

When you want to modify a plot, ask AI to change arguments, not code:

**✅ Good prompts:**
- "Change the line color to 'oc.red5'"
- "Increase linewidth to 1.2"
- "Set figsize to (12, 8)"
- "Add a title parameter and set it to 'My Plot'"

**❌ Bad prompts:**
- "Make the line a bit thicker"
- "Change the color slightly"
- "Adjust the figure size"
- "Make it look better"

Clear, argument-based requests are faster, more reliable, and less error-prone.

## 3. Rapid Iteration with Autoreload

The fastest way to develop plots with AI assistance is to work in a notebook environment with autoreload enabled. The key benefit of autoreload is that it **automatically updates changes from external Python files**, allowing you to modify functions in separate `.py` files and see results immediately in your notebook.

### Why Use External Python Files?

While you *can* define functions directly in notebook cells, it's better to define visualization functions in separate `.py` files outside the notebook:

**Problems with defining functions in notebook cells:**
- AI assistants sometimes struggle to modify code within cells
- Cell-based code is harder to version control effectively
- Mixing function definitions and testing code makes the notebook cluttered
- Difficult to reuse functions across multiple notebooks

**Benefits of external `.py` files:**
- AI assistants work more reliably with separate Python files
- Better version control: track function changes independently
- Cleaner notebooks: notebooks focus on testing and visualization
- Reusable: import the same functions in multiple notebooks
- Easier collaboration: team members can work on functions and notebooks separately

### Recommended Workflow: Separate Files

**1. Create a Python file for your visualization functions** (`plotting.py`):

```python
# plotting.py
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

def plot_signal(
    data: np.ndarray,
    color: str = 'oc.blue5',
    linewidth: float = 0.7,
    figsize: tuple[float, float] | None = None
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a signal with configurable styling.
    
    Parameters
    ----
    data : np.ndarray
        Signal data to plot.
    color : str, optional
        Line color. Default is 'oc.blue5'.
    linewidth : float, optional
        Line width. Default is 0.7.
    figsize : tuple[float, float] | None, optional
        Figure size in inches. If None, uses (9cm, 7cm).
    
    Returns
    ----
    fig : matplotlib.figure.Figure
        The created figure.
    ax : matplotlib.axes.Axes
        The axes containing the plot.
    """
    dm.style.use('scientific')
    
    if figsize is None:
        figsize = (dm.cm2in(9), dm.cm2in(7))
    
    fig = plt.figure(figsize=figsize, dpi=200)
    gs = fig.add_gridspec(
        nrows=1, ncols=1,
        left=0.17, right=0.95,
        top=0.95, bottom=0.17
    )
    ax = fig.add_subplot(gs[0, 0])
    
    x = np.arange(len(data))
    ax.plot(x, data, color=color, linewidth=linewidth)
    ax.set_xlabel('Time [s]', fontsize=dm.fs(0))
    ax.set_ylabel('Amplitude', fontsize=dm.fs(0))
    
    dm.simple_layout(fig)
    
    return fig, ax
```

**2. Use autoreload in your notebook to test the function**:

```python
# notebook.ipynb - Cell 1: Setup
%load_ext autoreload
%autoreload 2

import numpy as np
import dartwork_mpl as dm
from plotting import plot_signal  # Import from external file

# Cell 2: Generate test data
data = np.random.randn(100).cumsum()

# Cell 3: Test the function
fig, ax = plot_signal(data, color='oc.red5', linewidth=1.2)
dm.save_and_show(fig)
```

**3. Modify the function in `plotting.py` and see changes immediately**:

When you modify `plot_signal()` in `plotting.py`, autoreload automatically reloads the module. Just re-run the notebook cell to see the updated function in action—no need to restart the kernel or re-import.

### Setup: Enable Autoreload

In Jupyter or IPython, enable autoreload at the start of your notebook:

```python
%load_ext autoreload
%autoreload 2
```

The `%autoreload 2` setting automatically reloads all modules (except those excluded by `%aimport`) before executing code. This means:
1. Define plot functions in external `.py` files
2. Import them in your notebook
3. Modify functions in the `.py` files
4. Re-run notebook cells to see changes immediately (no kernel restart needed)

### Use `save_and_show()` for Consistent Results

Always use `dm.save_and_show()` instead of `plt.show()`:

```python
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

def plot_example(data: np.ndarray, color: str = 'oc.blue5'):
    """Plot example with configurable color."""
    dm.style.use('scientific')
    fig = plt.figure(figsize=(dm.cm2in(9), dm.cm2in(7)), dpi=200)
    # ... plotting code ...
    dm.simple_layout(fig)
    dm.save_and_show(fig)  # ✅ Use this instead of plt.show()

# Test with different arguments
data = np.random.randn(100).cumsum()
plot_example(data, color='oc.red5')  # Change argument, re-run cell
plot_example(data, color='oc.green5')  # Change argument, re-run cell
```

**Why `save_and_show()`?**
- Shows the **actual saved result**, not just a preview
- Consistent with final exported figure
- Works better in notebooks
- Can specify display size

### Complete Workflow Example

Here's a complete example of the recommended workflow using external Python files:

**Step 1: Create `plotting.py` file** (outside notebook):

```python
# plotting.py
import numpy as np
import matplotlib.pyplot as plt
import dartwork_mpl as dm

def plot_comparison(
    data1: np.ndarray,
    data2: np.ndarray,
    color1: str = 'oc.red5',
    color2: str = 'oc.blue5',
    linewidth: float = 0.7,
    title: str | None = None,
    figsize: tuple[float, float] | None = None
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot two signals for comparison.
    
    Parameters
    ----
    data1 : np.ndarray
        First signal data.
    data2 : np.ndarray
        Second signal data.
    color1 : str, optional
        Color for first signal. Default is 'oc.red5'.
    color2 : str, optional
        Color for second signal. Default is 'oc.blue5'.
    linewidth : float, optional
        Line width for both signals. Default is 0.7.
    title : str | None, optional
        Plot title. If None, no title is shown.
    figsize : tuple[float, float] | None, optional
        Figure size in inches. If None, uses (9cm, 7cm).
    
    Returns
    ----
    fig : matplotlib.figure.Figure
        The created figure.
    ax : matplotlib.axes.Axes
        The axes containing the plot.
    """
    dm.style.use('scientific')
    
    if figsize is None:
        figsize = (dm.cm2in(9), dm.cm2in(7))
    
    fig = plt.figure(figsize=figsize, dpi=200)
    gs = fig.add_gridspec(
        nrows=1, ncols=1,
        left=0.17, right=0.95,
        top=0.95, bottom=0.17
    )
    ax = fig.add_subplot(gs[0, 0])
    
    x = np.arange(len(data1))
    ax.plot(x, data1, color=color1, linewidth=linewidth, label='Signal 1')
    ax.plot(x, data2, color=color2, linewidth=linewidth, label='Signal 2')
    
    ax.set_xlabel('Time [s]', fontsize=dm.fs(0))
    ax.set_ylabel('Amplitude', fontsize=dm.fs(0))
    
    if title:
        ax.set_title(title, fontsize=dm.fs(1), fontweight=dm.fw(1))
    
    ax.legend(fontsize=dm.fs(-1))
    dm.simple_layout(fig)
    
    return fig, ax
```

**Step 2: Use in notebook** (`notebook.ipynb`):

```python
# Cell 1: Setup autoreload
%load_ext autoreload
%autoreload 2

import numpy as np
import dartwork_mpl as dm
from plotting import plot_comparison  # Import from external file

# Cell 2: Generate test data
data1 = np.random.randn(100).cumsum()
data2 = np.random.randn(100).cumsum() + 5

# Cell 3: Test the function
fig, ax = plot_comparison(data1, data2)
dm.save_and_show(fig)

# Cell 4: Iterate by changing arguments
fig, ax = plot_comparison(
    data1, data2,
    color1='oc.green5',  # Change argument
    color2='oc.orange5',  # Change argument
    linewidth=1.2,  # Change argument
    title='Comparison Plot'  # Add title
)
dm.save_and_show(fig)
```

**Step 3: Modify function in `plotting.py` and test**:

When you modify `plot_comparison()` in `plotting.py` (e.g., add new parameters, change default values), autoreload automatically reloads the module. Just re-run the notebook cells to see the updated function—no kernel restart needed!

### Benefits of This Workflow

1. **Fast iteration**: Modify functions in external files, autoreload updates automatically, re-run cell to see results immediately
2. **Better AI compatibility**: AI assistants work more reliably with separate Python files than notebook cells
3. **No code modification needed**: Function stays the same, only arguments change for visual tweaks
4. **Consistent results**: `save_and_show()` shows actual saved output, matching final exported figures
5. **AI-friendly**: Clear, explicit argument changes that AI can understand and suggest
6. **Version control friendly**: Track function changes independently in `.py` files, separate from notebook outputs
7. **Less error-prone**: No risk of breaking code when making visual changes via arguments
8. **Reusable**: Import the same functions across multiple notebooks

## Summary: Best Practices

1. **Set up context prompts once**:
   ```python
   dm.copy_prompt('layout-guide', '.cursor/rules/layout-guide.mdc')
   dm.copy_prompt('general-guide', '.cursor/rules/general-guide.mdc')
   ```

2. **Create plot functions with arguments**:
   - Make all visual parameters configurable
   - Provide sensible defaults
   - Use type hints and documentation

3. **Define functions in external `.py` files**:
   - Better AI assistant compatibility
   - Improved version control
   - Cleaner notebooks (focus on testing)
   - Reusable across multiple notebooks

4. **Work in autoreload-enabled notebooks**:
   - Enable `%autoreload 2` to automatically reload external modules
   - Import functions from `.py` files
   - Modify functions in external files and see changes immediately
   - Use `dm.save_and_show()` instead of `plt.show()`
   - Iterate by changing function arguments

5. **Ask AI to change arguments, not code**:
   - ✅ "Change color to 'oc.red5'"
   - ❌ "Make it a bit redder"

Following these practices will make your AI-assisted graph development faster, more reliable, and more enjoyable.

