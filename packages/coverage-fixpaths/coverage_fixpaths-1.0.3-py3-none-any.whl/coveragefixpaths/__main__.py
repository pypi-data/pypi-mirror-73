import argparse
import logging

from . import fix_coverage_filenames


def main():
    args = _arguments()
    logger = _get_logger(args.loglevel)
    all_ok = fix_coverage_filenames(args.report, args.source, out_file=args.out, logger=logger)
    if all_ok:
        exit(0)
    else:
        exit(1)


def _arguments():
    parser = argparse.ArgumentParser(description='Automatically fix coverage.xml filenames.')
    parser.add_argument('report', type=str, metavar='REPORT', help='Path of the coverage report (XML).')
    parser.add_argument('--source',  default='.', metavar='PATH', help='Directory to search for source files.')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error'], help='Log level.')
    parser.add_argument('--out', default=None, metavar='FILE', help='File to write out to. Overwrite input file if not given.')
    return parser.parse_args()


def _get_logger(level):
    logging.basicConfig()
    logger = logging.getLogger(name='coveragefixpaths')
    logger.setLevel(level.upper())
    return logger


if __name__ == '__main__':
    main()
