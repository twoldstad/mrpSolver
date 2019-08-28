import sys
import os.path
import csv
import re
import textwrap

class part:
   def __init__(self, name, oh, alloc, ss, lt, ls):
      self.name = name
      self.oh = oh
      self.alloc = alloc
      self.ss = ss
      self.lt = lt
      self.ls = ls
      self.sr = {}
      self.bom = {}
      self.mps = {}
      self.mrp = []
      self.avl = []
      self.prnt = 0
      self.queued = False
      self.next = next

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
         and self.avl == other.avl
         and self.prnt == other.prnt
         and self.queued == other.queued
         and self.next == other.next
      )

   def __hash__(self):
      return hash((self.name))

   def __repr__(self):
      return ("part({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r},{!r}, {!r})".format(self.name, self.oh, self.alloc, self.ss, self.lt, self.ls, self.sr, self.bom, self.mps, self.mrp, self.avl, self.prnt, self.queued))

class Queue:
   def __init__(self):
      self.front = None
      self.rear = None
      self.num_items = 0

   def __eq__(self, other):
      return ((type(other) == Queue)
         and self.capacity == other.capacity
         and self.front == other.front
      )

   def __repr__(self, other):
      return ("Queue({!r}, {!r})".format(self.capacity, self.front))

   def is_empty(self):
      return self.num_items == 0

   def add(self, item):
      if self.is_empty():
         self.front = item
      else:
         self.rear.next = item
      self.rear = item
      self.num_items += 1

   def get(self):
      item = self.front
      if self.num_items > 1:
         self.front = self.front.next
      else:
         self.front = None
         self.rear = None
      self.num_items -= 1
      return item

def input_message(doc):
   fle = input('Please enter the name of the ' + doc + ' file you would like to use (csv files only): ')
   return fle

def imf_input():
   doc = input_message('IMF')
   if doc == 'demo':
      doc = os.path.join('sample', 'sample_imf.csv')
   with open(doc) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      skip = next(csv_)
      for line in csv_:
         line = [e.strip() for e in line]
         prt = part(str(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]))
         try:
            sr = re.split('[: ]', line[6])
            sr = [int(e) for e in sr]
            prt.sr = dict(zip(sr[0::2], sr[1::2]))
         except ValueError:
            pass
         all_parts.append(prt)
         part_names[prt.name] = prt

def mps_input():
   global num_periods
   doc = input_message('MPS')
   if doc == 'demo':
      doc = os.path.join('sample', 'sample_mps.csv')
   with open(doc) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      header = next(csv_)
      header = [e.strip() for e in header]
      periods = [int(e) for e in header[1::]]
      num_periods = max(periods)
      mn = min(periods)
      if mn <= 0:
         neg = 1 - mn
      for line in csv_:
         line = [e.strip() for e in line]
         prt = part_names[line[0]]
         prt.mps = dict(zip(periods, [int(e) for e in line[1:]]))

def bom_input():
   doc = input_message('BOM')
   if doc == 'demo':
      doc = os.path.join('sample', 'sample_bom.csv')
   with open(doc) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      skip = next(csv_)
      for line in csv_:
         line = [e.strip() for e in line]
         if len(line) == 2:
            chldrn = re.split('[: ]', line[1])
            ch_names = [str(e) for e in chldrn[0::2]]
            ch_qt = [int(e) for e in chldrn[1::2]]
            parent = part_names[line[0]]
            for i, name in enumerate(ch_names):
               chld = part_names[name]
               chld.prnt += 1
               parent.bom[chld] = ch_qt[i]

def draw_bom(part, level):
   for child, qt in part.bom.items():
      print(' '+level*'|   '+'|- '+child.name+' ('+str(qt)+')')
      draw_bom(child, level +1)

