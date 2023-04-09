import csv
import sys

prodflag = True

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

if prodflag:
    if len(sys.argv) < 2:
        #print('Argument List:', str(sys.argv))
        print("\n\nERROR!! please put fortigate fw config file in parameter\n")
        print("sample\n------")
        print("python3 forticfg2csv fw_cfg_2000-01-02.cfg\n")
        sys.exit(1)

    cfg_filename = sys.argv[1]

else:
    cfg_filename = "FW-A_7-0_0304_202207041420.conf"


with open(cfg_filename, encoding="utf-8") as f:
    lines = f.readlines()

policy_flag = False
policy_order = 0
policy_dict = {}

policy_lists_all = []

for line in lines:
    if "config firewall policy" in line:
        policy_flag = True
        continue
    if policy_flag:
        if "end" in line:
            break
        elif "next" in line:
            policy_dict["order"] = policy_order
            policy_dict["cfg_filename"] = cfg_filename
            policy_lists_all.append(policy_dict)
            policy_dict = {}

            policy_order = policy_order+1
        else:
            strlst = line[:-1].split()
            if "edit" in strlst[0]:
                policy_dict[strlst[0]] = strlst[1]
            else:
                policy_dict[strlst[1]] = str(strlst[2:])


csv_filename = cfg_filename+".csv"
print("export fw policy from : "+cfg_filename)
print("export fw policy to   : "+csv_filename)


with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ["order",
                  "cfg_filename",
                  "edit",
                  "uuid",
                  "status",
                  "srcintf",
                  "dstintf",
                  "srcaddr",
                  "dstaddr",
                  "action",
                  "schedule",
                  "service",
                  "utm-status",
                  "logtraffic",
                  "ips-sensor",
                  "application-list",
                  "profile-protocol-options",
                  "ssl-ssh-profile"]
    writer = csv.DictWriter(
        csvfile, fieldnames=fieldnames, extrasaction='ignore')

    writer.writeheader()  # add header to csv

    for i in policy_lists_all:
        writer.writerow(i)
