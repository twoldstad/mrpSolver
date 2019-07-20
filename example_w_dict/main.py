import pr_structure
from pr_structure import *

child_list = []
current_level = []
fin_parents = []
parts = {}

for part in all_parts:  #adds attributes to parts for further period-based calculations
   part.update({'GR': {}, 'PA': {}})
   for key in part['children']:
      child_list += key

#while len(fin_parents) != len(all_parts):
for part in all_parts:
   if part not in child_list and fin_parents:
      current_level += part

print current_level

print all_parts



print child_list

#print parts

#print A['children']['D']
