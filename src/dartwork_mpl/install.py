"""
Installation utilities for IDE integrations and LLM assistants.
"""
import os
import shutil
from pathlib import Path


def install_llm_txt(project_dir=None):
    """
    Install dartwork-mpl usage guide to project's IDE integration folders.
    
    This function creates appropriate instructions for different AI coding
    assistants by installing the usage guide to:
    - .claude/commands/ (for Claude Code)
    - .cursor/ (for Cursor IDE)
    
    Parameters
    ----------
    project_dir : str or Path, optional
        Project directory path. If None, uses current working directory.
    """
    # Get the usage guide path from the asset folder
    usage_guide_path = Path(__file__).parent / 'asset' / 'USAGE_GUIDE.md'
    
    if not usage_guide_path.exists():
        raise FileNotFoundError(f"Usage guide not found at: {usage_guide_path}")
    
    # Get project directory (current working directory if not specified)
    if project_dir is None:
        project_dir = Path.cwd()
    else:
        project_dir = Path(project_dir)
    
    # Install for Claude Code
    claude_dir = project_dir / '.claude' / 'commands'
    claude_dir.mkdir(parents=True, exist_ok=True)
    claude_file = claude_dir / 'dartwork-mpl-usage.md'
    
    # Install for Cursor IDE
    cursor_dir = project_dir / '.cursor'
    cursor_dir.mkdir(parents=True, exist_ok=True)
    cursor_file = cursor_dir / 'dartwork-mpl-usage.md'
    
    # Read the original usage guide
    with open(usage_guide_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create Claude Code version with command prefix
    claude_content = f"""# dartwork-mpl Library Usage Command

This command provides comprehensive usage guide for the dartwork-mpl library.

## Usage
Type `/dartwork-mpl` to get help with dartwork-mpl library usage.

---

{content}
"""
    
    # Create Cursor IDE version with instruction format
    cursor_content = f"""// Cursor IDE Instructions for dartwork-mpl library
// This file provides context about dartwork-mpl library usage

{content}
"""
    
    # Write files
    with open(claude_file, 'w', encoding='utf-8') as f:
        f.write(claude_content)
    
    with open(cursor_file, 'w', encoding='utf-8') as f:
        f.write(cursor_content)
    
    print(f"✅ dartwork-mpl usage guide installed successfully!")
    print(f"📁 Project: {project_dir}")
    print(f"📁 Claude Code: {claude_file}")
    print(f"📁 Cursor IDE: {cursor_file}")
    print()
    print("🔧 Usage:")
    print("- In Claude Code: Type '/dartwork-mpl' for help")
    print("- In Cursor IDE: The AI will automatically have access to dartwork-mpl context")


def uninstall_llm_txt(project_dir=None):
    """
    Remove dartwork-mpl usage guide from project's IDE integration folders.
    
    Parameters
    ----------
    project_dir : str or Path, optional
        Project directory path. If None, uses current working directory.
    """
    # Get project directory (current working directory if not specified)
    if project_dir is None:
        project_dir = Path.cwd()
    else:
        project_dir = Path(project_dir)
    
    # Files to remove
    files_to_remove = [
        project_dir / '.claude' / 'commands' / 'dartwork-mpl-usage.md',
        project_dir / '.cursor' / 'dartwork-mpl-usage.md'
    ]
    
    removed_files = []
    for file_path in files_to_remove:
        if file_path.exists():
            file_path.unlink()
            removed_files.append(file_path)
    
    if removed_files:
        print("✅ dartwork-mpl usage guide uninstalled successfully!")
        for file_path in removed_files:
            print(f"🗑️  Removed: {file_path}")
    else:
        print("ℹ️  No dartwork-mpl usage guides found to remove.")


if __name__ == "__main__":
    install_llm_txt()