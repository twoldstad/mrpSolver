A = {
   'children': {'B':1, 'C':2, 'D':2}, # All children of part (child:quantity)
   'OH': None, # On Hand
   'ALLO': None, # Allocated
   'SS': None, # Safety Stock
   'LT': 2, # Lead Time
   'LS': 1, # Lot Size
   'SR': {},  # Scheduled Receipt (Period:Amount)
   'PS': {4:10, 6:100, 7:10, 8:10} # Production Schedule
}

B = {
   'children': {'C': 2, 'E': 3},
   'OH': 100,
   'ALLO': None,
   'SS': None,
   'LT': 1,
   'LS': 1,
   'SR': {},  # Period:Amount
   'PS': {}
}

F = {
   'children': {'B': 1, 'D': 1, 'E': 1},
   'OH': None,
   'ALLO': None,
   'SS': None,
   'LT': 1,
   'LS': 1,
   'SR': {},  # Period:Amount
   'PS': {5:20, 6:20, 8:10}
}

D = {
   'children': {},
   'OH': 170,
   'ALLO': 120,
   'SS': None,
   'LT': 1,
   'LS': 160,
   'SR': {1:100},  # Period:Amount
   'PS': {}
}

C = {
   'children': {},
   'OH': 120,
   'ALLO': None,
   'SS': 15,
   'LT': 2,
   'LS': 150,
   'SR': {},  # Period:Amount
   'PS': {1:10, 2:10, 3:10, 4:10, 5:10, 6:10, 7:10, 8:10}
}

E = {
   'children': {},
   'OH': 120,
   'ALLO': None,
   'SS': None,
   'LT': 1,
   'LS': 140,
   'SR': {},  # Period:Amount
   'PS': {}
}

all_parts = [A,B,F,D,C,E]
periods = 8
#print A['children']['D']

