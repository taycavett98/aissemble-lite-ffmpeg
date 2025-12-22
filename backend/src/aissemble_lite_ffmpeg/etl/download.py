# Copyright 2025 Booz Allen Hamilton.
#
# Booz Allen Hamilton Confidential Information.
#
# The contents of this file are the intellectual property of
# Booz Allen Hamilton, Inc. ("BAH") and are subject to copyright protection
# under the laws of the United States and other countries.
#
# You acknowledge that misappropriation, misuse, or redistribution of content
# on the file could cause irreparable harm to BAH and/or to third parties.
#
# You may not copy, reproduce, distribute, publish, display, execute, modify,
# create derivative works of, transmit, sell or offer for resale, or in any way
# exploit any part of this code or program without BAH's express written permission.
#
# The contents of this code or program contains code
# that is itself or was created using artificial intelligence.
#
# To the best of our knowledge, this code does not infringe third-party intellectual
# property rights, contain errors, inaccuracies, bias, or security concerns.
#
# However, Booz Allen does not warrant, claim, or provide any implied
# or express warranty for the aforementioned, nor of merchantability
# or fitness for purpose.
#
# Booz Allen expressly limits liability, whether by contract, tort or in equity
# for any damage or harm caused by use of this artificial intelligence code or program.
#
# Booz Allen is providing this code or program "as is" with the understanding
# that any separately negotiated standards of performance for said code
# or program will be met for the duration of any applicable contract under which
# the code or program is provided.

"""aissemble_lite_ffmpeg data download script.

Download data for the aissemble_lite_ffmpeg project into the
backend/data/ directory.
"""

from pathlib import Path

import requests

from aissemble_lite_ffmpeg.common import DATA_DIR


def download_file(url: str) -> None:
    """Download a file from a URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    filename = url.split("/")[-1]
    filepath = DATA_DIR / filename

    with Path.open(filepath, "wb") as file:
        file.write(response.content)

    print(f"Downloaded {url} to {filepath}")


def main() -> None:
    """Run ETL pipeline."""
    urls = [
        "https://miroz.com.hr/random/monsters.csv",
    ]

    DATA_DIR.mkdir(exist_ok=True, parents=True)

    map(download_file, urls)
