import pytest
from project0 import project0 as p
import sqlite3
url='https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-01_daily_incident_summary.pdf'
dbase='normanpd.db'
def test_fetchincidents():
    data=p.fetchincidents(url)
    assert type(data)==bytes
def test_extractincidents():
    data=p.fetchincidents(url)
    incidents=p.extractincidents(data)
    assert type(incidents)==list
def test_extractincidents1():
    data=p.fetchincidents(url)
    incidents=p.extractincidents(data)
    A=[]
    for i in incidents:
        if len(i)==5:
            continue
        else:
            A=A.append(incidents[i])
    assert len(A)==0
def test_extractincidents1():
    data=p.fetchincidents(url)
    incidents=p.extractincidents(data)
    A=[]
    for i in incidents:
        if len(i)==5:
            continue
        else:
            A=A.append(incidents[i])
    assert len(A)==0
def test_createdb():
    db=p.createdb()
    assert db=='normanpd.db'
def test_populatedb():
    db = p.createdb()
    data=p.fetchincidents(url)
    incidents = p.extractincidents(data)
    p.populatedb(db,incidents)
    sql = sqlite3.connect(dbase)
    cur = sql.cursor()
    cur.execute('''select * from incidents''')
    assert cur.fetchall() is not None
    sql.close()
def test_status():
    db = p.createdb()
    data=p.fetchincidents(url)
    incidents = p.extractincidents(data)
    p.populatedb(db,incidents)
    stat=p.status(db)
    sql = sqlite3.connect(dbase)
    cur = sql.cursor()
    cur.execute('''select nature,count(nature) as cnt from incidents group by nature order by cnt DESC''')
    assert stat is not None
    

