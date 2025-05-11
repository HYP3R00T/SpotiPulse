#!/bin/bash
set -euo pipefail

# Define paths
MISE_PATH="$HOME/.local/bin"
MISE_SHIM_PATH="$HOME/.local/share/mise/shims"
RC_FILE="${ZSH_VERSION:+$HOME/.zshrc}"
RC_FILE="${RC_FILE:-$HOME/.bashrc}"

# Install mise if not already installed
if ! command -v mise &>/dev/null; then
    echo "Installing mise..."
    curl -sSf https://mise.run | MISE_INSTALL_PATH="$MISE_PATH/mise" sh
fi

# Ensure mise is in PATH and activate it
export PATH="$MISE_PATH:$MISE_SHIM_PATH:$PATH"
eval "$(mise activate)"

# Optionally, append mise activation to RC file
if ! grep -q 'eval "$(mise activate)"' "$RC_FILE"; then
    echo 'eval "$(mise activate)"' >>"$RC_FILE"
fi

# Install pre-commit if not already installed
if ! command -v pre-commit &>/dev/null; then
    echo "Installing pre-commit..."
    mise install pre-commit
    mise use -g pre-commit@latest
fi

# Set up pre-commit hooks if config exists
if [[ -f .pre-commit-config.yaml ]]; then
    echo "Setting up pre-commit hooks..."
    pre-commit install
else
    echo "No .pre-commit-config.yaml found. Please create one to configure pre-commit."
fi

# Explicitly enable idiomatic version files for Python to remove warnings
mise settings add idiomatic_version_file_enable_tools python

# Install uv using mise
mise install uv
mise use -g uv@latest

# Check installation
if ! command -v uv &>/dev/null; then
    echo "❌ uv installation failed. Ensure mise is properly configured."
    exit 1
fi

uv venv
source .venv/bin/activate
uv sync

echo "Setup complete."
