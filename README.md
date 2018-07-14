
### Code and supplemental files for completion of data engineering task from Applecart
author: Sean Watford

email: smwatford@gmail.com

date: 14 July 2018

Included in this directory:

  * political_data_vendor.csv: provided by Applecart and unaltered (input for match.py and match.ipynb)
 
  * resume_data_vendor.csv: provided by Applecart and unaltered (input for match.py and match.ipynb)
  
  * match.py: python script that can be run from the commandline
```
 >> python match.py political_data_vendor.csv resume_data_vendor.csv
```

  * match.ipynb: jupyter notebook detailing exploratory steps

These scripts are dependant on the use of python packages pandas and urllib.

Scripts run in < 8min on Ubuntu 16.04 2.0TB Disk 32.0 GB memory (i.e. my home workstation). 

Initially the files were investigated column-by-column to understand any inconsistencies or issues with the corresponding datatypes. For example, were strings all the same case, were any non-numeric characters in numeric fields, were any numeric characters in non-numeric fields, etc (and detailed in "match.ipynb"). Also, the common fields accross both files were identified: "last_name", "first_name", and "city"/"local_region". The column "city" was not present in "resume_data_vendor.csv", but the city was extracted from the "local_region" column as an additional feature to identify matching rows. No numeric fields could easily be used to match rows. Although, use case that could be helpful in identifying incorrect or corrupt rows is the use of "degree_start" and "birth_year", e.g. a person cannot start a degree 16 years before their birth year. Only one, generic method was defined for cleaning and standardizing strings: "clean_name". This method only captures a minimal number of issues with the strings: url-encoded characters, ensures uppercase, replaces 0 with O, removes periods (".") and commas (","). These were only a few things I identified that could be easily fixed, but with more time, more complex scenarios can be accounted for. 

The two files were merged together first by matching last name, then by matching last and first name, and finally an exact match defined as matching last and first name and city. An exact match was defined as a match across all overlapping fields, while an ambiguous match is any match of an overlapping field. I didn't report out the first name matching as I was constrained by my workstation using pandas native methods and hitting a memory wall. The other option would be write out matches to disk but that proves take a long time, O(n^2), to complete. A further option I would consider is using spark as use of distributed datasets would keep me from hitting a memory wall. The reason I didn't use spark for this task is because I haven't set it up on my home workstation. Below is a table summarizing the % overlap across the three types of matching. NOTE: Over 30% of original resume data rows is matched with a unique political data row.  

Filename               | Feature                           | % overlap
:-|:-|:-:
resume_data_vendor.csv | same last name (ambiguous match)                    | 85.29  
resume_data_vendor.csv | same last and first name(ambiguous match)          | 53.12 
resume_data_vendor.csv | same last and first name and city (exact match) | 39.56    
political_data_vendor.csv | same last name (ambiguous match)                    | 85.9     
political_data_vendor.csv | same last and first name (ambiguous match)          | 14.9     
political_data_vendor.csv | same last and first name and city (exact match) | 6.98    

### If I had more time...

I would define standards and specifications for reporting and delivering information that vendors could use. Vendor compliance could dramatically reduce errors and loss of data. I would also define a more robust and generic workflow for importing this information. From previous conversations, Applecart data is structured as a graph in a relational database. I would ensure that an appropriate object relational mapper (ORM) layer is in place to accomade the different types of queries needed to support read/write to the graph. 

I heavily use pandas and other statistical packages day-to-day, but several tools are avaible for rapid invesitgation and scaling up to well-defined workflows to handle any size or point of access of data. Each comes with their limiations (as seen in the example above with hitting memory walls with pandas), but I would idenify and evaluate existing and any new tools that could aid in optimizing extract, transform, and load (ETL) layers. 
