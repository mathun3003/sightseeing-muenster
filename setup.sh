#! /bin/sh
pip install --upgrade pip
pip install pre-commit
pip install git+https://github.com/ostrolucky/Bulk-Bing-Image-downloader
pip install -r requirements.txt

pre-commit install --install-hooks
