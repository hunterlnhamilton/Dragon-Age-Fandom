#!/bin/bash

# --- CONFIGURATION START ---
SITE_NAME="Dragon Age: Fandom"
INPUT_DIR="./DAFics"
DEPLOYMENT_URL="https://dragonagefandom.pages.dev"
THEME_CSS="assets/css/thedas.css"
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

# Page dates come from git history, so make sure the clone has all of it
if [ "$(git rev-parse --is-shallow-repository 2>/dev/null)" = "true" ]; then
  git fetch --quiet --unshallow || echo "Warning: shallow clone, page dates will be hidden."
fi

# Turn Loresmith notes into sheets, category pages, timeline and calendars.
# Works on a copy in ./.build, so the vault itself is never touched.
echo "Preparing Loresmith pages..."
python3 tools/loresmith_site.py "$INPUT_DIR" ./.build

# Run the build
echo "Building site..."
./kiln generate \
  --input ./.build \
  --output ./public \
  --flat-urls=true \
  --name "$SITE_NAME" \
  --url "$DEPLOYMENT_URL"

# Put back what Kiln can't get from the staged pages: graph links, page
# descriptions, real word counts and dates
echo "Finishing pages..."
python3 tools/postbuild.py ./public ./.build-manifest.json

# Add the Fade theme on top of Kiln's built-in one
echo "Applying Fade theme..."
mkdir -p ./public/assets/css
cp "$THEME_CSS" ./public/assets/css/
cp assets/favicon.svg ./public/favicon.svg
CSS_HREF="/assets/css/$(basename "$THEME_CSS")"
# Also fix Kiln's home link: with flat URLs it writes href="//", which browsers block
find ./public -name '*.html' -exec \
  sed -i -e "s#</head>#<link rel=\"icon\" href=\"/favicon.svg\" type=\"image/svg+xml\"><link rel=\"stylesheet\" href=\"${CSS_HREF}\"></head>#" \
         -e 's#href="//"#href="/"#g' \
         -e 's#\(pages\.dev\)//#\1/#g' {} +

echo "Kiln build complete successfully"
