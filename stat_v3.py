#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import re
import glob
import sqlite3
bindir = os.path.abspath(os.path.dirname(__file__))

__author__='Liu Tao'
__mail__= 'taoliu@annoroad.com'

pat1=re.compile('^\s+$')

def read_standard(f_in):
	std_dict , add_dict = {} , {}
	conn = sqlite3.connect( f_in ) 
	tt = [ 'REPORT_ID' , 'PORJECT_TYPE'  ,'PROJECT_DALEI' , 'PROJECT_DETAIL' , 'CONTRACT_ID' ,
			'SUB_PROJECT_ID' , 'MISSION_NAME' , 'DUTYER' , 'MISSION_END_DATE' , 'PROJECT_END_DATE' ,
			'COST' ,  'BACKUP_DATE', 'BOOL_DELAY', 'DELAY_CAUSE' , 'CHECKER' ,
			'PASS_CEHCKER' , 'PASS_PM' , 'PASS_QC' , 'BOOL_CHECK_TABLE' , 'QUOTA' ,
			'PATHWAY' , 'BOOL_SEQ' , 'SEQ_FINISH_DATE' , 'PROJECT_STATE' ,'INFORMATION_TABLE_DATE' , 'GANNT_DATE'] 
	for tmp in conn.execute('SELECT {0}  FROM PROJECT ; '.format( ",".join(tt))) :
		code , type , dalei ,  person , checker  = tmp[0] , tmp[1] , tmp[2] ,  tmp[7] , tmp[14]
		report_id = int(code.split('-')[-1])
		if report_id <= 5000 : 
			if not code in std_dict :
				std_dict[code] = [type , dalei , person , checker]
			else:
				print("{0} is repeat".format(code))
		else:
			if not code in add_dict :
				add_dict[code] = [type , dalei , person , checker]
			else:
				print("{0} is repeat".format(code))
	return std_dict , add_dict

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-b','--backup',help='backup  file',dest='back' , default='/annoroad/data1/bakPROJECT/PROJECT/log/backup.db') #required=True)
	parser.add_argument('-d', '--dir', help = 'indir',  dest = 'dir' , nargs = '+' , default=['/annoroad/data1/bakPROJECT/PROJECT/current/'])
	#parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	#parser.add_argument('-m','--mm',help='output file',dest='mm',action='store_false')
	args=parser.parse_args()

	std_dict , add_dict = read_standard(args.back)
	#add_dict = read_addition(args.add)
	
	pat = re.compile('^KJ-DB-\S+?-2016-\d{4}')

	stat = {}
	types = []
	persons = []
	checked = {}
	for a_dir in args.dir :
		for a_project in glob.glob("{0}/KJ-DB*".format(a_dir)):
			project_name = os.path.basename(a_project)
			mm = re.findall(pat , project_name)
		#print(mm)
			if len(mm) == 1 :
				sub_project_id = mm[0]
				if sub_project_id in checked : 
					print(sub_project_id + " backup repeat")
				checked[sub_project_id] = 0 
				if sub_project_id in std_dict :
					type , dalei , person , checker = std_dict[sub_project_id]
					tt = ''
					if type == '商业':
						if dalei == 'Filter':
							tt = '过滤'
						else:
							tt = '分析'
					elif type == '研发':
						tt = '研发'
					elif type == '个性化分析':
						tt = '个性'
					else:
						print('{0} {1} '.format( sub_project_id , person))
					if not tt in stat: stat[tt] = {}
					if not person in stat[tt]:stat[tt][person] = []
					stat[tt][person].append(sub_project_id)
					if not tt in types : types.append(tt)
					if not person in persons : persons.append(person)
				elif sub_project_id in add_dict:
					type , dalei ,  person ,checker = add_dict[sub_project_id] 
					tt = ''
					if type == '商业':
						if dalei == 'Filter':
							tt = '过滤'
						else:
							tt = '分析'
					elif type == '研发':
						tt = '研发'
					elif type == '个性化分析':
						tt = '个性'
					else:
						print('{0} {1} '.format( sub_project_id , person))
					if not tt in stat: stat[tt] = {}
					if not person in stat[tt]:stat[tt][person] = []
					stat[tt][person].append(sub_project_id)
					if not tt in types : types.append(tt)
					if not person in persons : persons.append(person)
				else:
					print('{0} is not in table'.format(sub_project_id))
			else:
				print(mm , project_name)
			#print('{0} is error not in table'.format(sub_project_id))
	output = '#\t' + '\t'.join( sorted(persons)) + "\n"
	if not '总计' in stat :
		stat['总计'] = {}
	for i in sorted(types)+['总计'] :
		output += '{0}\t'.format(i)
		for j in sorted(persons):
			if not j in stat[i]: 
				stat[i][j] = []
			if not j in stat['总计'] :
				stat['总计'][j] = 0
			if i != '总计' :
				stat['总计'][j] += len(stat[i][j])
				output += '{0}\t'.format(len(stat[i][j]))
			else:
				output += '{0}\t'.format(stat[i][j])
		output = output.rstrip() + "\n"

	print(output)


if __name__ == '__main__':
	main()
