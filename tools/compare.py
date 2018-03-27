import sys
import pprint

if (len(sys.argv) < 3):
    print("Usage: python3 compare.py file1 file2")
    sys.exit()

pp = pprint.PrettyPrinter(indent=2)
f1 = sys.argv[1]
f2 = sys.argv[2]
print("Compare %s %s" % (f1, f2))
data1 = eval(open(f1, "r").read())
data2 = eval(open(f2, "r").read())

for k in data1.keys():
    if(k in data2):
        if(data1[k] != data2[k]):
            print("<<")
            pp.pprint(data1[k])
            print(">>")
            pp.pprint(data2[k])
    else:
        print("++%s" % k)

for k in data2.keys():
    if(not k in data1):
        print("--%s" % k)


