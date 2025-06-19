#!/bin/bash

set -e
echo "TailsNet Updater v1.0.0"
# URL of the instruction file
URL="http://192.168.0.107/tailsnet/client/files.txt"
TEMP_FILE="/tmp/tailsnet_files.txt"

# Download the file
curl -fsSL "$URL" -o "$TEMP_FILE" || {
    echo "Failed to download instruction file."
    exit 1
}

# Read and interpret each line
while IFS= read -r line; do
    # Skip empty lines or comments
    [[ -z "$line" || "$line" == \#* ]] && continue

    cmd=$(echo "$line" | cut -d' ' -f1)
    args=$(echo "$line" | cut -d' ' -f2-)

    case "$cmd" in
        DOWNLOAD)
            url=$(echo "$args" | cut -d' ' -f1)
            dest=$(echo "$args" | cut -d' ' -f2-)
            echo "Downloading $url to $dest..."
            curl -fsSL "$url" -o "$dest"
            ;;
        DIR)
            echo "Creating directory: $args"
            mkdir -p "$args"
            ;;
        CMD)
            echo "Running command: $args"
            bash -c "$args"
            ;;
        DEL)
            echo "Deleting file: $args"
            rm -f "$args"
            ;;
        DELDIR)
            echo "Deleting directory: $args"
            rm -rf "$args"
            ;;
        *)
            echo "Unknown command: $cmd"
            ;;
    esac
done < "$TEMP_FILE"

echo "All instructions processed."
