import argparse
import os
import random  # For generating a temp file for stdin
import string  # For generating a temp file for stdin
import sys
import tempfile

# ipwb modules
from ipwb import settings, replay, indexer, util
from ipwb.error_handler import exception_logger
from .__init__ import __version__ as ipwb_version


@exception_logger(catch=not settings.DEBUG)
def main():
    checkArgs(sys.argv)


def checkArgs_index(args):
    util.check_daemon_is_alive()

    encKey = None
    compressionLevel = None
    if args.e:
        encKey = ''
    if args.c:
        compressionLevel = 6  # Magic 6, TA-DA!

    indexer.indexFileAt(args.warcPath, encKey, compressionLevel,
                        args.compressFirst, outfile=args.outfile,
                        debug=args.debug)


def checkArgs_replay(args):
    suppliedIndexParameter = hasattr(args, 'index') and args.index is not None
    likelyPiping = not sys.stdin.isatty()

    if not suppliedIndexParameter and likelyPiping:
        cdxjIn = ''.join(sys.stdin.readlines())
        if len(cdxjIn) == 0:  # Daemon was not running, so nothing was indexed
            print(('ERROR: The IPFS daemon must be running to pipe input from'
                  ' the indexer to the replay system.'))
            sys.exit()

        random.seed()
        # Write data to temp file (sub-optimal)

        fh, args.index = tempfile.mkstemp(suffix='.cdxj')
        os.close(fh)
        with open(args.index, 'w') as f:
            f.write(cdxjIn)

        suppliedIndexParameter = True

    proxy = None
    if hasattr(args, 'proxy') and args.proxy is not None:
        print(f'Proxying to {args.proxy}')
        proxy = args.proxy

    # TODO: add any other sub-arguments for replay here
    if suppliedIndexParameter:
        replay.start(cdxjFilePath=args.index, proxy=proxy)
    else:
        print('ERROR: An index file must be specified if not piping, e.g.,')
        print(("> ipwb replay "
               f"{os.path.join('path', 'to', 'your', 'index.cdxj')}\n"))

        args.onError()
        sys.exit()


def checkArgs(argsIn):
    """
    Check to ensure valid arguments were passed in and provides guidance
    on the available options if not
    """
    parser = argparse.ArgumentParser(
        description='InterPlanetary Wayback (ipwb)', prog="ipwb")
    subparsers = parser.add_subparsers(
        title="ipwb commands",
        description=("Invoke using \"ipwb <command>\""
                     ", e.g., ipwb replay <cdxjFile>"))

    indexParser = subparsers.add_parser(
        'index',
        prog="ipwb",
        description="Index a WARC file for replay in ipwb",
        help="Index a WARC file for replay in ipwb")
    indexParser.add_argument(
        'warcPath',
        help="Path to a WARC[.gz] file",
        metavar="index <warcPath>",
        nargs='+',
        default=None)
    indexParser.add_argument(
        '-e',
        help="Encrypt WARC content prior to adding to IPFS",
        action='store_true',
        default=False)
    indexParser.add_argument(
        '-c',
        help='Compress WARC content prior to adding to IPFS',
        action='store_true',
        default=False)
    indexParser.add_argument(
        '--compressFirst',
        help='Compress data before encryption, where applicable',
        action='store_true',
        default=False)
    indexParser.add_argument(
        '-o', '--outfile',
        help='Path to an output CDXJ file, defaults to STDOUT',
        default=None)
    indexParser.add_argument(
        '--debug',
        help='Convenience flag to help with testing and debugging',
        action='store_true',
        default=False)
    indexParser.set_defaults(func=checkArgs_index)

    replayParser = subparsers.add_parser(
        'replay',
        prog="ipwb replay",
        description="Start the ipwb relay system",
        help="Start the ipwb replay system")
    replayParser.add_argument(
        'index',
        help='path, URI, or multihash of file to use for replay',
        nargs='?')
    replayParser.add_argument(
        '-P', '--proxy',
        help='Proxy URL',
        metavar='<host:port>',
        nargs='?')
    replayParser.set_defaults(func=checkArgs_replay,
                              onError=replayParser.print_help)

    parser.add_argument(
        '-d', '--daemon',
        help=("Multi-address of IPFS daemon "
              "(default /dns/localhost/tcp/5001/http)"),
        default=util.IPFSAPI_MUTLIADDRESS,
        dest='daemon_address')
    parser.add_argument(
        '-v', '--version', help='Report the version of ipwb', action='version',
        version=f'InterPlanetary Wayback {ipwb_version}')
    parser.add_argument(
        '-u', '--update-check',
        action='store_true',
        help='Check whether an updated version of ipwb is available'
        )
    parser.set_defaults(func=util.checkForUpdate)

    argCount = len(argsIn)
    cmdList = ['index', 'replay']
    baseParserFlagList = ['-d', '--daemon', '-v', '--version',
                          '-u', '--update-check']

    # Various invocation error, used to show appropriate help
    cmdError_index = argCount == 2 and argsIn[1] == 'index'
    cmdError_noCommand = argCount == 1
    cmdError_invalidCommand = argCount > 1 \
        and argsIn[1] not in cmdList + baseParserFlagList

    if cmdError_noCommand or cmdError_invalidCommand:
        parser.print_help()
        sys.exit()
    elif cmdError_index:
        indexParser.print_help()
        sys.exit()

    results = parser.parse_args()
    results.func(results)

    return results


if __name__ == "__main__":
    main()
