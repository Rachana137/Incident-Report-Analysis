import urllib.request
import pandas as pd
import sqlite3

#Download data
def fetchincidents(url):
    import urllib
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    return data



#Extract data
def extractincidents(incident_data):
    import tempfile
    fp = tempfile.TemporaryFile()
    import datetime as dt
    import PyPDF2
    import re
    data=incident_data

    # Write the pdf data to a temp file
    fp.write(data)

    # Set the curser of the file back to the begining
    fp.seek(0)

    # Read the PDF
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    pagecount = pdfReader.getNumPages()

    # Get the first page
    page1 = pdfReader.getPage(0).extractText()


    page1 = re.sub(r'\n+','\n',page1).strip()


    li = list(page1.split("\n"))

    column=li[0:5]
    li = [x for x in li if x not in column]


    rmv_li = ['NORMAN POLICE DEPARTMENT', 'Daily Incident Summary (Public)', '']
    for i in rmv_li:
        try:
            li.remove(i)
        except ValueError:
            pass

    # Now get all the other pages
    pages=[]
    for pagenum in range(1, pagecount):
        p = pdfReader.getPage(pagenum).extractText()
        p = re.sub(r'\n+','\n',p).strip()
        p = list(p.split("\n"))
        pages = pages + p

    list_rows = li + pages
    list_rows = [space for space in list_rows if space.strip()]
    list_rows = list_rows[:-1]

    ori = ['OK0140200','14005','EMSSTAT','14009']
    pagerows=[]
    row=[]

    f=0
    for i in list_rows:
        if list_rows[f] not in ori:
            row.append(list_rows[f])
        if list_rows[f] in ori:
            row.append(list_rows[f])
            pagerows.append(row)
            row=[]
        f=f+1
    f=0
    for i in pagerows:
        if len(pagerows[f])> 5:
            pagerows[f][2]=pagerows[f][2] + pagerows[f][3]
            pagerows[f].remove(pagerows[f][3])    



        f=f+1
    f=0

    for i in pagerows:
        if len(pagerows[f])<3:
            pagerows[f].insert(1,'Nan')
        if len(pagerows[f])<4:
            pagerows[f].insert(2,'Nan')
        if len(pagerows[f])<5:
            pagerows[f].insert(3,'Nan')
        f=f+1
    return pagerows

#Create database
def createdb():

    import sqlite3
    dbase='normanpd.db'
    conn= sqlite3.connect(dbase)

    #Create a table in the database.
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS incidents''')
    cur.execute('''CREATE TABLE incidents(
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
        )''')
    conn.commit()
    conn.close()

    return dbase

#Insert data
def populatedb(db,incidents):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.executemany('''INSERT INTO incidents (incident_time,incident_number,incident_location,nature,incident_ori)
    VALUES (?,?,?,?,?)''',incidents)
    conn.commit()
    cur.execute('''select * from incidents''')
    
def status(db):
    conn= sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''select nature,count(nature) as cnt from incidents group by nature order by cnt DESC ''')
    for a in cur.fetchall():
        print(a[0]+' |',a[1])
    return cur.fetchall()


