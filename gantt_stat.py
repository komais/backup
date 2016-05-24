#! /usr/bin/env python3
import argparse
import sys
import os
import re
bindir = os.path.abspath(os.path.dirname(__file__))
import sqlite3
import collections
import datetime
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
		self.seq_finish_date = remove_bad_format_date (tmp[22] ) 
		self.state = tmp[23]
		self.information_table_date = remove_bad_format_date ( tmp[24] )
		self.gannt_write_date = remove_bad_format_date (tmp[25] )
	def judge_type(self) :
		if self.project_type == '个性化分析':
			return 'gexinghua'
		elif self.project_type == '研发':
			return 'research'
		elif self.project_type == '商业':
			if self.project_dalei == 'Filter': 
				return 'filter'
			else:
				return 'analysis'
		else:
			if self.project_dalei == 'Filter': 
				return 'filter'
			else:
				return 'unknown'
	def judge_delay(self):
		if self.state == '项目延期':
			return True
		else :
			return False
	def finish_this_week(self , day):
		if self.finish :
			this_week = datetime.datetime.strptime(day , '%Y%m%d').isocalendar()
			finish_week = datetime.datetime.strptime(self.finish , '%Y%m%d').isocalendar()
			if this_week[0] == finish_week[0] and this_week[1] == finish_week[1] :
				return True
			else :
				return False
		else:
			return False
	def finish_next_week(self, day ):
		if self.end :
			this_week = datetime.datetime.strptime(day , '%Y%m%d').isocalendar()
			finish_week = datetime.datetime.strptime(self.end , '%Y%m%d').isocalendar()
			if this_week[0] == finish_week[0] and this_week[1] == finish_week[1] - 1  :
				return True
			else :
				return False
		else:
			return False
	def delay_this_week(self , day ):
		if self.state == '停止':
			return False
		else:
			if self.finish :
				if self.finish_this_week( day ) :
					if self.end :
						if time.strptime( self.finish  , "%Y%m%d") <= time.strptime(self.end , "%Y%m%d") :
							return False
						else :
							return True
					else :
						return False
				else:
					return False
			else:
				if self.end :
					this_week = datetime.datetime.strptime(day , '%Y%m%d').isocalendar()
					end_week = datetime.datetime.strptime(self.end , '%Y%m%d').isocalendar()[1]
					if time.strptime(self.end , "%Y%m%d")   <= time.strptime(day  , "%Y%m%d")  :
						return True
					else : 
						if this_week == end_week :
							return 'yet finish'
				else :
					return False
	def __str__(self):
		return '|'.join([self.report_id , self.project_type , self.project_dalei , self.project_xifen, self.sub_project , 
			             self.name , self.person , self.start , self.end,
			              self.finish    , self.delay ,       self.delay_cause        , self.sequence_finish ,
						  self.seq_finish_date        ,       self.state, self.information_table_date , self.gannt_write_date]) + "\n"
	def delay_type(self):
		if  self.sequence_finish :
			if self.sequence_finish == '否': 
				if self.project_type == '商业' or self.project_dalei == 'Filter':
					return 'experiment delay'
				else :
					return 'bioinformatic delay'
			else :
				return 'bioinformatic delay'
		else :
			if self.project_type == '商业' or self.project_dalei == 'Filter':
				return 'experiment delay'
			else :
				return 'bioinformatic delay'
		if self.start and self.seq_finish_date and self.end and self.finish :
			experiment_expect_date = datetime.datetime.strptime( self.start , "%Y%m%d")
			experiment_reality_date = datetime.datetime.strptime( self.seq_finish_date , "%Y%m%d")
			project_expect_date = datetime.datetime.strptime( self.end , "%Y%m%d")
			project_reality_date = datetime.datetime.strptime( self.finish , "%Y%m%d")

			day_delay_info_table = 0
			if self.information_table_date : 
				information_table_date = datetime.datetime.strptime( self.information_table_date, "%Y%m%d")
				day_delay_info_table = information_table_date - experiment_expect_date
				day_delay_info_table = day_delay_info_table.days

			day_delay_experiment = experiment_reality_date - experiment_expect_date
			day_delay_experiment = day_delay_experiment.days
			day_delay_project = project_reality_date - project_expect_date
			day_delay_project = day_delay_project.days
			max_day = max(day_delay_experiment , day_delay_info_table)

			if day_delay_project > max_day :
				return 'bioinformatic delay'
			else:
				if day_delay_experiment > day_delay_info_table :
					return 'experiment delay'
				else :
					return 'infor_table delay'
		else :
			return 'bioinformatic delay' 

def remove_bad_format_date(day):
	day = day.replace("-" , "")
	day = day.replace("/" , "")
	return day

def read_project(f_in):
	all_project = collections.OrderedDict()
	conn = sqlite3.connect( f_in )
	tt = [ 'REPORT_ID' , 'PORJECT_TYPE'  ,'PROJECT_DALEI' , 'PROJECT_DETAIL' , 'CONTRACT_ID' ,
			'SUB_PROJECT_ID' , 'MISSION_NAME' , 'DUTYER' , 'MISSION_END_DATE' , 'PROJECT_END_DATE' ,
			'COST' ,  'BACKUP_DATE', 'BOOL_DELAY', 'DELAY_CAUSE' , 'CHECKER' ,
			'PASS_CEHCKER' , 'PASS_PM' , 'PASS_QC' , 'BOOL_CHECK_TABLE' , 'QUOTA' ,
			'PATHWAY' , 'BOOL_SEQ' , 'SEQ_FINISH_DATE' , 'PROJECT_STATE' ,'INFORMATION_TABLE_DATE' , 'GANNT_DATE']
	for tmp in conn.execute('SELECT {0}  FROM PROJECT ; '.format( ",".join(tt))) :
		a_project = Project(tmp)
		all_project[a_project.report_id] = a_project
	return all_project

