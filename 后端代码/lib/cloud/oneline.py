import re
with open("Gamma1.txt", "r+") as f:
    line = f.readline()
    ret = re.match("((\d+,){41})",line)
    print(ret)