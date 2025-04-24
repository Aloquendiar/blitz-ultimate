#!/bin/bash

# Set a variable to track whether the ARK build failed
FAILED_ARK_BUILD=0

# Set the path to arkhelper and check if the script is running on macOS
if [[ $(uname -s) == "Darwin" ]]; then
    echo "Running on macOS"
    # macOS-specific path to arkhelper executable
    ARKHELPER_PATH="$(pwd)/dependencies/macos/arkhelper"
else
    echo "Not running on macOS"
    # Assume Linux or other Unix-like systems
    ARKHELPER_PATH="$(pwd)/dependencies/linux/arkhelper"
fi

# Move Xbox files out of ark to reduce file size
echo "Moving Xbox files out of ark"
find "$PWD/_ark" -type f -name "*.*_xbox" | while read -r filepath; do
   relative_path="${filepath#$PWD/_ark/}"
   dest_path="$PWD/_temp/$relative_path"

   mkdir -p "$(dirname "$dest_path")"

   mv "$filepath" "$dest_path"
done

# Building PS3 ARK
echo
echo "Building PS3 ARK"
"$ARKHELPER_PATH" dir2ark "$PWD/_ark" "$PWD/_build/ps3/USRDIR/gen" -n "patch_ps3" -e -v 6 -s 4073741823
if [ $? -ne 0 ]; then
    FAILED_ARK_BUILD=1
fi

echo "Moving Xbox files back"
for folder in "$PWD/_temp"/*; do
  [ -d "$folder" ] || continue
  name=$(basename "$folder")

  find "$folder" -type f | while read -r f; do
    rel_path=${f#"$folder/"}
    dest="$PWD/_ark/$name/$rel_path"
    mv "$f" "$dest"
  done

done

rm -r "$PWD/_temp"

# Check if the ARK build failed and provide appropriate message
echo
if [ "$FAILED_ARK_BUILD" -ne 1 ]; then
    echo "Successfully built Rock Band Blitz Ultimate ARK files. You may find the files needed to place on your PS3 in /_build/ps3/"
else
    echo "Error building ARK. Download the repo again or some dta file is bad p.s turn echo on to see what arkhelper says"
fi

echo
read -p "Press Enter to continue..."
