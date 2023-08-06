import logging
import os
import xml.etree.ElementTree as ElementTree

from typing import Optional


class CoverageFixPathsError(Exception):
    pass


def fix_coverage_filenames(coverage_report: str, source_dir: str, out_file=None, logger=None) -> None:
    if logger is None:
        logger = logging

    # Get data from the coverage report.
    tree = _parse_coverage_report(coverage_report)
    classes = tree.findall('./packages/package/classes/class[@filename]')
    xml_filenames = {c.get('filename') for c in classes}
    xml_prefix = os.path.commonpath(xml_filenames)
    logger.debug(f"Found {len(xml_filenames)} filenames in report.")
    logger.debug(f"Common prefix for filenames in report is '{xml_prefix}'.")

    # Find the shallowest location of the files in the coverage report on the actual file system,
    # and update the coverage report accordingly.
    new_prefix = _find_first_matching_prefix(xml_filenames, xml_prefix, source_dir, logger)
    if new_prefix is None:
        raise CoverageFixPathsError(f'Cannot find all coverage report files in the directory {source_dir}')
    logger.info(f"Replacing prefix '{xml_prefix}' with '{new_prefix}'.")
    _update_report_filenames(new_prefix, xml_prefix, classes)
    _update_sources_tags(source_dir, tree, logger)

    # Write out the updated coverage file.
    if out_file:
        target = out_file
    else:
        target = coverage_report
    tree.write(target)
    logger.debug(f"Done writing out new coverage report to {target}.")


def _parse_coverage_report(coverage_report_path: str) -> ElementTree.ElementTree:
    try:
        tree = ElementTree.parse(coverage_report_path)
    except FileNotFoundError:
        raise CoverageFixPathsError(f"Cannot find coverage report {coverage_report_path}.")
    except IsADirectoryError:
        raise CoverageFixPathsError(f"Given coverage report {coverage_report_path} is a directory.")
    except ElementTree.ParseError as e:
        raise CoverageFixPathsError(f"Error parsing coverage report (error code {e.code}).")
    return tree


def _find_first_matching_prefix(xml_filenames, xml_prefix, source_dir, logger) -> Optional[str]:
    # Distill a bit of information from the XML filenames.
    xml_basenames = {os.path.basename(f) for f in xml_filenames}
    xml_root_files = set()
    xml_root_folders = set()
    xml_rel_filenames = set()
    for filename in xml_filenames:
        relative_filename = os.path.relpath(filename, start=xml_prefix)
        xml_rel_filenames.add(relative_filename)
        *folders, file = relative_filename.split(os.sep)
        if not folders:
            xml_root_files.add(file)
        else:
            xml_root_folders.add(folders[0])

    # Parse data from the file system.
    source_filenames = set()
    source_paths = []
    for path, subdirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(path, start=source_dir)
        if xml_root_files.issubset(set(files)) and xml_root_folders.issubset(set(subdirs)):
            source_paths.append(rel_path)
        for file in files:
            if file in xml_basenames:
                filename = _normjoin(rel_path, file)
                source_filenames.add(filename)
    logger.debug(f"Found {len(source_paths)} possible matching source directories.")
    logger.debug(f"Found {len(source_filenames)} file base names in source dir that match those in report.")

    # Attempt to find the first / shallowest matching prefix (breadth-first).
    first_prefix = None
    source_paths = sorted(source_paths, key=lambda path: (path.count(os.sep), path.startswith('.'), path.lower()))
    for source_path in source_paths:
        is_match = True
        for xml_rel_filename in xml_rel_filenames:
            if _normjoin(source_path, xml_rel_filename) not in source_filenames:
                is_match = False
                break
        if is_match:
            first_prefix = source_path
            break

    return first_prefix


def _update_report_filenames(new_prefix: str, old_prefix: str, classes) -> None:
    for c in classes:
        old_filename = c.get('filename')
        new_filename = _normjoin(
            new_prefix,
            os.path.relpath(old_filename, start=old_prefix)
        )
        c.set('filename', new_filename)


def _update_sources_tags(source_dir: str, tree, logger) -> None:
    # Lastly, update the <sources> tag.
    sources = tree.find('./sources')
    for source in list(iter(sources)):
        logger.debug(f"Removing source path {source.text} from report.")
        sources.remove(source)
    abs_source_path = os.path.abspath(source_dir)
    logger.debug(f"Adding source path {abs_source_path} to report.")
    source_element = ElementTree.Element('source')
    source_element.text = abs_source_path
    sources.append(source_element)


def _normjoin(*args):
    return os.path.normpath(os.path.join(*args))
