import requests


def parse_id(args):

    id = args.get("id")

    # Remove the preceding A if included
    id = id.replace('A', '')

    # Add trailing zeros if necessary
    length = len(id)
    if length < 6:
        for i in range(0, 6 - length):
            id = "0" + id

    # Add A at the beginning of the query
    id = 'A' + id

    return id


def find_id(id):

    url = f"https://oeis.org/search?q=id:{id}&fmt=text"
    r = requests.get(url)

    if "No results." in r.text:
        return None

    return r


def parse_integers(sequence):

    text = sequence.results.text

    text = str.splitlines(text)

    rows = []

    if sequence.args.get("ext") == "Y":

        b_id = sequence.id.replace('A', 'b')
        url = f"https://oeis.org/{sequence.id}/{b_id}.txt"
        r = requests.get(url)
        sequence.results = r
        text = r.text
        text = str.splitlines(text)

        for line in text:
            space = line.find(" ")
            row = line[space + 1:]
            row = row.split(', ')
            rows.append(row)

    else:

        for line in text:
            if line.startswith('%S') or line.startswith('%T') or line.startswith('%U'):
                # integers start 11 characters into the line
                row = line[11:]
                row = row.split(',')
                rows.append(row)

    rows = [row for integer in rows for row in integer]

    # Remove empty elements resulting from commas at the end of the %S and %T rows
    rows = list(filter(None, rows))

    trim = sequence.args.get("trim")

    if trim:
        if ":" not in trim:
            print("Trim argument missing colons ( : ).")
            return
        trim = trim.split(":")
        if not (trim[0] is "" or trim[1] is ""):
            for i in trim:
                if i.isdigit() and trim[0] >= trim[1]:
                    print("Start value must be less than the end value.")
                    return
        if trim[0] is "":
            trim[0] = '0'
        if trim[1] is "":
            trim[1] = len(rows)
        for i in trim:
            i = str(i)
            if not i.isdigit():
                print("Invalid input for trim argument.")
                return
        trim = list(map(int, trim))
        start = trim[0]
        end = trim[1]
        if len(trim) == 3:
            if trim[2] is 0:
                print("Step value cannot be zero.")
                return
            step = trim[2]
            rows = rows[start:end:step]
        else:
            rows = rows[start:end]

    return rows
