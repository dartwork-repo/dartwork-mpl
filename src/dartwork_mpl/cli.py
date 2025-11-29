#!/usr/bin/env python3
"""Command Line Interface for dartwork-mpl library.

This module provides a command-line interface for dartwork-mpl library
utilities including installation and version information.
"""

import argparse
import sys

from .install import install_llm_txt, uninstall_llm_txt


def main() -> None:
    """
    Main CLI entry point.

    Handles command-line argument parsing and dispatches to appropriate
    functions based on the command provided.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="dartwork-mpl CLI tools", prog="dmpl"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser(
        "install-llm",
        help="Install dartwork-mpl usage guide for IDE integrations",
    )
    install_parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default=None,
        help="Project directory (default: current directory)",
    )

    # Uninstall command
    uninstall_parser = subparsers.add_parser(
        "uninstall-llm",
        help="Remove dartwork-mpl usage guide from IDE integrations",
    )
    uninstall_parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default=None,
        help="Project directory (default: current directory)",
    )

    # Version command
    subparsers.add_parser("version", help="Show dartwork-mpl version")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "install-llm":
        try:
            install_llm_txt(project_dir=args.dir)
        except Exception as e:
            print(f"❌ Installation failed: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "uninstall-llm":
        try:
            uninstall_llm_txt(project_dir=args.dir)
        except Exception as e:
            print(f"❌ Uninstallation failed: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "version":
        try:
            import dartwork_mpl

            print(f"dartwork-mpl version: {dartwork_mpl.__version__}")
        except AttributeError:
            print("dartwork-mpl version: development")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
