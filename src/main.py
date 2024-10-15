import datetime
import os
import sys

import cantools
import parser

# define global
db_name = None
db_dict = {}


def read_dbc(path):
    # global vars
    global db_name
    global db_dict

    # start code
    db_name = os.path.basename(path).split('.')[0]
    print("loading " + db_name + "...")

    # try loading
    try:
        db = cantools.database.load_file(path)
    except cantools.database.errors.Error as e:
        print("unable to parse db, errors in file:")
        print(e)
        sys.exit(1)

    version = db.version
    if version is None:
        version = "NA"
    elif version == "":
        version = "not set"
    print("db version: " + version + "\n")

    for m in db.messages:
        for s in m.senders:
            if s in db_dict:
                db_dict[s].append(m)
            else:
                db_dict[s] = [m]

    for s in db_dict:
        print(str(s) + ":")
        for m in db_dict[s]:
            print("\t" + str(m))
            for sg in m.signals:
                print("\t\t" + str(sg))
            print()

    print("finished loading db\n")


def main():
    name = sys.argv[0]  # unused, for clarity

    # guard against missing argument
    if len(sys.argv) < 2:
        print("Path is missing!")
        sys.exit(1)
    else:
        dbc_path = sys.argv[1]  # put target dbc path here

    # guard against invalid path
    if not os.path.exists(dbc_path):
        print("invalid Path!")
        sys.exit(1)

    read_dbc(dbc_path)
    parser.to_enum_header(db_dict, db_name)
    parser.to_mapping_header(db_dict, db_name)

    print("finished")


if __name__ == '__main__':
    if not __package__:
        # Make CLI runnable from source tree with
        #    python src/package
        package_source_path = os.path.dirname(os.path.dirname(__file__))
        sys.path.insert(0, package_source_path)

    main()
