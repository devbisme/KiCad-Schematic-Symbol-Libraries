# MIT license
#
# Copyright (C) 2015 by XESS Corp.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import

import copy
import csv
from collections import defaultdict

from kipart.common import *
from kipart.kipart import *


def psoc5lp_pin_name_process(name):
    #    leading_paren = re.compile(r'^\s*(?P<paren>\([^)]*\))\s*(?<pin_name>.+)$', re.IGNORECASE)
    #    leading_paren = re.compile(r'^\s*(?P<paren>\([^)]*\))', re.IGNORECASE)
    leading_paren = re.compile(
        r"^\s*(?P<paren>\([^)]*\))\s*(?P<pin_name>.+)$", re.IGNORECASE
    )
    m = leading_paren.match(name)
    if m is not None:
        name = m.group("pin_name") + " " + m.group("paren")
    name = re.sub(r"^\s+", "", name)  # Remove leading spaces.
    name = re.sub(r"\s+$", "", name)  # Remove trailing spaces.
    name = re.sub(
        r'\s*([-@#$%^&*_=+|",.<>!;?]+)\s*', r"\1", name
    )  # Remove spaces around punc.
    name = re.sub(
        r"([\[\{\(]+)\s*", r"\1", name
    )  # Remove spaces around braces and such.
    name = re.sub(
        r"\s*([\]\}\)]+)", r"\1", name
    )  # Remove spaces around braces and such.
    name = re.sub(r"\s+", "_", name)  # Replace spaces with underscores.
    return name


def psoc5lp_reader(part_data_file, part_data_file_name, part_data_file_type=".csv"):
    """Extract pin data from a Cypress PSoC5LP CSV/text/Excel file and return a dictionary of pin data.
       The file contains one or more groups of rows formatted as follows:
           A row with a single field containing the part number.
           Zero or more blank rows.
           A row containing the column headers:
               'Pin', 'Unit', 'Type', 'Style', 'Side', and 'Name'.
               (Only 'Pin' and 'Name' are required. The order of
               the columns is not important.)
           Each succeeding row should contain:
               The 'Pin' column should contain the pin number.
               The 'Unit' column specifies the bank or unit number for the pin.
               The 'Type' column specifies the pin type (input, output,...).
               The 'Style' column specifies the pin's schematic style.
               The 'Side' column specifies the side of the symbol the pin is on.
               The 'Name' column contains the pin name.
           A blank row terminates the pin data for the part and begins
           a new group of rows for another part.
    """

    # If part data file is Excel, convert it to CSV.
    if part_data_file_type == ".xlsx":
        part_data_file = convert_xlsx_to_csv(part_data_file)
    csv_file = part_data_file

    while True:
        # Create a dictionary that uses the unit numbers as keys. Each entry in this dictionary
        # contains another dictionary that uses the side of the symbol as a key. Each entry in
        # that dictionary uses the pin names in that unit and on that side as keys. Each entry
        # in that dictionary is a list of Pin objects with each Pin object having the same name
        # as the dictionary key. So the pins are separated into units at the top level, and then
        # the sides of the symbol, and then the pins with the same name that are on that side
        # of the unit.
        pin_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        # Create a reader that starts from the current position in the CSV file.
        csv_reader = csv.reader(csv_file, skipinitialspace=True)

        # Extract part number from the first non-blank line. Break out of the infinite
        # while loop and stop processing this file if no part number is found.
        (
            part_num,
            part_ref_prefix,
            part_footprint,
            part_manf_num,
            part_datasheet,
            part_desc,
        ) = get_part_info(csv_reader)
        if part_num is None:
            break

        # Get the column header row for the part's pin data.
        headers = clean_headers(get_nonblank_row(csv_reader))

        # Now create a DictReader for grabbing the pin data in each row.
        dict_reader = csv.DictReader(csv_file, headers, skipinitialspace=True)
        for index, row in enumerate(dict_reader):

            # A blank line signals the end of the pin data.
            if num_row_elements(list(row.values())) == 0:
                break

            # Get the pin attributes from the cells of the row of data.
            pin = copy.copy(DEFAULT_PIN)
            pin.index = index
            pin.type = ""
            for c, a in list(COLUMN_NAMES.items()):
                try:
                    if c == "name":
                        row[c] = psoc5lp_pin_name_process(row[c])
                    setattr(pin, a, row[c])
                except KeyError:
                    pass
            if pin.num is None:
                issue(
                    "ERROR: No pin number on row {index} of {part_num}".format(
                        index=index, part_num=part_num
                    ),
                    level="error",
                )
            if pin.type == "":
                # No explicit pin type, so infer it from the pin name.
                DEFAULT_PIN_TYPE = (
                    "input"  # Assign this pin type if name inference can't be made.
                )
                PIN_TYPE_PREFIXES = [
                    (r"P[0-9]+\[[0-9]+\]", "bidirectional"),
                    (r"VCC", "power_out"),
                    (r"VDD", "power_in"),
                    (r"VSS", "power_in"),
                    (r"IND", "passive"),
                    (r"VBOOST", "input"),
                    (r"VBAT", "power_in"),
                    (r"XRES", "input"),
                    (r"NC", "no_connect"),
                ]
                for prefix, typ in PIN_TYPE_PREFIXES:
                    if re.match(prefix, pin.name, re.IGNORECASE):
                        pin.type = typ
                        break
                else:
                    issue(
                        "No match for pin {} on part {}, assigning as {}".format(
                            pin.name, part_num, DEFAULT_PIN_TYPE
                        )
                    )
                    pin.type = DEFAULT_PIN_TYPE

            # Add the pin from this row of the CVS file to the pin dictionary.
            # Place all the like-named pins into a list under their common name.
            # We'll unbundle them later, if necessary.
            pin_data[pin.unit][pin.side][pin.name].append(pin)

        yield part_num, part_ref_prefix, part_footprint, part_manf_num, part_datasheet, part_desc, pin_data  # Return the dictionary of pins extracted from the CVS file.