def solver():
   global all_parts
   global top_level
   global part_names
   global current_level
   global num_periods
   global neg

   imf_input()
   mps_input()
   bom_input()

   for part in all_parts:
      if part.prnt == 0:
         top_level.append(part)
         current_level.add(part)

   while not current_level.is_empty():
      current_part = current_level.get()
      if current_part.prnt == 0:
         for child in current_part.bom:
            child.prnt -= 1
            if not child.queued:
               current_level.add(child)
               child.queued = True
         # run calculations on current part
         need_lst = [0] * (num_periods + neg)
         release_lst = need_lst[::]
         avail_lst = need_lst[::]
         avail = 0
         first_add = False
         # go through demand for part and add to list that accounts for negative periods
         for period, qt in current_part.mps.items():
            need_lst[int(period) + neg - 1] = qt
         # go through list of demand for part while maintaining correct period references
         for per, qt in enumerate(need_lst, start=(1-neg)):
            i_per = per + neg - 1
            avail += current_part.sr.get(per, 0)
            if per > 0 and first_add is False:
                  avail += current_part.oh - current_part.alloc
                  first_add = True
            if qt > 0:
               leftover = avail - qt
               if leftover < current_part.ss:
                  when = per - current_part.lt
                  i_when = when + neg - 1  
                  if 1 - when > neg:
                     new_neg = 1 - when
                     neg_dif = new_neg - neg
                     release_lst = [0]*neg_dif + release_lst
                     need_lst = [0]*neg_dif + need_lst
                     avail_lst = [0]*neg_dif + avail_lst
                     i_per += neg_dif
                     i_when += neg_dif
                     neg = new_neg
                  if per > 0:
                     short = current_part.ss - leftover
                     buy = (short // current_part.ls + (short % current_part.ls > 0)) * current_part.ls
                  else:
                     buy = qt
                  avail += buy
                  release_lst[i_when] += buy
                  for child, amount in current_part.bom.items():
                     child.mps[when] = amount*buy + child.mps.get(when, 0)
               avail -= qt
            avail_lst[i_per] = avail
         current_part.mrp = release_lst
         current_part.avl = avail_lst
      else:
         current_level.add(current_part)

title = 'mrpSolver'
subtitle = 'By Teddy Woldstad'
space = len(subtitle) + 2
opening = 'In order to calculate a material resource planning (MRP) order-release schedule, an item master file (IMF), manufacturing production schedule (MPS), and bill of materials (BOM) is required. Please check the example files provided for correct formatting. NOTE: This program is designed to account for available materials from the present time period. A correct MPS should not incur past-due or late orders. However, this program will still consider such orders and will report them without applying presently available resources. As such, material quantities needed in the past will be reported in exact quantities without regard to lot sizes and will not impact future available quantities.'
b_table_title = 'Indented BOM'
a_table_title = 'Available Quantities Per Time Period'
m_table_title = 'MRP Order-Release Schedule'
print((title.center(space)).center(100, '#')+'\n')
print(subtitle.center(100)+'\n\n')
print(textwrap.fill(opening, 100)+'\n')

all_parts = []
top_level = []
part_names = {}
current_level = Queue()
num_periods = 0
neg = 0
notes = []

solver()

total_periods = num_periods + neg
for part in all_parts:
   if len(part.mrp) < total_periods:
      part.mrp = [0] * (total_periods - len(part.mrp)) + part.mrp
   if len(part.avl) < total_periods:
      part.avl = [0] * (total_periods - len(part.avl)) + part.avl

print(' Result '.center(100, '-')+'\n\n')
print(b_table_title+'\n')
for part in top_level:
   print(part.name)
   draw_bom(part, 0)

cols = list(range(1-neg, num_periods+1))
top_row = '{:10s}'.format('Part')+''.join('{:^6d}'.format(e) for e in cols)
top_width = 10 + 6*len(cols)

print('\n\n'+a_table_title.center(top_width)+'\n')
print(top_row)
print('-' * top_width)
for part in all_parts:
   print('{:10s}'.format(part.name)+''.join('{:^6d}'.format(e) for e in part.avl))

print('\n\n'+m_table_title.center(top_width)+'\n')
print(top_row)
print('-' * top_width)
for part in all_parts:
   print('{:10s}'.format(part.name)+''.join('{:^6d}'.format(e) for e in part.mrp))

if not notes:
   print('\nDone.\n')
else:
   print('\nNotes:')
   print(notes)
