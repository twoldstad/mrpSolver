import math
import sys

def hypotenuse(a,b):
   result = math.sqrt(a * a + b * b)
   return result

def is_even(x):
   result = x % 2 == 0
   return result

def in_an_interval(x):
   result = 2<= x <9 or 47< x <92 or 12< x <=19 or 101<= x <=103
   return result

def are_positive(input_list):
   output_list = []
   for entry in input_list:
      if entry > 0:
         output_list.append(entry)
   return output_list

def are_greater_than(input_list, n):
   output_list = []
   for entry in input_list:
      if entry > n:
         output_list.append(entry)
   return output_list

def are_in_first_quadrant(input_list):
   output_list = []
   for point in input_list:
      if point.x > 0 and point.y > 0:
         output_list.append(point)
   return output_list

def index_of_smallest(input_list):
   if len(input_list) > 0:
      output = input_list[0]
      output_list = []
      for entry in input_list:
         if entry <= output:
            output = entry
         else:
            output = output
      for i, j in enumerate(input_list):
         if j == output:
            output_list.append(i)
      return output_list
   else:
      return None

def groups_of_3(input_list):
   output_list = [input_list[i:i+3] for i in range(0, len(input_list), 3)]
   return output_list

def for_version(items):
   result = []
   for i in range(len(items) - 1, -1, -1):
      result.append(items[i])
   return result

def str_translate_101(input_str, old, new):
   output_lst = []
   for char in input_str:
      if char == old:
         output_lst.append(new)
      else:
         output_lst.append(char)
   output_str = ''.join(output_lst)
   return output_str

for i, j in enumerate(sys.argv):
   print i, j

def float_default(str, value):
   try:
      result = float(str)
   except:
      result = value
   return result










file_to_open = None
try:
   file_to_open = sys.argv[1]
except:
   print "YA DINGUS! That filename is wrong."
   exit()

fobj = None
try:
   fobj = open(file_to_open, 'r')
except:
   print "YA DINGUS! That file could not be opened."
   exit()

sum=0
for line in fobj:
   x = 0
   y = 0
   try:
      x = line.split()[0]
      y = line.split()[1]
   except:
      print "YA DINGUS! You are missing a number."
      continue
   try:
      total = float(x) + float(y)
      print total
   except:
      print "YA DINGUS! That ain't a number."
      continue







OUTFILE_NAME = "detabbed"
TAB_STOP_SIZE = 8
NUM_ARGS = 2
FILE_ARG_IDX = 1

#Theoodore was here


def main(argv):
   if (len(argv) < NUM_ARGS):
      print >> sys.stderr, "file name missing"
      sys.exit(1)

   try:
      infile = open(argv[FILE_ARG_IDX], "r")
   except IOError as e:
      print >> sys.stderr, e
      sys.exit(1)

   try:
      outfile = open(OUTFILE_NAME, "w")
   except IOError as e:
      print >> sys.stderr, e
      sys.exit(1)

   character_count = 0;

   c = infile.read(1)
   while (c):
      if (c == '\t'):
         num_spaces =  TAB_STOP_SIZE - (character_count % TAB_STOP_SIZE)
         for i in range(num_spaces):
            outfile.write(' ')
         character_count = character_count + num_spaces
      elif (c == '\n'):
         outfile.write('\n')
         character_count = 0
      else:
         outfile.write(c)
         character_count = character_count + 1
      c = infile.read(1)

   infile.close()
   outfile.close()


if __name__ == "__main__":
   main(sys.argv)






fobj = None
try:
   fobj = open(file_to_open, 'r')
except:
   print "YA DINGUS! That file could not be opened."
   exit()

total = 0
for line in fobj:
   x = int(number_of_column)
   y = 0
   try:
      y = line.split()[x]
   except:
      y = 0
      continue
   try:
      total = float(y) + total
   except:
      print "YA DINGUS! That ain't a number."
      continue


