"""
CLI entry point.
"""

import argparse
import json

from . import usage, version
from .retriever import retrieve
from .sources.ncbi import link_reference


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        description=usage[0],
        epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("-v", action="version", version=version(parser.prog))

    parser.add_argument("reference", help="the reference id")

    parser.add_argument(
        "--sizeoff", help="do not consider file size", action="store_true"
    )

    parser.add_argument(
        "--link", help="link protein to transcript", action="store_true"
    )

    parser.add_argument("--parse", help="parse reference content", action="store_true")

    parser.add_argument(
        "--source", help="retrieval source", choices=["ncbi", "ensembl", "lrg"]
    )

    parser.add_argument(
        "--type", help="reference type", choices=["gff3", "genbank", "json", "sequence"]
    )

    parser.add_argument("-c", "--configuration", help="configuration file path")

    args = parser.parse_args()

    if args.link:
        link, method = link_reference(args.reference)
        if link:
            print("{} (from {})".format(link, method))
        return
    else:
        output = retrieve(
            reference_id=args.reference,
            reference_source=args.source,
            reference_type=args.type,
            size_off=args.sizeoff,
            parse=args.parse,
            configuration_path=args.configuration,
        )
        if isinstance(output, dict):
            print(json.dumps(output, indent=2))
        else:
            print(output)
