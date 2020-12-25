# Script to pull transaction information from RBC pdfs

I wrote this a couple of years ago, it has problems with H's and ends up recognizing them as 11, and some other small issues.

I give no guarantee about accuracy of the output files vs the input. This uses character recognition, I suggest you compare the data after running the script.

I really only run it yearly to do an audit for taxes. I can't quite recall what the proper requirments.txt values are. As well as I think there are some specific libraries needed outside of pip for the ocr.

Create a virtualenv:

    virtualenv -p python2 venv

You'll need to install some packages. Not exactly sure the minimal set that is required, see below.

Usage:

    rbc_ocr.py "PATH/TO/PDF/FILE"

the packages I have installed in my virtualenv are:

    image==1.5.27
      - django [required: Any, installed: 1.11.18]
        - pytz [required: Any, installed: 2018.9]
      - pillow [required: Any, installed: 5.4.1]
    matplotlib==2.2.3
      - backports.functools-lru-cache [required: Any, installed: 1.5]
      - cycler [required: >=0.10, installed: 0.10.0]
        - six [required: Any, installed: 1.12.0]
      - kiwisolver [required: >=1.0.1, installed: 1.0.1]
        - setuptools [required: Any, installed: 44.1.1]
      - numpy [required: >=1.7.1, installed: 1.16.0]
      - pyparsing [required: >=2.0.1,!=2.1.6,!=2.1.2,!=2.0.4, installed: 2.3.1]
      - python-dateutil [required: >=2.1, installed: 2.7.5]
        - six [required: >=1.5, installed: 1.12.0]
      - pytz [required: Any, installed: 2018.9]
      - six [required: >=1.10, installed: 1.12.0]
      - subprocess32 [required: Any, installed: 3.5.3]
    opencv-python==4.0.0.21
      - numpy [required: >=1.11.1, installed: 1.16.0]
    pdf2image==1.4.0
      - pillow [required: Any, installed: 5.4.1]
    pip==20.3.3
    pkg-resources==0.0.0
    pyocr==0.5.3
      - Pillow [required: Any, installed: 5.4.1]
      - six [required: Any, installed: 1.12.0]
    tesseract==0.1.3
    unicodecsv==0.14.1
    Wand==0.5.0
    wheel==0.36.2

There was some specifics I needed to get tesseract/pyocr installed, hopefully the above helps.
