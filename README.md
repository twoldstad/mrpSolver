# mrpSolver

Calculate a maufacturing Material Requirements Planning (MRP) order release schedule and Available to Promise (ATP) schedule using item master file, master production schedule, and bill of material information.

## About

In operating a just-in-time (JIT) manufacturing environment, it is essential to have the right quantities of material and finished goods in the exact time they are required. Using the appropriate production data, these quantities can be calculated. The following documents are needed:
+ **Item Master File / IMF:** contains all materials associated with production, including raw materials, parts, assemblies, packaging, etc, and provides corresponding inventory info.
+ **Master Production Schedule / MPS:** lists all end products and present production quantities per time period.
+ **Bill of Materials / BOM:** lists all assemblies and their components/materials with corresponding quantities.

We can then find a suggested MRP release schedule and ATP schedule that reflects present demand and product design.

## Quickstart

Use the `cli_app.py` script to run the mrpSolver with minimal setup. The app requires 3 arguments: an IMF, MPS, and BOM in CSV or JSON file formats. Sample files with the required formatting can be found under `tests/sample_files`. An option to show an indented BOM from the inputted files is also available using a flag, `--show_bom`. To test the sample files, use the following command:

    python3 cli_app.py --imf ./tests/sample_files/sample_imf.json --mps ./tests/sample_files/sample_mps_by_part.json --bom ./tests/sample_files/sample_bom.json --show_bom

The result will show an indented BOM, an ATP schedule, and a MRP order-release schedule.

## Future Improvements

+ Feature to determine which items will be affected by past-due orders
+ Ability to export results as CSV/JSON files
+ Scrap rate functionality for placing more accurate orders
+ Capacity requirements planning (CRP) functionality
