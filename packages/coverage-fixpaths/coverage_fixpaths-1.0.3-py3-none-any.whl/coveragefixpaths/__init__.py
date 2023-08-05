import logging
import os
import xml.etree.ElementTree as ElementTree


def fix_coverage_filenames(coverage_report, source_dir, out_file=None, logger=None):
    if logger is None:
        logger = logging
    # Parse data from the coverage report.
    try:
        tree = ElementTree.parse(coverage_report)
    except FileNotFoundError:
        logger.error(f"Cannot find coverage report {coverage_report}.")
        return False
    except IsADirectoryError:
        logger.error(f"Given coverage report {coverage_report} is a directory.")
        return False
    except ElementTree.ParseError as e:
        logger.error(f"Error parsing coverage report (error code {e.code}).")
        return False
    root = tree.getroot()
    child_parent_mapping = {child: parent for parent in tree.iter('classes') for child in parent}
    classes = root.findall('./packages/package/classes/class[@filename]')
    xml_filenames = {c.get('filename') for c in classes}
    xml_basenames = {os.path.basename(f) for f in xml_filenames}
    xml_prefix = os.path.commonpath(xml_filenames)
    xml_rel_filenames = {os.path.relpath(f, start=xml_prefix) for f in xml_filenames}
    logger.debug(f"Found {len(xml_filenames)} filenames in report.")
    logger.debug(f"Common prefix for filenames in report is '{xml_prefix}'.")

    # Parse data from the file system.
    source_filenames = set()
    source_paths = []
    for path, subdirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(path, start=source_dir)
        source_paths.append(rel_path)
        for file in files:
            if file in xml_basenames:
                filename = _normjoin(rel_path, file)
                source_filenames.add(filename)
    logger.debug(f"Found {len(source_filenames)} file base names in source dir that match those in report.")

    # Attempt to find the best relative path in the file system that matches the paths in the coverage report.
    score_prefix_tuples = []
    for source_path in source_paths:
        xml_moved_filenames = {_normjoin(source_path, f) for f in xml_rel_filenames}
        intersection = xml_moved_filenames & source_filenames
        num_missing = len(xml_rel_filenames) - len(intersection)
        dir_depth = len(_normjoin(source_dir, source_path).split(os.sep))
        score_prefix_tuples.append((num_missing, dir_depth, source_path))
    best_missing, _, best_prefix = sorted(score_prefix_tuples)[0]
    logger.info(f"Replacing prefix '{xml_prefix}' with '{best_prefix}'.")
    if best_missing > 0:
        logger.warning(f"Removing {best_missing} files from report because they are not in source dir.")

    # Update all the filenames in the XML.
    for c in classes:
        old_filename = c.get('filename')
        new_filename = _normjoin(
            best_prefix,
            os.path.relpath(old_filename, start=xml_prefix)
        )
        if new_filename not in source_filenames:
            logger.debug(f"Removing {new_filename} from report because it is not in source dir.")
            parent = child_parent_mapping[c]
            parent.remove(c)
        else:
            c.set('filename', new_filename)

    # Lastly, update the <sources> tag.
    sources = root.find('./sources')
    for source in list(iter(sources)):
        logger.debug(f"Removing source path {source.text} from report.")
        sources.remove(source)
    abs_source_path = os.path.abspath(source_dir)
    logger.debug(f"Adding source path {abs_source_path} to report.")
    source_element = ElementTree.Element('source')
    source_element.text = abs_source_path
    sources.append(source_element)

    # Write out the updated coverage file.
    if out_file:
        target = out_file
    else:
        target = coverage_report
    tree.write(target)
    logger.debug(f"Done writing out new coverage report to {target}.")

    # Success!
    return True


def _normjoin(*args):
    return os.path.normpath(os.path.join(*args))
