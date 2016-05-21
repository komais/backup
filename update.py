import sqlite3

conn = sqlite3.connect('/annoroad/data1/bakPROJECT/PROJECT/log/backup.db')

'''
conn.execute(''CREATE TABLE PROJECT
(ID INT PRIMARY KEY     ,
REPORT_ID           TEXT    NOT NULL,
PORJECT_TYPE        TEXT    ,
PROJECT_DALEI       TEXT    ,
PROJECT_DETAIL      TEXT    ,
CONTRACT_ID         TEXT    ,
SUB_PROJECT_ID      TEXT    ,
MISSION_NAME        TEXT    ,
DUTYER              TEXT    NOT NULL,
MISSION_END_DATE    TEXT    ,
PROJECT_END_DATE    TEXT    ,
COST                TEXT    ,
BACKUP_DATE         TEXT    ,
BOOL_DELAY          TEXT    ,
DELAY_CAUSE         TEXT    ,
CHECKER             TEXT    ,
PASS_CEHCKER        TEXT    ,
PASS_PM             TEXT    ,
PASS_QC             TEXT    ,
BOOL_CHECK_TABLE    TEXT    , 
QUOTA               TEXT    ,
PATHWAY             TEXT    ,
BOOL_SEQ            TEXT    ,
SEQ_FINISH_DATE     TEXT    ,
PROJECT_STATE       TEXT    ,
INFORMATION_TABLE_DATE TEXT , 
GANNT_DATE          TEXT    );'') '''

tt = conn.execute( " select count(*) from PROJECT ; ")
count  = tt.fetchall()[0][0]
count += 1 
with open('tt') as f_in:
	for cc , line in enumerate(f_in):
		tmp = line.strip('\n').split('\t')
		print(tmp)
		tttt = "  ,  ".join([ "'{0}'".format(i) for i in tmp])
		print(" INSERT INTO PROJECT VALUES( {0} , {1}); ".format('' , tttt ))
		conn.execute(" INSERT INTO PROJECT VALUES( {0} , {1}); ".format( count  , tttt ))
		count += 1 
conn.commit()
conn.close()
