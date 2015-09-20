# Open a file
fo = open("oo.txt", "a+")
print "Name of the file: ", fo.name

# Assuming file has following 5 lines
# This is 1st line
# This is 2nd line
# This is 3rd line
# This is 4th line
# This is 5th line

str = "This is 6th line"
# Write a line at the end of the file.
#fo.seek(0, 2)
line = fo.write( str +'\n')

# Now read complete file from beginning.
#fo.seek(0,0)
#for index in range(6):
#   line = fo.next()
#   print "Line No %d - %s" % (index, line)

# Close opend file
fo.close()