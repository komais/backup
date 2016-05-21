#! /usr/bin/env python3
import argparse
import sys
import os
import re
bindir = os.path.abspath(os.path.dirname(__file__))
import sqlite3
import collections
import time



__author__='Liu Tao'
__mail__= 'taoliu@annoroad.com'

pat1=re.compile('^\s+$')

class Project():
	def __init__(self , tmp ):
		self.report_id = tmp[0]
		self.project_type = tmp[1]
		self.project_dalei = tmp[2]
		self.project_xifen = tmp[3]
		self.contract_id = tmp[4]
		self.sub_project = tmp[5]
		self.name = tmp[6]
		self.person = tmp[7]
		self.start = remove_bad_format_date ( tmp[8] )
		self.end = remove_bad_format_date ( tmp[9] )
		self.cost = tmp[10]
		self.finish = remove_bad_format_date ( tmp[11] )
		self.delay = tmp[12]
		self.delay_cause = tmp[13]
		self.checker = tmp[14]
		self.pass_check = tmp[15]
		self.pass_pm = tmp[16]
		self.pass_qc = tmp[17]
		self.submit_table = tmp[18]
		self.dir_quota = tmp[19]
		self.analysis_dir = tmp[20]
		self.sequence_finish = remove_bad_format_date ( tmp[21] )
		self.seq_finish_date = remove_bad_format_date ( tmp[22] )
		self.state = tmp[23]
		self.information_table_date = remove_bad_format_date ( tmp[24] )
		self.gannt_write_date = remove_bad_format_date( tmp[25] ) 
	def __str__(self ):
		return "\t".join([self.report_id , self.project_type , self.project_dalei, self.project_xifen , self.contract_id , self.sub_project , self.name , self.person , format_date(self.start) , format_date(self.end) , self.cost , format_date(self.finish) , self.delay, self.delay_cause , self.checker , self.pass_check  , self.pass_pm , self.pass_qc , self.submit_table , self.dir_quota , self.analysis_dir , self.sequence_finish , format_date(self.seq_finish_date) ,self.state , format_date(self.information_table_date) , format_date(self.gannt_write_date)]) + "\n"

def format_date(day):
	day = day.strip()
	if day == '' or day == 'False End Date!' or day== '###############################################################################################################################################################################################################################################################':
		return ''
	else :
		return time.strftime("%Y/%m/%d" , time.strptime( day  , "%Y%m%d") ) 

def remove_bad_format_date(day):
	day = day.replace("-" , "")
	day = day.replace("/" , "")
	return day


def read_project(f_in , f_out):
	all_project = collections.defaultdict()
	conn = sqlite3.connect( f_in )
	tt = [ 'REPORT_ID' , 'PORJECT_TYPE'  ,'PROJECT_DALEI' , 'PROJECT_DETAIL' , 'CONTRACT_ID' ,
			'SUB_PROJECT_ID' , 'MISSION_NAME' , 'DUTYER' , 'MISSION_END_DATE' , 'PROJECT_END_DATE' ,
			'COST' ,  'BACKUP_DATE', 'BOOL_DELAY', 'DELAY_CAUSE' , 'CHECKER' ,
			'PASS_CEHCKER' , 'PASS_PM' , 'PASS_QC' , 'BOOL_CHECK_TABLE' , 'QUOTA' ,
			'PATHWAY' , 'BOOL_SEQ' , 'SEQ_FINISH_DATE' , 'PROJECT_STATE' ,'INFORMATION_TABLE_DATE' , 'GANNT_DATE']
	f_out.write("\t".join(tt) + '\n')
	for tmp in conn.execute('SELECT {0}  FROM PROJECT ; '.format( ",".join(tt))) :
		a_project = Project(tmp)
		f_out.write(a_project.__str__())
	return all_project

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input file',dest='input',default='/annoroad/data1/bakPROJECT/PROJECT/log/backup.db')
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	#parser.add_argument('-m','--mm',help='output file',dest='mm',action='store_false')
	args=parser.parse_args()
	
	all_projects = read_project(args.input, args.output)




if __name__ == '__main__':
	main()
