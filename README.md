
# CS5293SP22-Project0
### Author: RACHANA VELLAMPALLI
### EMAIL: rachana@ou.edu

In the Project0, trying to extract information from the PDF file and insert it into a SQLITE database named 'normanpd.db'.
The PDF file is cleaned using python and the data is formated into list of rows.

## Data
The Norman, Oklahoma police department regularly reports incidents, arrests, and other activities. This data is hosted on [their website](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports) which is distributed to the public in the form of PDF files.
The project is about building a function which uses only incidents pdf.

Example [incident PDF](https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-01_daily_incident_summary.pdf).

## Packages Required 
```bash
pipenv install pandas
pipenv install PyPDF2    
pipenv install pytest  
pip install urllib3
import PyPDF2
import urllib
import pandas
import sqlite3
import re
import pytest
```
# Project0/main.py
main.py contains the call functions for each functionality.
 - p.fetchincidents(url)
 - p.extractincidents(incident_data)
 - p.createdb()
 - p.populatedb(db, incidents)
 - p.status(db)
 main.py is executed by following command in SSH.
 
```bash
  pipenv run python project0/main.py --incidents <url>
```
By giving url of any certain incident file, it should
 download the data and insert it into a database
  and print a summary of the incidents.
## Project0/project0.py 

The p0.py file contains functions to download PDF,
 extract data, create a database, insert data into database
  and retrieve nature of incidents by its occurance. 
  
1. To download data **fetchincidents(url)** 
This function takes a URL string and
 uses the Python urllib.request library to grab one incident
  pdf for the
   [norman police report webpage](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports).

2. To extract data **extractincidents(incident_data)** 
This function takes data from a pdf file and extracts the raw data
and stores it in a list.
 ### steps to extract data
  - With PyPDF2 extract Pdf file to a raw data
  ```bash
  fp = tempfile.TemporaryFile()
  fp.write(data)
  fp.seek(0)
  pdfReader = PyPDF2.pdf.PdfFileReader(fp)
  page1 = = pdfReader.getPage(0).extractText()
  ```
  The PdfFileReader function of the PyPDF2 package retrieves the data.
  The data obtained is in string format and contains excess data which
  is not required.
  - Splitting and removing unnecessary data. 
  ```bash
  page1 = re.sub(r'\n+','\n',page1).strip()
  ```
  After splitting the data, In page 1 headers ('NORMAN POLICE DEPARTMENT', 'Daily Incident Summary (Public)')
  will be removed from the list and then add it to the list which contains other pages.
  From the list which contains all pages last value will be removed using slicing as it is not in the table.
  ```bash
  list_rows = li + pages
  list_rows = [space for space in list_rows if space.strip()]
  list_rows = list_rows[:-1]
  ```
  - Creating sublist in a list for rows.
   Incident ORI column having only 4 values ('OK0140200',
  '14005', 'EMSSTAT', '14009') used to detect end of row.
   
  ```bash
   ori = ['OK0140200','14005','EMSSTAT','14009']
     f=0 #flag=0
    for i in list_rows:
        if list_rows[f] not in ori:
            row.append(list_rows[f])
        if list_rows[f] in ori:
            row.append(list_rows[f])
            pagerows.append(row)
            row=[]
        f=f+1
  ``` 
  Now, In each row there may be more than 5 values since in the pdf
  location address is large it is new line. So, After splitting data 
  with newlines /n+ it is stored as a separate value. So we concatenate 
  the location address as one.
  ```bash
   f=0 #flag
    for i in pagerows:
        if len(pagerows[f])> 5:
            pagerows[f][2]=pagerows[f][2] + pagerows[f][3]
            pagerows[f].remove(pagerows[f][3])    
        f=f+1
  ``` 
- Handling Missing values.
Assuming only Location or nature of incidents will be missing. Inserting
Nan value in that position.
```bash
  f=0
  for i in pagerows:
      if len(pagerows[f])<3:
          pagerows[f].insert(1,'Nan')
      if len(pagerows[f])<4:
          pagerows[f].insert(2,'Nan')
      if len(pagerows[f])<5:
          pagerows[f].insert(3,'Nan')
      f=f+1
```  
The list of rows will be created. 

3. Create Database **createdb()**
A database named **normanpd.db** is created using the function createdb().
The sqlite3 will open the connection creating normanpd.db database.
The incidents will be created in the database using the cursor and execute functions.
```bash
cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS incidents''')
    cur.execute('''CREATE TABLE incidents(
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
        )''')
```
4. Insert data **populatedb(db,incidents)**
The function populatedb(db, incidents) takes the rows created in the extractincidents()
 function and adds it to the normanpd.db database.
 This function opens a connection to the database 'normanpd.db' and
  inserts the rows from the incidents data into the database.
  ```bash
  cur.executemany('''INSERT INTO incidents (incident_time,incident_number,incident_location,nature,incident_ori)
    VALUES (?,?,?,?,?)''',incidents)
    conn.commit()
    cur.execute('''select * from incidents''')
  ```
5. Status print **statusdb()**
  This function returns the query
   of the nature of incidents and the number of
    times they have occurred from the database 'normanpd.db'.
  ```bash
  cur.execute('''select nature,count(nature) as cnt
   from incidents
    group by nature order by cnt DESC ''')
    for a in cur.fetchall():
        print(a[0]+' |',a[1])
  ```






