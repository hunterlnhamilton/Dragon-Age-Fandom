#!/bin/bash

# --- CONFIGURATION START ---
SITE_NAME="Dragon Age: Fandom"
INPUT_DIR="./DAFics"
DEPLOYMENT_URL="https://dragonagefandom.pages.dev"
# --- CONFIGURATION END ---

# Exit immediately if any command fails
set -e

echo "Kiln build script"

# Find the latest version of Kiln
LATEST_TAG=$(curl -s https://api.github.com/repos/otaleghani/kiln/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST_TAG" ]; then
  echo "Error: Could not determine latest Kiln version."
  exit 1
fi

echo "Detected latest version: $LATEST_TAG"

# Download the binary
URL="https://github.com/otaleghani/kiln/releases/download/${LATEST_TAG}/kiln_linux_amd64"

echo "Downloading binary from $URL..."
curl -L -o ./kiln "$URL"
chmod +x ./kiln

# Run the build
echo "Building site..."
./kiln generate \
  --input "$INPUT_DIR" \
  --output ./public \
  --flat-urls=true \
  --name "$SITE_NAME" \
  --url "$DEPLOYMENT_URL"

echo "Kiln build complete successfully"
