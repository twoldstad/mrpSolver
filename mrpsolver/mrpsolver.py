import os
import re
import csv
import json
from collections import deque
from dataclasses import dataclass, field
from typing import Any, List
from pathlib import Path


@dataclass
class Part:
   id: str        # unique part identifier
   oh: float      # on hand
   alloc: float   # allocated
   ss: float      # safey stock
   lt: float      # lead time
   ls: float      # lot size
   scrap: float = None   # percentage of component/assembly expected to be scrapped, represented as a decimal; 1.2% -> 0.012
   name: str = None     # descriptive part name (does not affect calculations)
   desc: str = None      # part description (does not affect calculations)
   sr: dict = field(default_factory=dict)         # scheduled receipt
   bom: dict = field(default_factory=dict)        # bill of materials
   mps: dict = field(default_factory=dict)        # manufacturing production schedule -> [time period]:[quantity]
   mrp: dict = field(default_factory=dict)        # order release schedule
   avail: dict = field(default_factory=dict)      # available per time period
   parents: List['Part'] = field(default_factory=list)    # all parent components
   rem_parents: int = 0 # total remaining parents to be processed
   queued: bool = False

   def __post_init__(self):
      """ A little bit of data cleaning/reformatting when parts are initiated manually """
      self.sr_clean_keys()
      self.bom_clean_keys()
      self.mps_clean_keys()
   
   def sr_clean_keys(self):
      self.sr = {k: float(v) for k, v in self.sr.items() if v}

   def bom_clean_keys(self):
      self.bom = {k: float(v) for k, v in self.bom.items() if v}

   def mps_clean_keys(self):
      self.mps = {k: float(v) for k, v in self.mps.items() if v}


