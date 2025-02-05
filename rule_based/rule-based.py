# pandas read from sqlite
from datetime import datetime
import pandas as pd
import sqlite3
import os

os.chdir('../')

conn = sqlite3.connect('instance/flaskr.sqlite')

query = """

SELECT * FROM cif

"""

cif_suspicious=pd.read_sql_query(query, conn)
cif_suspicious=cif_suspicious[(cif_suspicious['email']!=cif_suspicious['old_email']) & (cif_suspicious['old_email'].notnull())]
cif_suspicious['scammerName']=cif_suspicious['firstname']+' '+cif_suspicious['lastname']
cif_suspicious['flagSource']='Rule Based'
cif_suspicious['recordedDate'] = datetime.now().strftime("%Y-%m-%dT%H:%M")
cif_suspicious=cif_suspicious[['scammerName','flagSource','recordedDate','email']]



conn = sqlite3.connect('instance/flaskr.sqlite')

cif_suspicious.to_sql('scammer', conn, if_exists='append', index=False)