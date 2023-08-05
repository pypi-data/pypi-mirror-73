import datetime
import math
import os

from entomb import (
    constants,
    utilities,
)


@utilities.hide_cursor()
def produce_report(path, include_git):
    """Print a report.

    Parameters
    ----------
    path : str
        An absolute path.
    include_git: bool
        Whether to include git files and directories.

    Returns
    -------
    None

    """
    # Set up.
    directory_count = 0
    immutable_file_count = 0
    link_count = 0
    mutable_file_count = 0

    # Print the operation.
    print("Produce report")
    print()

    # If the path is a file or link, print an abbreviated report then return.
    if os.path.isfile(path):
        _print_file_or_link_report(path)
        return

    # Print the progress header and set up the progress bar.
    utilities.print_header("Progress")
    total_file_paths = utilities.count_file_paths(path, include_git)
    start_time = datetime.datetime.now()
    utilities.print_progress_bar(start_time, 0, total_file_paths)

    # Walk the tree.
    for root_dir, dirnames, filenames in os.walk(path):

        # Exclude git files and directories if directed.
        if not include_git:
            dirnames[:] = [d for d in dirnames if d != ".git"]

        # Count the directory.
        directory_count += 1

        # Examine each file path.
        for filename in filenames:
            file_path = os.path.join(root_dir, filename)

            # Count the link.
            if os.path.islink(file_path):
                link_count += 1

            # Count the file.
            else:
                if utilities.file_is_immutable(file_path):
                    immutable_file_count += 1
                else:
                    mutable_file_count += 1

            # Update the progress bar.
            utilities.print_progress_bar(
                start_time,
                (immutable_file_count + mutable_file_count + link_count),
                total_file_paths,
            )

    print()
    print()

    _print_full_report(
        directory_count,
        link_count,
        immutable_file_count,
        mutable_file_count,
    )


def _print_file_or_link_report(path):
    """Print a report for a path which is a file or a link.

    This function assumes that the path has already been confirmed to reference
    a file or link.

    Parameters
    ----------
    path : str
        An absolute path.

    Returns
    -------
    None

    """
    utilities.print_header("Report")

    if os.path.islink(path):
        print("A link has no immutable attribute")
    else:
        if utilities.file_is_immutable(path):
            print("File is immutable")
        else:
            print("File is mutable")

    print()


def _print_full_report(directory_count, link_count, immutable_file_count,
                       mutable_file_count):
    """Print a report for a path which is a file or a link.

    Parameters
    ----------
    directory_count : int
        The number of directories counted.
    link_count : int
        The number of links counted.
    immutable_file_count : int
        The number of immutable files counted.
    mutable_file_count : int
        The number of mutable files counted.

    Returns
    -------
    None

    """
    # Do calculations.
    subdirectory_count = directory_count - 1
    total_file_count = immutable_file_count + mutable_file_count

    try:
        entombed_proportion = immutable_file_count / total_file_count
        entombed_percentage_integer = math.floor(entombed_proportion * 100)
        entombed_percentage = "{}%".format(entombed_percentage_integer)
    except ZeroDivisionError:
        entombed_percentage = "n/a"

    # Print the report.
    report_separator = "-" * constants.TABLE_WIDTH
    print("Report")
    print(report_separator)
    print(
        "Immutable files",
        "{:,}".format(immutable_file_count).rjust(constants.TABLE_WIDTH - 16),
    )
    print(report_separator)
    print(
        "Mutable files",
        "{:,}".format(mutable_file_count).rjust(constants.TABLE_WIDTH - 14),
    )
    print(report_separator)
    print(
        "All files",
        "{:,}".format(total_file_count).rjust(constants.TABLE_WIDTH - 10),
    )
    print(report_separator)
    print(
        "Entombed",
        entombed_percentage.rjust(constants.TABLE_WIDTH - 9),
    )
    print(report_separator)
    print(
        "Links",
        "{:,}".format(link_count).rjust(constants.TABLE_WIDTH - 6),
    )
    print(report_separator)
    print(
        "Sub-directories",
        "{:,}".format(subdirectory_count).rjust(constants.TABLE_WIDTH - 16),
    )
    print(report_separator)
    print()