def perfect_print(all_dict , f_out , person_dict):
	header = ''
	output = '' 
	for i in (['total' , 'running' , 'finish' , 'finish_this_week' , 'delay' , 'qc' , 'check' , 'pass_check']):
		for j in ([ 'gexinghua' ,   'filter' , 'analysis' , 'research' , 'unknown' , 'all'] ) :
			header += "{0}_{1}\t".format(i , j )
	for person in person_dict:
		output += person + '\t'
		for i in (['total' , 'running' , 'finish' , 'finish_this_week' ,  'delay' , 'qc' , 'check' , 'pass_check']):
			for j in ([ 'gexinghua' ,   'filter' , 'analysis' , 'research' , 'unknown' , 'all'] ) :
				if not person in all_dict[i][j]:
					all_dict[i][j][person] = 0 
				output += '{0}\t'.format(all_dict[i][j][person])
		output = output.rstrip() + '\n'
	header = header.rstrip() + '\n'
	f_out.write('#\t'+ header + output)

def read_person_list():
	infile = '{0}/person.list'.format(bindir)
	person_dict = {}
	with open(infile)  as f_in :
		for line in f_in :
			if line.startswith('#') or re.search(pat1,line):continue
			tmp = line.rstrip().split()
			name , login = tmp[0] ,tmp[1]
			person_dict[name ] = 1 
	return person_dict

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input file',dest='input',default='/annoroad/data1/bakPROJECT/PROJECT/log/backup.db')
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	parser.add_argument('-d','--delay',help='delay project log file',dest='delay',type=argparse.FileType('w'),required=True)
	parser.add_argument('-day','--day',help='day',dest='day',default= datetime.date.today().strftime('%Y%m%d') )
	#parser.add_argument('-m','--mm',help='output file',dest='mm',action='store_false')
	args=parser.parse_args()

	person_dict = read_person_list()

	delay_this_week , should_finish_this_week ,  should_finish_next_week = '', '' ,''
	bio_delay , expe_delay , info_delay  = '' , '' ,''

	all_projects = read_project(args.input)
	all_stat = {}
	for i in (['total' , 'running' , 'finish' , 'delay' , 'qc' , 'check' , 'pass_check' , 'finish_this_week']):
		all_stat[i] = {} 
		for j in ([ 'gexinghua' ,   'filter' , 'analysis' , 'research' , 'all' , 'unknown'] ) :  
			all_stat[i][j] = collections.defaultdict(int)

	for project_id in all_projects:
		a_project = all_projects[project_id]
		all_stat['total']['all'][a_project.person] += 1 
		all_stat['total'][a_project.judge_type()][a_project.person] += 1

		if a_project.delay_this_week(args.day) == 'yet finish':
			should_finish_next_week += '*' + a_project.__str__() 
		elif a_project.delay_this_week(args.day): 
			if a_project.delay_type() == 'bioinformatic delay':
				bio_delay += a_project.__str__()
			elif a_project.delay_type() == 'experiment delay':
				expe_delay += a_project.__str__()
			else :
				info_delay += a_project.__str__()
			#delay_this_week += '' + a_project.__str__()
		if a_project.finish_next_week(args.day):
			should_finish_next_week += '#' + a_project.__str__()

		if not a_project.state in ['结题' ,'停止' ,'暂停']:
			all_stat['running']['all'][a_project.person] += 1 
			all_stat['running'][a_project.judge_type()][a_project.person] += 1
		else:
			all_stat['finish']['all'][a_project.person] += 1 
			all_stat['finish'][a_project.judge_type()][a_project.person] += 1
			if a_project.finish_this_week(args.day) :
				all_stat['finish_this_week']['all'][a_project.person] += 1 
				all_stat['finish_this_week'][a_project.judge_type()][a_project.person] += 1

		if a_project.judge_delay() :
			all_stat['delay']['all'][a_project.person] += 1 
			all_stat['delay'][a_project.judge_type()][a_project.person] += 1

		if not a_project.pass_check == '否':
			all_stat['qc']['all'][a_project.person] += 1 
			all_stat['qc'][a_project.judge_type()][a_project.person] += 1

		all_stat['check']['all'][a_project.checker] += 1 
		all_stat['check'][a_project.judge_type()][a_project.checker] += 1

		if not a_project.pass_pm == '否':
			all_stat['pass_check']['all'][a_project.person] += 1 
			all_stat['pass_check'][a_project.judge_type()][a_project.person] += 1

	perfect_print(all_stat , args.output ,person_dict)
	args.delay.write("report_id|project_type|project_dalei|project_detail|project_id|name|person|start|end|finish_day|delay|delay_reason|sequence_finish|seq_date|state|infor_table_date|gannt_day")
	args.delay.write('''
-------------------------信息延期--------------------------------
{0}-------------------------实验延期--------------------------------
{1}-------------------------信息收集表延期-------------------------
{2}-------------------------yet finish this week-------------------
{3}-------------------------should finish next week-----------------
{4}'''.format( bio_delay , expe_delay , info_delay  , should_finish_this_week , should_finish_next_week))

if __name__ == '__main__':
	main()
