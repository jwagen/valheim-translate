import csv
import polib
import argparse
import os
import io


class TranslateStr:
    def __init__(self, key, english, other_lang):
        self.key = key
        self.english = english
        self.other_lang = other_lang


def find_csv_in_assets(data):
    loc_start = data.find(b"localization\x93")

    csv_start = data.find(b" ", loc_start) -1
    csv_end = data.find(b"\x00\x07\x00\x00", csv_start) -1

    return (csv_start, csv_end)

def extract_csv(path):
    #valheim_path = r"D:\SteamLibrary\steamapps\common\Valheim\valheim_Data"
    assset_filename = os.path.join(path, "resources.assets")

    #output_file = "out.csv"

    data = ""
    with open(assset_filename, 'rb') as f:
        data = f.read()


    (csv_start, csv_end) = find_csv_in_assets(data)

    print(csv_start)
    print(csv_end)

    csv_text = data[csv_start:csv_end].decode("utf-8").split("\n")



    return csv.reader(csv_text)

def extract_strings(path):
    csv_data = extract_csv(path)

    s = []
    for l in csv_data:
        s.append(TranslateStr(l[0], l[1], l[13]))

    return s

    #with open(output_file, "w", encoding="utf-8", newline="") as f:
    #    w = csv.writer(f, quotechar='\"', quoting=csv.QUOTE_ALL)
    #    for l in csv_data:
    #        w.writerow( (l[0], l[1], l[13], "") )



# Create input arguments
parser = argparse.ArgumentParser()
parser.add_argument("resource", help="Path to resources.assets")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--extract","-e", type=str, help="output .po file")
group.add_argument("--patch", "-p", type=str, help="Pach sassets with .po")
args = parser.parse_args()



if args.extract:
    strings = extract_strings(args.resource)
    po = polib.POFile()
    for s in strings:
        if s.english not in [x.msgid for x in po]:
            entry = polib.POEntry(
                msgid=s.english,
                comment=s.key,
                msgstr=s.other_lang
            )
            po.append(entry)


    po.save(args.extract)

elif args.patch:
    # Read po file
    po = polib.pofile(args.patch)
    print(po)

    strings = []
    for t in po:
        s = TranslateStr(t.comment, t.msgid, t.msgstr)
        print(f"{s.key}, {s.english}, {s.other_lang}")
        strings.append(s)
    
    csv_data = extract_csv(args.resource)
    csv_out_mem_file = io.StringIO()
    csv_out_writer = csv.writer(csv_out_mem_file)
    for s in strings:
        print(r"s.english {}",s.key)

        for r in csv_data:
            print(f"row[0] = {r[0]}")
            if r[1] == s.english:
                r.append(s.other_lang)
                print(r)
                csv_out_writer.writerows(r)
    
    #print(csv_out_mem_file.getvalue())
            
                


#print(csv_data)

#new_csv = ""
#for l in csv_data:
#    print(l)