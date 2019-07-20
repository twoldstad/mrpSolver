import sys
import csv
import pandas as pd

class part:
   def __init__(self, name, oh, alloc, ss, lt, ls, sr):
      self.name = name
      self.oh = oh
      self.alloc = alloc
      self.ss = ss
      self.lt = lt
      self.ls = ls
      self.sr = {}
      self.bom = {}
      self.mps = {}
      self.mrp = {}

   def __eq__(self, other):
      return ((type(other) == part)
         and self.name == other.name
         and self.oh == other.oh
         and self.alloc == other.alloc
         and self.ss == other.ss
         and self.lt == other.lt
         and self.ls == other.ls
         and self.sr == other.sr
         and self.bom == other.bom
         and self.mps == other.mps
         and self.mrp == other.mrp
      )

   def __repr__(self):
      return ("part({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})".format(self.name, self.oh, self.allo, self.ss, self.lt, self.ls, self.sr))

def input_message2(doc):
   _file = input('Please enter the name of the ' + doc + ' file you would like to use (csv files only): ')
   return _file

def imf_input:
   doc = input_message2('IMF')
   with open(doc) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      skip = next(csv_)
      for line in csv_:
         prt = part(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
         all_parts.append(prt)
         parts_left.append(prt)

def mps_input:
   doc = input_message2('MPS')
   with open(doc) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      skip = next(csv_)
      for line in csv_:
         for prt in all_parts:
            if prt.name == line[0]
               prt.mps = line[1:]

def bom_input:
   doc = input_message2('BOM')
   with open(doc) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      skip = next(csv_)
      for line in csv_:


all_parts = []
child_lst = []
current_level = []
parts_left = []
finished_parts = []

while parts_left:
   for part in parts_left


for row in imf.itertuples():
   all_parts += row.part
   #parts[x] = {}
   #for col in imf.columns:
      #print imf.loc[row, col]
      #parts[x][col] = imf.at[row,col]
      #print parts[x][col]

'''
'''
for row in bom.itertuples():
   x = row.part
   lst = []
   lst = row.children.replace(":"," ").split()
   for i,j in enumerate(lst):
      if i % 2 == 0:
         child_lst += j
         parts[x][i] = lst[i+1]

#for row in 
#for part in all_parts:  #adds attributes to parts for further period-based calculations
#   part.update({'GR': {}, 'PA': {}})
#   for key in part['children']:
#      child_list += key
#
#for part in all_parts:
#   if part not in child_list:
#      current_level += part

#print current_level


#print A['children']['D']
