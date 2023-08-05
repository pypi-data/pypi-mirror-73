import sys
import webbrowser
from parsing import *
from desmos import *
from sequence import Sequence


def main():

    intro = \
      "DesmOEIS\n" \
      "A tool for converting OEIS sequences to Desmos lists.\n" \
      "\n" \
      "Type id=<OEIS id> (without the brackets) to convert a sequence. \n" \
      "Type help for a list of all valid commands. \n" \
      "Type exit to close the application. \n" \

    help = \
        "\nSyntax: (Command Name)=(Argument)\n\n" \
        "id: Attempts to convert an OEIS id argument into a Desmos list. \n" \
        "The \"A\" is optional, and trailing zeros may be excluded.\n\n" \
        \
        "name: Assigns the resulting Desmos list to a variable with the given name. \n" \
        "Names must be exactly one letter character (except \"e\"), no numbers or special characters.\n\n" \
        \
        "trim: Filters a list using Python-style slicing syntax. For A:B:C:\n" \
        "A is the starting index (inclusive), default 0.\n" \
        "B is the ending index (exclusive), default is the list length.\n" \
        "C is a step value that is used to skip every C elements, default is 1 (don't skip anything).\n\n" \
        \
        "ext: Pass Y to this to output the extended version of the OEIS sequence.\n" \
        "WARNING: Passing an entire extended sequence this way is usually not a good idea, as such\n" \
        "sequences can be hundreds of elements long, and can cause your browser to hang. You may want\n" \
        "to combine this with trimming syntax to reduce the number of elements.\n\n" \
        \
        "view: Opens the .html file containing the last converted sequence since starting the program. \n" \
        "Does not work if used before converting a sequence.\n\n" \
        \
        "help: View a list of all valid commands.\n\n" \
        \
        "exit: Closes the application." \

    print(intro)

    file = None

    while True:
        cmd = input()

        if cmd == "help":
            print(help)
            continue

        if cmd == "view":
            if file is None:
                print("No sequence converted yet.")
                continue
            webbrowser.open(f"file://{os.path.realpath(file)}")
            continue

        if cmd == "exit":
            sys.exit()

        # Multiple commands are comma separated
        cmds = cmd.split(', ')
        cmds[-1] = cmds[-1].replace(',', '')

        if not cmds[0].startswith("id"):
            print("First argument must be id.")
            continue

        args = dict()

        for i in cmds:
            i = i.split("=")

            cmd = i[0]
            value = i[1]

            args[cmd] = value

        id = parse_id(args)

        results = find_id(id)

        if results:
            sequence = Sequence(id)
            sequence.args = args
            sequence.results = results
        else:
            print("Invalid id.")
            continue

        sequence.integers = parse_integers(sequence)

        name = sequence.args.get("name")

        if name:
            if len(name) > 1:
                print("Variable names must be one character only.")
                continue

            if str.isdecimal(name) or name == 'e':
                print("Numeric names and the constant e (2.71828...) are not allowed.")
                continue

        sequence.name = name

        file = create_expression(sequence, create_desmos_list)

        print("Sequence converted successfully! \n")


if __name__ == '__main__':
    main()

