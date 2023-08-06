import data_3_6
import data_3_7
import data_3_8

info_36 = data_3_6.info
info_37 = data_3_7.info
info_38 = data_3_8.info

print("<div>")
files = set([])


def print_different(filename, in_36, in_37, in_38):
    # Just tracking changes going forward in time, from
    # one version to the next.
    printed_37 = False
    if in_36 != in_37:
        if filename not in files:
            print("<div class='filename-header'>")
            files.add(filename)
            print(filename)
            print("</div>")
        print("<pre class='highlight friendly-small-pre'>")
        print("3.6:\n", in_36, sep="")
        print("3.7:\n", in_37, sep="")
        printed_37 = True
        print("</pre>")
    if in_37 != in_38:
        if filename not in files:
            print("<div class='filename-header'>")
            files.add(filename)
            print(filename)
            print("</div>")
        print("<pre class='highlight friendly-small-pre'>")
        if not printed_37:
            print("3.7:\n", in_37, sep="")
        print("3.8:\n", in_38, sep="")
        print("</pre>")


for filename in info_36:
    try:
        data_36 = info_36[filename]
        data_37 = info_37[filename]
        data_38 = info_38[filename]
    except KeyError:
        print("<div class='filename-header'>")
        print("entry does not exist in one data file for ", filename)
        print("</div>")
        continue

    print_different(
        filename, data_36["message"], data_37["message"], data_38["message"]
    )
    # Leave the following data out for now as it does not give us anything
    # useful ... so far.
    # print_different(
    #     filename,
    #     data_36["parsing_error_source"],
    #     data_37["parsing_error_source"],
    #     data_38["parsing_error_source"],
    # )
    print_different(filename, data_36["cause"], data_37["cause"], data_38["cause"])

print("</div>")
