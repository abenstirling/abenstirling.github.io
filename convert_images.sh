#!/bin/bash

# Install required tools if not present
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg..."
    brew install ffmpeg
fi

# Convert GIFs to WebP
for gif in images/*.gif; do
    if [ -f "$gif" ]; then
        webp="${gif%.gif}.webp"
        echo "Converting $gif to $webp..."
        ffmpeg -i "$gif" -c:v libwebp -lossless 0 -compression_level 6 -q:v 50 -loop 0 -preset picture -an -vsync 0 "$webp"
    fi
done

echo "Conversion complete!" 