"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from tributors.main import TributorsClient
from .utils import parse_extra
import os
import sys


def main(args, extra):

    client = TributorsClient(skip_cache=args.skip_cache)

    # Parse extra arguments
    extra = parse_extra(extra)

    # Start with user provided parsers
    parsers = args.parsers

    # If unset, try to detect files
    if "unset" in parsers:
        lookup = {
            "allcontrib": extra.get("--allcontrib-file", ".all-contributorsrc"),
            "zenodo": extra.get("--zenodo-file", ".zenodo.json"),
            "codemeta": extra.get("--codemeta-file", ".codemeta.json"),
        }

        parsers = []
        for parser, filename in lookup.items():
            if os.path.exists(filename):
                parsers.append(parser)

        # Exit if no parsers auto-detected
        if not parsers:
            sys.exit("No parsers auto-detected. Specify a parser name instead?")

    if "all" in parsers:
        client.update(
            parsers=["zenodo", "allcontrib", "codemeta"],
            thresh=args.thresh,
            repo=args.repo,
            params=extra,
        )

    else:
        client.update(parsers=parsers, repo=args.repo, params=extra, thresh=args.thresh)
