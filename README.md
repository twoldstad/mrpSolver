# mrpSolver
Demonstration video soon to be posted.

## About
Use this script to calculate a material resource planning (MRP) order-release schedule. When run, the mrpSolver will ask the user to input an item master file (IMF), manufacturing production schedule (MPS), and bill of materials (BOM) in CSV file format. Please check the example files provided for correct formatting. To test the sample files, simply type "demo" for each of the input questions. For testing your own files, place the files in the same folder as the "main.py" script and include the ".csv" extension when inputting the file names.

Generally, a master production schedule (MPS) should be planned based on available resources and each product's production requirements. This program will not fill past-due orders with presently available resources. Instead, it returns an order-release schedule representing past-due orders in exact quantities (rather than lot size quanities) in the time periods they should have been ordered/produced. This is done in order to allow users the greatest flexibility (e.g. expediting production, etc.).

Note: This project was initially designed to check "by hand" calculations and evolved into a fun side project/personal challenge. I do not recommend directly implementing this into a production environment without significant adjustments.

## Future Improvements
+ Add feature to determine which items will be affected by past-due orders

## Contact
Please visit my LinkedIn profile here: www.linkedin.com/in/teddywoldstad
