__author__ = 'xiaxuan'

file = open('../count.txt', 'r+')
str = file.readline()
if str == '':
    print "is null"
    str = '111'
    file.write(str)
else:
    str = '2345678'
    file.write(str)
file.close()