class Solver:
   def __init__(self, allow_negative=False):
      self.allow_negative = allow_negative   # bool, if negative/past periods are considered valid, functionality not yet implemented
      self.all_parts = {}           # Dict{Part.id, Part}
      self.orphans = []             # List[Part], parts with no parents
      self.min_period = 1           # int
      self.max_period = 1           # int
      self.current_level = deque()

   def __eq__(self, other):
      return ((type(other) == Solver)
         and self.allow_negative == other.allow_negative
         and self.all_parts == other.all_parts
         and self.orphans == other.orphans
         and self.min_period == other.min_period
         and self.max_period == other.max_period
         and self.current_level == other.current_level
      )

   def __repr__(self) -> str:
      return ("Solver(allow_negative= {!r}, all_parts= {!r}, orphans= {!r}, min_period= {!r}, max_period= {!r}, current_level= {!r})".format(self.allow_negative, self.all_parts, self.orphans, self.min_period, self.max_period, self.current_level))

   def total_periods(self) -> int:
      return self.max_period - self.min_period + 1

   def negative_periods(self) -> bool:
      return self.min_period <= 0   # a "0" period is considered negative
   
   def load_imf(self, file: os.PathLike) -> None:
      if file.suffix == '.json':
         imf_from_json(self, file)
      elif file.suffix == '.csv':
         imf_from_csv(self, file)
      else:
         raise Exception

   def load_mps(self, file: os.PathLike, listed_by: str) -> None:
      if file.suffix == '.json':
         if not listed_by:
            raise Exception
         mps_from_json(self, file, listed_by)
      elif file.suffix == '.csv':
         mps_from_csv(self, file)
      else:
         raise Exception       

   def load_bom(self, file: os.PathLike) -> None:
      if file.suffix == '.json':
         bom_from_json(self, file)
      elif file.suffix == '.csv':
         bom_from_csv(self, file)
      else:
         raise Exception         # work on this
 
   def orphan_check(self) -> None:
      """ used when building the initial list and possibly when a part is updated? TBD """
      for part in self.all_parts.values():
         part.queued = False
         if part.rem_parents == 0:
            self.orphans.append(part)
            self.current_level.append(part)
            part.queued = True

   def process_part(self, part: Part) -> None:
      for child_id in part.bom.keys():
         child = self.all_parts[child_id]
         child.rem_parents -= 1
         if child.rem_parents == 0 and not child.queued:
            self.current_level.append(child)
            child.queued = True
      available = 0
      for period in range(self.min_period, self.max_period+1):
         if period == 1:      # assumes period "1" is the present next period
            available += part.oh
            available -= part.alloc
         available += part.sr.get(period, 0.0)
         needed_qt = part.mps.get(period, 0.0)
         if needed_qt:
            leftover = available - needed_qt
            if leftover < part.ss:
               when_needed = period - part.lt
               if when_needed < self.min_period:
                  self.min_per = when_needed
                  # self.negative_periods_check()
               if period > 0 or self.allow_negative is True: # need to revisit / expand this
                  short = part.ss - leftover
                  order = (short // part.ls + (short % part.ls > 0)) * part.ls
                  part.mrp[when_needed] = order
                  available += order
                  for child_id, amount in part.bom.items():
                     child = self.all_parts[child_id]
                     child.mps[when_needed] = amount * order + child.mps.get(when_needed, 0)
               # else:
               #    order = needed_qt          # need to revisit / expand this
               # available += order
            available -= needed_qt
         part.avail[period] = available
      


   def solve(self) -> tuple[dict, dict]:
      """ Processes all parts and calculates the MRP order release schedule and ATP schedule """
      mrp = {}
      now_available = {}
      if not self.all_parts:
         raise ValueError("There are no parts. Please import an IMF file.")
      self.orphan_check()
      if not self.orphans:
         raise ValueError("There are no independent parent parts. Please import valid IMF and BOM files.")
      while self.current_level:         
         current_part = self.current_level.popleft()
         self.process_part(current_part)
      for id, part in self.all_parts.items():
         mrp[id] = mrp_to_list(part, self)
         now_available[id] = avail_to_list(part, self)
      return mrp, now_available


def imf_from_json(solver: Solver, json_file: str) -> None:
   """ Processes an IMF file from a json file. File format should match the sample file -> sample_imf.json """
   with open(json_file, "r") as file_:
      data = json.load(file_)
      for item in data:
         new_part = Part(
            id = str(item['partID']),
            name = str(item.get('name')) if item.get('name') else None,                # optional parameter
            desc = str(item.get('description')) if item.get('description') else None,  # optional parameter
            oh = int(item['onHand']),
            alloc = int(item['allocated']),
            ss = int(item['safetyStock']),
            lt = int(item['leadTime']),
            ls = int(item['lotSize']),
            sr = {receipt['period']:receipt['quantity'] for receipt in item['scheduledReceipt'] if receipt['quantity'] > 0}
         )
         solver.all_parts[new_part.id] = new_part

def imf_from_csv(solver: Solver, csv_file: str) -> None:
   """ Processes an IMF file from a csv file. File format should match the sample file -> sample_imf.csv """
   correct_headers = dict.fromkeys(['part_id', 'name', 'desc', 'oh', 'alloc', 'ss', 'lt', 'ls', 'sr'])    # Input file must contain these headers
   with open(csv_file) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      headers = [e.strip() for e in next(csv_)]
      for i, header in enumerate(headers):
         if header in correct_headers:
            correct_headers[header] = i   # for ensuring that each column is processed correctly based on its header
      if any(column is None for column in correct_headers.values()):
         raise ValueError("IMF file does not contain all expected header values.")
      for line in csv_:
         line = [e.strip() for e in line]
         new_part = Part(
            id = str(line[correct_headers['part_id']]),
            name = str(line[correct_headers['name']]) if line[correct_headers['name']] else None,
            desc = str(line[correct_headers['desc']]) if line[correct_headers['desc']] else None,
            oh = int(line[correct_headers['oh']]),
            alloc = int(line[correct_headers['alloc']]),
            ss = int(line[correct_headers['ss']]),
            lt = int(line[correct_headers['lt']]),
            ls = int(line[correct_headers['ls']])
         )
         try:
            sr = re.split('[: ]', line[correct_headers['sr']])
            dirty_dict = dict(zip(sr[0::2], sr[1::2]))
            new_part.sr = {int(k): float(v) for k, v in dirty_dict.items() if v}
         except ValueError:
            pass
         solver.all_parts[new_part.id] = new_part

def mps_from_json(solver: Solver, json_file: str, listed_by: str) -> None:
   """ Processes an MPS file from a json file. File format should match the sample file -> sample_mps_by_part.json
         Can be listed by part number or by period """
   with open(json_file, "r") as file_:
      data = json.load(file_)
      periods = set()
      if listed_by == 'period':
         for period in data:
            per = str(period['period'])
            valid_per = False
            for item in period['demand']:
               prt = solver.all_parts[str(item['partID'])]
               qt = float(item['quantity'])
               if qt > 0:
                  prt.mps[per] = qt
                  valid_per = True
            if valid_per:
               periods.add(per)                          # check if numeric
      if listed_by == 'part':
         for part in data:
               prt = solver.all_parts[str(part['partID'])]
               for period in part['demand']:
                  per, qt = period['period'], float(period['quantity'])
                  if qt > 0:
                     prt.mps[per] = qt
                     periods.add(per)
      if not periods:
         raise ValueError("No periods specified in provided MPS file.")
      solver.min_period = min(periods) if min(periods) < 1 else 1
      solver.max_period = max(periods)

def mps_from_csv(solver: Solver, csv_file: str) -> None:
   """ Processes an MPS file from a csv file. File format should match the sample file -> sample_mps.csv """
   periods = set()
   with open(csv_file) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      header = next(csv_)
      header = [e.strip() for e in header]
      try:
         period_list = [int(e) for e in header[1::]]
      except:
         raise ValueError("MPS period headers not numerical.")
      if not period_list:
         raise ValueError("No periods specified in provided MPS file.")
      for line in csv_:
         line = [e.strip() for e in line]
         prt = solver.all_parts[line[0]]
         dirty_dict = dict(zip(period_list, [int(e) for e in line[1:]]))
         prt.mps = {k: float(v) for k, v in dirty_dict.items() if v}
         periods.update(prt.mps.keys())
      solver.min_period = min(periods) if min(periods) < 1 else 1
      solver.max_period = max(periods)

def bom_from_json(solver: Solver, json_file: str) -> None:
   """ Processes BOM from a json file. File format should match the sample file -> sample_bom.json """
   with open(json_file, "r") as file_:
      data = json.load(file_)
      for part in data:
         p_id = part['partID'] 
         parent = solver.all_parts[p_id]
         for child in part['children']:
               c_id = child['partID']
               kid = solver.all_parts[c_id]
               kid.rem_parents += 1
               kid.parents.append(parent)
               parent.bom[c_id] = float(child['quantity'])

def bom_from_csv(solver: Solver, csv_file: str) -> None:
   """ Processes BOM from a csv file. File format should match the sample file -> sample_bom.csv """
   with open(csv_file) as file_:
      csv_ = csv.reader(file_, delimiter=',')
      header = next(csv_)
      for line in csv_:
         line = [e.strip() for e in line]
         if len(line) == 2:
            chldrn = re.split('[: ]', line[1])
            ch_names = [str(e) for e in chldrn[0::2]]
            ch_qt = [float(e) for e in chldrn[1::2]]
            parent = solver.all_parts[line[0]]
            for i, c_id in enumerate(ch_names):
               kid = solver.all_parts[c_id]
               kid.rem_parents += 1
               kid.parents.append(parent)
               parent.bom[c_id] = ch_qt[i]

def mrp_to_list(part: Part, solver: Solver) -> list:
   mrp_lst = []
   for period in range(solver.min_period, solver.max_period+1):
      qt = part.mrp.get(period, 0.0)
      mrp_lst.append(qt)
   return mrp_lst

def avail_to_list(part: Part, solver: Solver) -> list:
   avail_lst = []
   for period in range(solver.min_period, solver.max_period+1):
      qt = part.avail.get(period, 0.0)
      avail_lst.append(qt)
   return avail_lst

def parts_affected(part):
   """ recursive function for determining all parent components affected by the unavailability of a lower component """
   affected = {}
   for parent in part.parents:
      affected += parts_affected(parent)
   return affected + part      
