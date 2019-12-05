




# 字典排序-根据key
for key in sorted(mydict.keys()):
    print("%s: %s" % (key, mydict[key]))


# 字典排序-根据val
for key, value in sorted(mydict.items(), key=lambda item: item[1]):
    print("%s: %s" % (key, value))

