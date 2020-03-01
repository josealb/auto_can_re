import csv
import os
import numpy as np
from tools.lib.logreader import LogReader
example_segment = "/home/josealb/Downloads/3533c53bb29502d1_2019-12-10--01-13-27--0--rlog.bz2"

lr = LogReader(example_segment)
logs = list(lr)

id_list = []
for entry in logs:
    print("new entry")
    if entry.which() == "can":
        print("new can message")
        for can_message in entry.can:        
            if not can_message.address in id_list:
                id_list.append(can_message.address)

print(id_list)

latest_value = [str(x) for x in np.zeros(len(id_list))]
with open("can.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(id_list)
    for entry in logs:
        print("new entry")
        if entry.which() == "can":
            print("new can message")
            for can_message in entry.can:        
                list_index = id_list.index(can_message.address)
                latest_value[list_index] = can_message.dat
                print(latest_value)
                writer.writerow(latest_value)
            # print("decoding values")
            # decoded_values = [print(x) for x in msgs.values()]
            # print("types")
            # decoded_values = [print(type(x)) for x in msgs.values()]
            # #msgs["timestamp"]=str(lp)
            # decoded_values = [binascii.hexlify(x) for x in msgs.values()]

            # decoded_values = [int(x,16) for x in decoded_values]
            # decoded_values.append(str(lp))
            # print("decoded values")
            # print(decoded_values)
            # writer.writerow(decoded_values)
