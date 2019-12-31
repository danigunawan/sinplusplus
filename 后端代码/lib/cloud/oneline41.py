with open("Gamma1.txt", "r+") as f:
    line = f.readline()
    dots = line.split(',')
    i=1
    f.write("\n")
    for dot in dots:
        i+=1
        new_line = dot+","
        f.write(new_line)
        if i > 41:
            i = 1
            f.write("\n")
    f.flush()