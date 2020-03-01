import binascii
import csv
import os
import numpy as np

from tools.lib.logreader import LogReader

#example_segment = "/home/josealb/Downloads/3533c53bb29502d1_2019-12-10--01-13-27--0--rlog.bz2"  # demo
#example_segment = "/home/josealb/Downloads/drive/eb378db0873da597_2020-02-29--11-50-42--0--qlog.bz2"  # turning
#example_segment = "3533c53bb29502d1|2019-12-10--01-13-27"  # remote file, doesn't load
#example_segment = "/home/josealb/Downloads/drive/eb378db0873da597_2020-02-29--11-50-42--0--rlog.bz2"
#example_segment = "/home/josealb/Downloads/f89c604cf653e2bf_2018-09-29--13-46-50.bz2"  # turning
#example_segment = "/home/josealb/Downloads/6fb4948a7ebe670e_2019-11-12--00-35-53.bz2"
#example_segment = "/home/josealb/Downloads/drive/eb378db0873da597_2020-02-29--11-50-42--1--rlog.bz2"
example_segment = "/home/josealb/Downloads/rlog.bz2"

lr = LogReader(example_segment)
logs = list(lr)

id_list = []
for entry in logs:
    if entry.which() == "can":
        for can_message in entry.can:        
            if not can_message.address in id_list:
                id_list.append(can_message.address)

print(f"Found the follwing can ids: {id_list}")

output_file = f"{os.path.basename(example_segment).split()[0]}.csv"
latest_value = [str(x) for x in np.zeros(len(id_list)+1)]
last_timestamp = 0

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    labels = id_list
    labels.append("busTime")
    writer.writerow(labels)
    for entry in logs:
        if entry.which() == "can":
            for can_message in entry.can:        
                list_index = id_list.index(can_message.address)
                hex_string = binascii.hexlify(can_message.dat)
                value = int(hex_string,16)
                latest_value[list_index] = value
                if entry.logMonoTime != last_timestamp:
                    latest_value[-1] = entry.logMonoTime
                    writer.writerow(latest_value)
                    last_timestamp = entry.logMonoTime
print ("finished writing csv")
