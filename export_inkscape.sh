#!/bin/bash
# Scripts for batch conversion of Inkscape files into PDFs and PNGs:
#     - Find all the Inkscape files in the input folder.
#     - Create the PDF and PNG files in the output folder.
#
# Thomas Guillod - Dartmouth College
# Mozilla Public License Version 2.0

set -o nounset
set -o pipefail

function convert_folder {
    # get the folders
    INPUT=$1
    OUTPUT=$2
    
    # show the processed folders
    echo "================== ${INPUT} / ${OUTPUT}"
        
    # create the folders
    mkdir -p ${INPUT}
    mkdir -p ${OUTPUT}

    # get the command line parameters
    for name in ${INPUT}/*.svg; do
        # get the filename without the extension
        [ -f "$name" ] || break
        name=$(basename -- "$name" .svg)
        file_svg="${INPUT}/${name}.svg"
        file_pdf="${OUTPUT}/${name}.pdf"
        file_png="${OUTPUT}/${name}.png"
    
        # show the processed file
        echo "========= ${name}"
    
       # convert to PDF (for the paper)
        inkscape ${file_svg} --export-filename ${file_pdf}
    
        # convert to PNG (for the slides)
        inkscape ${file_svg} --export-filename ${file_png} --export-dpi 500
    done
}

# run the script
convert_folder "fig_schemas" "export"
convert_folder "fig_plots" "export"

# successful termination
exit 0

