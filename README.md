# Script to pull transaction information from RBC pdfs

I wrote this a couple of years ago, it has problems with H's and ends up recognizing them as 11, and some other small issues.

I give no guarantee about accuracy of the output files vs the input. This uses character recognition, I suggest you compare the data after running the script.

I really only run it yearly to do an audit for taxes. I can't quite recall what the proper requirments.txt values are. As well as I think there are some specific libraries needed outside of pip for the ocr.

## Setup:

    virtualenv -p python3 venv
    pip install -r requirements.txt

## Usage:

    rbc_ocr.py "PATH/TO/PDF/FILE"

