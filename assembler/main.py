# The AubLang Assembler
# Version 2
# By Aubrey Fields
# Start date: 10/16/2022
# Main functionality complete: 10/26/2022


import copy
import pre_process
import debug
import assemble
import generate_schematic as schem
import post_process


def main():
    # Get source file (.aub or .txt) and parse it into a list of strings line by line
    source, args = pre_process.get_input()

    # Take the list of strings and translate it into a list of Lines,
    # where a Line object stores the contents of the string, and the
    # line number (the index + 1), this is used later in debugging
    lines = pre_process.construct_lines(source)
    
    # Delete comments, empty lines, whitespace, etc
    clean_lines = pre_process.sanitize(lines)

    # debug() looks for syntax errors, valid arguments, etc and
    # prints an error message if an issue comes up
    debug.debug(clean_lines)

    # Replace labels (variables / jump labels) with their literal addresses
    no_labels = assemble.replace_labels(clean_lines)

    # Check to make sure there arent any arguments left that arent literal addresses
    debug.debug_literal(no_labels)

    # Create a second list of the assembly code for use in postProcess (printing etc)
    assembly = copy.deepcopy(no_labels)

    # Convert to binary, then make sure the binary is valid
    machine_code = assemble.assemble(no_labels)
    debug.debug_machine_code(machine_code)

    # Use the binary to generate a schematic to paste into Minecraft
    schem.bin_to_schem(machine_code)

    # Print a report
    post_process.post_process(args, assembly, machine_code)


main()