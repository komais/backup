#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import re
import time
import datetime
import getpass
import glob
import sqlite3
bindir = os.path.abspath(os.path.dirname(__file__))


__author__='Liu Tao'
__mail__= 'taoliu@annoroad.com'

pat1=re.compile('^\s*$')

class Project():
	def __init__(self, tmp):
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
		self.seq_finish_date = tmp[22]
		self.state = tmp[23]
		self.information_table_date = tmp[24]
		self.gannt_write_date = tmp[25]
		self.filepath = ''
	def __str__(self ):
		return "\t".join([self.report_id , self.project_type , self.project_dalei, self.project_xifen , self.contract_id , self.sub_project , self.name , self.person , self.start , self.end , self.cost , self.finish , self.delay, self.delay_cause , self.checker , self.pass_check  , self.pass_pm , self.pass_qc , self.submit_table , self.dir_quota , self.analysis_dir , self.sequence_finish , self.seq_finish_date ,self.state , self.information_table_date , self.gannt_write_date]) + "\n"
	def update(self , conn):
		tt = zip( [ 'REPORT_ID' , 'PORJECT_TYPE'  ,'PROJECT_DALEI' , 'PROJECT_DETAIL' , 'CONTRACT_ID' ,
			        'SUB_PROJECT_ID' , 'MISSION_NAME' , 'DUTYER' , 'MISSION_END_DATE' , 'PROJECT_END_DATE' ,
					'COST' ,  'BACKUP_DATE', 'BOOL_DELAY', 'DELAY_CAUSE' , 'CHECKER' , 
					'PASS_CEHCKER' , 'PASS_PM' , 'PASS_QC' , 'BOOL_CHECK_TABLE' , 'QUOTA' ,
					'PATHWAY' , 'BOOL_SEQ' , 'SEQ_FINISH_DATE' , 'PROJECT_STATE' ,'INFORMATION_TABLE_DATE' , 'GANNT_DATE'] , [self.report_id , self.project_type , self.project_dalei, self.project_xifen , self.contract_id , self.sub_project , self.name , self.person , self.start , self.end , self.cost , self.finish , self.delay, self.delay_cause , self.checker , self.pass_check  , self.pass_pm , self.pass_qc , self.submit_table , self.dir_quota , self.analysis_dir , self.sequence_finish , self.seq_finish_date ,self.state , self.information_table_date , self.gannt_write_date]) 
		ttt = [ "{0} = '{1}'".format(i[0] , i[1]) for i in tt ] 
		#print(''' UPDATE PROJECT SET {0} WHERE  REPORT_ID = {1} ; '''.format(",".join(ttt) , self.report_id ))
		conn.execute(''' UPDATE PROJECT SET {0} WHERE  REPORT_ID = '{1}' ; '''.format(",".join(ttt) , self.report_id ))
	def insert(self , conn):
		tt = ( [ 'REPORT_ID' , 'PORJECT_TYPE'  ,'PROJECT_DALEI' , 'PROJECT_DETAIL' , 'CONTRACT_ID' ,
			        'SUB_PROJECT_ID' , 'MISSION_NAME' , 'DUTYER' , 'MISSION_END_DATE' , 'PROJECT_END_DATE' ,
					'COST' ,  'BACKUP_DATE', 'BOOL_DELAY', 'DELAY_CAUSE' , 'CHECKER' , 
					'PASS_CEHCKER' , 'PASS_PM' , 'PASS_QC' , 'BOOL_CHECK_TABLE' , 'QUOTA' ,
					'PATHWAY' , 'BOOL_SEQ' , 'SEQ_FINISH_DATE' , 'PROJECT_STATE' ,'INFORMATION_TABLE_DATE' , 'GANNT_DATE'] , [self.report_id , self.project_type , self.project_dalei, self.project_xifen , self.contract_id , self.sub_project , self.name , self.person , self.start , self.end , self.cost , self.finish , self.delay, self.delay_cause , self.checker , self.pass_check  , self.pass_pm , self.pass_qc , self.submit_table , self.dir_quota , self.analysis_dir , self.sequence_finish , self.seq_finish_date ,self.state , self.information_table_date , self.gannt_write_date])
		ttt1 = ",".join(tt[0])
		ttt2 = ",".join(["'{0}'".format(i) for i in tt[1]])
		#print('''INSERT INTO PROJECT ({0})  VALUES ({1});'''.format(ttt1 , ttt2))
		conn.execute('''INSERT INTO PROJECT ({0})  VALUES ({1});'''.format(ttt1 , ttt2))


def remove_bad_format_date(day):
	day = day.replace("-" , "")
	day = day.replace("/" , "")
	return day

def read_person_list():
	infile = '{0}/person.list'.format(bindir)
	person_dict = {}
	with open(infile)  as f_in :
		for line in f_in :
			if line.startswith('#') or re.search(pat1,line):continue
			tmp = line.rstrip().split()
			name , login = tmp[0] ,tmp[1]
			person_dict[login] = name
	return person_dict

def read_project_file():
	infile = '{0}/project_type.xls'.format(bindir)
	project_dict = {}
	with open(infile) as f_in :
		for line in f_in :
			if line.startswith('#') or re.search(pat1,line):continue
			tmp = line.rstrip().split()
			dalei , xifen = tmp[0] , tmp[1]
			if not dalei in project_dict:
				project_dict[dalei] = []
			project_dict[dalei].append(xifen)
	return project_dict

def check_file_lock(filename):
	bakFile = '{0}.bak'.format(filename)
	runner = getpass.getuser()
	if os.path.exists(bakFile):
		name = os.popen("tail -1 {0}".format(bakFile))
		name = name.read().rstrip()
		sys.exit("{0}正在填写，请稍后再来。。。 或者 如果{0} 没有在填写，那么就是{0}没有正确退出，请联系liutao解决".format(name))
	else:
		os.system('cp {0} {1} && echo {2} >> {1} '.format(filename , bakFile , runner))

def myinput(content):
	result = ''
	while(1):
		try:
			result = input('>>> ' + content)
			result = result.rstrip()
			if result == 'exit':
				#release_file(filename)
				sys.exit(0)
			else:
				return result.rstrip()
		except SystemExit : 
			print("程序退出，bye")
			sys.exit(0)
		except :
			print("请重新输入")
			pass

def read_bms(bms , person_dict):
	person_list = person_dict.values()
	projectInfo = {}
	for count , line in enumerate(bms):
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.strip("\n").split('\t')
		if count == 0 : continue
		contractId , subProjectId , person , project_date , name , xiadan_date = tmp[0] , tmp[1], tmp[2] , remove_bad_format_date( tmp[5] )  ,  tmp[6] ,remove_bad_format_date( tmp[7] )
		if not person in person_list : continue
		if xiadan_date == '' : continue
		if time.strptime(xiadan_date , "%Y%m%d") < time.strptime("20160401" , "%Y%m%d") : continue
		experiment_date = remove_bad_format_date (  tmp[12] )

		if not subProjectId in projectInfo:
			projectInfo[ subProjectId ] = [contractId , person , experiment_date , project_date , name ]
		else:
			print("注意 : {0}在BMS上下了两次单，不过不影响备份，请继续...".format(subProjectId))
	return projectInfo

def more_than_one_day( date2 ) :
	date1 = get_time()
	date1 = remove_bad_format_date(date1) 
	date2 = remove_bad_format_date(date2) 
	#date1 = date1.replace("-" , "")
	#date1 = date1.replace("/" , "")
	#date2 = date2.replace("-" , "")
	#date2 = date2.replace("/" , "")
	if re.search(pat1, date2 ) :
		return False
	elif time.strptime(date1 , "%Y%m%d") > time.strptime(date2 , "%Y%m%d") : 
		return True
	else:
		return False

def update_new_project( newProject , output , person_dict):
	runner = get_runner_name( person_dict )
	oldProject = {} 
	std_id = list(range(1,5000))
	suppelement_id = list(range(5000 , 100000)) 
	conn = sqlite3.connect(output)
	tt = [ 'REPORT_ID' , 'PORJECT_TYPE'  ,'PROJECT_DALEI' , 'PROJECT_DETAIL' , 'CONTRACT_ID' ,
			        'SUB_PROJECT_ID' , 'MISSION_NAME' , 'DUTYER' , 'MISSION_END_DATE' , 'PROJECT_END_DATE' ,
					'COST' ,  'BACKUP_DATE', 'BOOL_DELAY', 'DELAY_CAUSE' , 'CHECKER' , 
					'PASS_CEHCKER' , 'PASS_PM' , 'PASS_QC' , 'BOOL_CHECK_TABLE' , 'QUOTA' ,
					'PATHWAY' , 'BOOL_SEQ' , 'SEQ_FINISH_DATE' , 'PROJECT_STATE' ,'INFORMATION_TABLE_DATE' , 'GANNT_DATE'] 

	for tmp in conn.execute('SELECT {0}  FROM PROJECT ; '.format( ",".join(tt))) : 
		report_id  , project_type , dalei   ,xifen  ,  sub_project ,name , charger  = tmp[0] , tmp[1] , tmp[2] ,tmp[3] , tmp[5] , tmp[6] , tmp[7] 
		checker , pass_check , pass_pm  , pass_qc , submit_table  = tmp[14], tmp[15], tmp[16], tmp[17] , tmp[18]
		finish_day , owner , seq_finish , project_stat , quota , gannt_fill_date = tmp[11] , tmp[7]  , tmp[21] , tmp[23] , tmp[19], remove_bad_format_date(tmp[25].rstrip())
		if checker == runner :
			if more_than_one_day( finish_day ) :
				if not  ( pass_check in ['是' ,'否']  and pass_pm in  ['是' ,'否' , '不知道'] and pass_qc in  ['是' ,'否' , '不知道' ]  and submit_table in  ['是' ,'否' , '不用提交']  ) :
					print("[项目复核]: {0} {3} {4} {1} {2} 需要您，请尽快复核".format(sub_project , name , charger , report_id , project_type ))
		my_week = datetime.date.today().weekday()
		today = get_time()
		gap_day = 10 
		if gannt_fill_date : 
			#print(today , gannt_fill_date)
			gap_day = datetime.datetime.strptime(today , "%Y%m%d") - datetime.datetime.strptime(gannt_fill_date , "%Y%m%d")
			gap_day = gap_day.days
		if (my_week >= 3 or my_week <=0) and owner == runner and gap_day > 2 :
			if project_type == '商业':
				if seq_finish != '是' or  ( not project_stat in [ '结题', '停止']) :
					print("[甘特图]: {0} {3} {4} {1} {2} 需要您填写甘特图 , 如果本周已经填写请忽视".format(sub_project , name , charger , report_id , project_type ))
			else:
				if project_stat != '结题':
					print("[甘特图]: {0} {3} {4} {1} {2} 需要您填写甘特图 , 如果本周已经填写请忽视".format(sub_project , name , charger , report_id , project_type ))

		if not quota  and project_type != '个性化分析'  and owner == runner : 
			if not (owner == '涂成芳' and  dalei == 'Filter') :
				print("[目录开通]: {0} {3} {4} {1} {2} 需要您填写开通目录配额，如果不用开通请填写0g".format(sub_project , name , charger , report_id , project_type ))

		serial_number = int(report_id.split('-')[-1])
		#print(serial_number)
		if serial_number >= 5000 : 
			if  serial_number in suppelement_id :
				suppelement_id.remove( serial_number )
		else :
			if serial_number in std_id  :
				std_id.remove( serial_number )
		if project_type == "个性化分析" or serial_number >= 5000: continue
		if sub_project in newProject : 
			newProject[sub_project] += [dalei , xifen]
			#print(newProject[sub_project])
		if not sub_project in oldProject:
			oldProject[sub_project] = report_id
		else: 
			print("{0} is repeat in backup.xls".format(sub_project))
	
	#print(newProject['CR0225-52'])
	#print(oldProject['CR0225-52'])
	for aProject in newProject:
		if not aProject in oldProject:
			if aProject == 'CR0225-52' :
				print('tttt')
			[contractId , person , experiment_date , project_date , name ] = newProject[aProject]
			a_std_id = std_id.pop(0) 
			report_id = "KJ-DB-{0}-2016-{1:04d}".format( aProject , a_std_id)
			dalei = ''
			tt1 = " , ".join( [ 'REPORT_ID' , 'PORJECT_TYPE'  ,'PROJECT_DALEI' , 'PROJECT_DETAIL' , 'CONTRACT_ID' ,
			        'SUB_PROJECT_ID' , 'MISSION_NAME' , 'DUTYER' , 'MISSION_END_DATE' , 'PROJECT_END_DATE' ,
					'COST' ,  'BACKUP_DATE', 'BOOL_DELAY', 'DELAY_CAUSE' , 'CHECKER' , 
					'PASS_CEHCKER' , 'PASS_PM' , 'PASS_QC' , 'BOOL_CHECK_TABLE' , 'QUOTA' ,
					'PATHWAY' , 'BOOL_SEQ' , 'SEQ_FINISH_DATE' , 'PROJECT_STATE' ,'INFORMATION_TABLE_DATE' , 'GANNT_DATE'] )
			if name.find('测序任务单') > 1 :
				dalei = 'Filter'

			tt2 = "  ,  ".join([ "'{0}'".format(i) for i in [ report_id , '', dalei, '' , contractId , 
				                                              aProject , name , person , experiment_date , project_date
															  ]+ ['']*16])
			#print("INSERT INTO PROJECT ( {0} ) VALUES ({1} );".format(tt1,   tt2 )) 
			conn.execute("INSERT INTO PROJECT ( {0} ) VALUES ({1} );".format(tt1,   tt2 )) 
	conn.commit()
	conn.close()
	return suppelement_id

def read_project( output):
	allProject = {} 
	allReprotID = {} 
	#with open(infile) as f_file:
	conn = sqlite3.connect(output)
	tt = [ 'REPORT_ID' , 'PORJECT_TYPE'  ,'PROJECT_DALEI' , 'PROJECT_DETAIL' , 'CONTRACT_ID' ,
			        'SUB_PROJECT_ID' , 'MISSION_NAME' , 'DUTYER' , 'MISSION_END_DATE' , 'PROJECT_END_DATE' ,
					'COST' ,  'BACKUP_DATE', 'BOOL_DELAY', 'DELAY_CAUSE' , 'CHECKER' , 
					'PASS_CEHCKER' , 'PASS_PM' , 'PASS_QC' , 'BOOL_CHECK_TABLE' , 'QUOTA' ,
					'PATHWAY' , 'BOOL_SEQ' , 'SEQ_FINISH_DATE' , 'PROJECT_STATE' ,'INFORMATION_TABLE_DATE' , 'GANNT_DATE'] 

	for tmp in conn.execute('SELECT {0}  FROM PROJECT ; '.format( ",".join(tt))) :
		a_project = Project(tmp)
		if not a_project.sub_project in allProject : 
			allProject[a_project.sub_project] = {"std" : []  , 'supp' : [] }
		if a_project.project_type == '个性化分析':
			allProject[a_project.sub_project]['supp'].append(a_project)
		else:
			allProject[a_project.sub_project]['std'].append(a_project)
		if not a_project.report_id in allReprotID :
			allReprotID[a_project.report_id] = 1 
	conn.close()
	return allProject , allReprotID

def get_runner_name(person_dict):
	runner = getpass.getuser()
	if runner in person_dict :
		name = person_dict[runner]
		return name
	else:
		print("你没有权限填写，bye!")
		#release_file(filename)
		sys.exit()

def get_date(content , blank = False):
	while(1):
		input_date = myinput("{0},格式为 20160412\n".format(content))
		if blank and input_date == '' :
			return ''
		try : 
			time.strptime( input_date , "%Y%m%d")
			return input_date
		except : 
			print("时间输入有误，请重新输入")
			continue

def create_report_id( subProject , supp_id):
	return "KJ-DB-{0}-2016-{1:04d}".format(subProject ,supp_id) 

def get_cost( content , a_list):
	#print(a_list)
	while(1):
		input_type = myinput(content + "\n")
		if input_type in list( map (str , range( len(a_list) ))):
			return a_list[int(input_type)]
		else:
			print("输入的类型错误，请重新输入")
			continue

def get_time() : 
	today = datetime.date.today()
	ISOFORMAT='%Y%m%d'
	return today.strftime(ISOFORMAT)

def judge_delay(date1 , date2) :
	#print(date1 , date2)
	date1 = remove_bad_format_date(date1) 
	date2 = remove_bad_format_date(date2) 
	#date1 = date1.replace("-" , "")
	#date1 = date1.replace("/" , "")
	#date2 = date2.replace("-" , "")
	#date2 = date2.replace("/" , "")
	if date1 == '' or date2 == '' : 
		return False
	if time.strptime(date1 , "%Y%m%d") >= time.strptime(date2 , "%Y%m%d") : 
		return False
	else:
		return True

def get_checker(content , person_dict , user):
	while(1):
		input_content = myinput("{0}\n".format(content))
		if input_content in person_dict.values() and input_content != user :
			return input_content
		elif input_content in person_dict.keys() and person_dict[input_content] != user :
			return person_dict[input_content]
		else:
			print("复核人员填写错误，请重新填写")

def get_dalei(content , project_dict):
	while(1):
		cc = content
		daleis = sorted(project_dict.keys())
		for i ,j in enumerate(daleis):
			cc += "\n{0:8}[{1}]".format(j , i )
		input_d = myinput(cc + "\n")
		if input_d in list(map(str,range( len( daleis )  ))):
			return daleis[int(input_d)]
		else:
			print("输入的类型错误，请重新输入")
			continue

def get_xifen( content , dalei , project_dict):
	while(1):
		cc = content
		xifen = sorted(project_dict[dalei])
		if len(xifen) > 1 :
			for i ,j in enumerate(xifen):
				cc += "\n{0:10}[{1}]".format(j , i )
			input_d = myinput(cc + "\n")
			if input_d in list(map(str,range( len( xifen )  ))):
				return xifen[int(input_d)]
			else:
				print("输入的类型错误，请重新输入")
				continue
		else :
			print("该类下只有一个选择，我帮你选了{0}".format(xifen[0]))
			return xifen[0]

def get_pass(content ,choose):
	while(1):
		input_d = myinput(content + "是[1]  否[2] {0}[3]\n".format(choose))
		if input_d == '1' :
			return '是'
		elif input_d == '2' :
			return '否'
		elif input_d == '3' :
			return choose
		else:
			print("输入错误，请重新输入")

def get_path(content):
	while(1):
		input_d = myinput(content + "\n" )
		if input_d == '':
			return ''
		elif input_d.startswith('/') and os.path.exists(input_d):
			return input_d
		else:
			print("{0}不存在，请重新输入".format(input_d))

def backup(project):
	backup_path = "/annoroad/data1/bakPROJECT/PROJECT/current/"
	if project.filepath == '' :
		print("如果你是分析人员，请手动备份")
	else:
		if len(glob.glob("{0}/{1}*".format(backup_path , project.report_id))) > 0 :
			print("注意：该项目之前的备份会被删除")
			cmd = 'rm -r {1}/{2}* && cp -r {0} {1}/{2}_{3}'.format(project.filepath , backup_path , project.report_id , os.path.basename(project.filepath))
		else:
			cmd = 'cp -r {0} {1}/{2}_{3}'.format(project.filepath , backup_path , project.report_id , os.path.basename(project.filepath))
		print("备份中")
		if os.system(cmd):
			print( "备份失败，请手动备份")
		else:
			print("备份成功")

def get_renwudan(a_dict):
	name = ''
	for i in a_dict:
		if len(a_dict[i]) == 0 :
			continue
		else:
			choose_project = a_dict[ i ][0]
			name = choose_project.name
	return name

def get_bms_information(a_dict):
	contract_id , user , name , dalei , xifen = '' , '' , '' , '' ,''
	for i in a_dict:
		if len(a_dict[i]) == 0 :
			continue
		else:
			choose_project = a_dict[ i ][0]
			#print(choose_project.contract_id , choose_project.name , choose_project.start)
			contract_id = choose_project.contract_id 
			user = choose_project.person
			dalei = choose_project.project_dalei
			xifen = choose_project.project_xifen
			name = choose_project.name
	return [contract_id , user , name , dalei , xifen]

def input_sub_project_id( allProject ) : 
	subProject = ''
	subProject = myinput("step1 请输入子项目号:\n")
	if not subProject in allProject :
		print("该项目不在项目列表中，请联系彬安更新bms文件或者刘涛进行立项")
		#release_file(filename)
		sys.exit()
	return subProject 

def get_choose_porject_object(project_type , a_dict):
	r_obj = ''
	if project_type == 0 : 
		if len( a_dict['std'] ) > 0 :
			r_obj =  a_dict['std'][0]
		else:
			print("注意：该项目没有标准分析的流水号在列表中，请选择个性化分析项目")
			#release_file(filename)
			sys.exit()
	elif project_type == 1 :
		print("注意：请不要选择修改一个结题项目，否则会更新记录，可能导致该项目延期")
		content = "请选择个性化项目：\n"
		choose_list = [ 'create_new' ] 
		content += "创建一个新的个性化分析[0]\n"
		project_length = len(a_dict['supp'])
		if project_length > 0 : 
			for count , i in enumerate(a_dict['supp']):
				content += "{0} {2} [{1}]\n".format(i.report_id , count+1  , i.state )
				choose_list.append( i ) 
		r_obj = get_cost( content.rstrip() , choose_list )
	if r_obj == 'create_new':
		pass
	else:
		if r_obj.state == '结题':
			confirm = get_cost("您是否要选择一个已经结题并备份完成的项目？是[0] 否[1]\n修改一个结题项目，否则会更新记录，可能导致该项目延期" , [0 , 1] )
			if confirm == 0 :
				pass
			else :
				print("退出中，bye")
				#release_file(filename)
				sys.exit()

	return r_obj

def do_create_new_supp_analysis(subProject ,  supp_id , allProject , project_bms ):
	if subProject in allProject :
		[contract_id , user , name , dalei , xifen ] = get_bms_information(allProject[subProject])
	elif subProject in project_bms:
		[contract_id , user , u1 , u2 , name , dalei , xifen ] = project_bms[subProject]
	else:
		print('Error : no information')
		#release_file(filename)
		sys.exit()
	print("注意： 以下*号项目填写后将无法进行修改，请慎重填写")
	project_start = get_date("*请输入个性化分析起始时间:")
	project_end = get_date("*请输入个性化约定结束时间:")
	a_supp_id = supp_id.pop(0) 
	report_id = create_report_id( subProject , a_supp_id) 
	project_cost = get_cost("*请输入项目人时消耗\n(0h  , 2h ] A [0] ;\n(2h  , 4h ] B [1]\n(4h  , 8h ] C [2];\n(8h  , 16h] D [3];\n(16h , 24h] E [4] ;\n(24h ,    ) F [5]" , ['A','B','C','D','E','F']  )
	choose_project = Project( [ report_id , '个性化分析' , dalei , xifen , contract_id , subProject , name , user , project_start , project_end , project_cost , '' , '' , '' , '' , '' , '' ,'' , '' , '' ,'' ,'' ,'' ,'' , '' , '' ] )
	return choose_project 

def do_update_project_information(choose_project , project_dict):
	if not choose_project.project_type :
		choose_project.project_type = get_cost("请输入项目类型：商业[0]  / 研发[1]" , ['商业' ,'研发'])
	if not choose_project.project_dalei : 
		choose_project.project_dalei = get_dalei("请输入项目类型" , project_dict)
	if not choose_project.project_xifen :
		choose_project.project_xifen = get_xifen("请输入项目细分类型" , choose_project.project_dalei , project_dict )
	if not choose_project.cost : 
		if choose_project.project_type == '商业':
			if choose_project.project_dalei == 'Filter':
				print("商业过滤标准分析默认工时是2h，等级为A")
				choose_project.cost = 'A'
			else:
				print("商业标准分析默认工时是4h，等级为B")
				choose_project.cost = 'B'
		else:
			choose_project.cost = get_cost("请输入项目人时消耗\n(0h  , 2h ] A [0] ;\n(2h  , 4h ] B [1]\n(4h  , 8h ] C [2];\n(8h  , 16h] D [3];\n(16h , 24h] E [4] ;\n(24h ,    ) F [5]" , ['A','B','C','D','E','F']  )

def input_delay_cause( choose_project ,date_input ):
	delay_reason = ''
	if choose_project.project_type == '商业':
		if choose_project.seq_finish_date == '' :
			print(">>>数据尚未下机，无需填写延期原因")
			delay_reason = '数据未下机'
		elif choose_project.end == '':
			print('>>>没有项目结题日期，所以无需填写')
			delay_reason = ''
		elif choose_project.start == '':
			print('>>>项目没有数据下机日期，请直接输入延期原因')
			delay_reason += myinput("请输入延期原因\n")
		else : 
			experiment_expect_date = datetime.datetime.strptime( choose_project.start , "%Y%m%d")
			experiment_reality_date = datetime.datetime.strptime( remove_bad_format_date(choose_project.seq_finish_date) , "%Y%m%d") 
			project_expect_date = datetime.datetime.strptime( choose_project.end , "%Y%m%d")
			project_reality_date = datetime.datetime.strptime( date_input , "%Y%m%d")
			
			day_delay_info_table = 0 
			if choose_project.project_dalei != 'Filter':
				if choose_project.information_table_date != '' :
					information_table_date = datetime.datetime.strptime( remove_bad_format_date(choose_project.information_table_date), "%Y%m%d")
					day_delay_info_table = information_table_date - experiment_expect_date 
					day_delay_info_table = day_delay_info_table.days
			
			day_delay_experiment = experiment_reality_date - experiment_expect_date 
			day_delay_experiment = day_delay_experiment.days 
			day_delay_project = project_reality_date - project_expect_date 
			day_delay_project = day_delay_project.days
			if day_delay_experiment > 0 and day_delay_info_table > 0  : 
				delay_reason = "下机延期{0}天 ; 信息收集表延期{1}天 ;  ".format( day_delay_experiment , day_delay_info_table)
				max_day = max(day_delay_experiment , day_delay_info_table)
				if day_delay_project > max_day :
					print('>>>下机和信息收集表总共延期{0}天， 项目延期{1}天，所以您还需要输入其他原因'.format( max_day , day_delay_project))
					delay_reason += myinput("请输入延期原因\n")
				else :
					print('>>>下机和信息收集表总共延期{0}天， 项目延期{1}天，您是否想输入其他的原因,没有请直接回车'.format( max_day, day_delay_project))
					delay_reason += myinput("请输入延期原因\n")
			elif day_delay_experiment > 0:
				delay_reason = "下机延期{0}天 ;  ".format( day_delay_experiment )
				max_day = day_delay_experiment
				if day_delay_project > max_day :
					print('>>>下机延期{0}天， 项目延期{1}天，所以您还需要输入其他原因'.format( max_day , day_delay_project))
					delay_reason += myinput("请输入延期原因\n")
				else :
					print('>>>下机延期{0}天， 项目延期{1}天，您是否想输入其他的原因,没有请直接回车'.format( max_day, day_delay_project))
					delay_reason += myinput("请输入延期原因\n")
			elif day_delay_info_table > 0 :
				delay_reason = "信息收集表延期{0}天 ;  ".format( day_delay_info_table)
				max_day = day_delay_info_table
				if day_delay_project > max_day :
					print('>>>信息收集表延期{0}天， 项目延期{1}天，所以您还需要输入其他原因'.format( max_day , day_delay_project))
					delay_reason += myinput("请输入延期原因\n")
				else :
					print('>>>信息收集表延期{0}天， 项目延期{1}天，您是否想输入其他的原因,没有请直接回车'.format( max_day, day_delay_project))
					delay_reason += myinput("请输入延期原因\n")
				pass
			else : 
				print('>>>实验和信息收集表都没有延期，项目延期{0}天，请您输入合理的理由:'.format(day_delay_project))
				delay_reason += myinput("请输入延期原因\n")
	else :
		delay_reason += myinput("请输入延期原因\n")
	return delay_reason

def do_modify_project_stat(choose_project ,person_dict , user ):
	choose_project.finish = get_time()
	if not choose_project.seq_finish_date : 
		if choose_project.project_type == '商业':
			if choose_project.sequence_finish == '是':
				if  choose_project.seq_finish_date :
					pass
				else:
					choose_project.seq_finish_date = get_date("请输入测序完成日期(收到旭宁的邮件的日期,不是反馈数据量的日期")
			else : 
				choose_project.sequence_finish = get_cost("数据是否完全下机：是[0] , 否[1]" , ['是' , '否'])
				choose_project.seq_finish_date = ''
				if choose_project.sequence_finish == '是' :
					choose_project.seq_finish_date = get_date("请输入测序完成日期(收到旭宁的邮件的日期,不是反馈数据量的日期")

	if choose_project.delay == '是':
		tt = get_cost("请输入延期原因: {0}[0] , 重新输入[1]".format(choose_project.delay_cause) , [ 0 , 1 ])
		if tt == 1 :
			#choose_project.delay_cause = myinput("请输入延期原因\n")
			choose_project.delay_cause = input_delay_cause( choose_project , choose_project.finish )
	else:
		project_delay = judge_delay( choose_project.end , choose_project.finish)
		choose_project.delay = '否'
		if project_delay : 
			choose_project.delay_cause = input_delay_cause( choose_project , choose_project.finish)
			choose_project.delay = '是'
	choose_project.checker = get_checker("请输入复核人" ,person_dict , user)
	choose_project.pass_check = ''
	choose_project.pass_pm = ''
	choose_project.pass_qc = ''
	choose_project.submit_table = ''
	choose_project.filepath = get_path("请输入文件路径[可选]")
	choose_project.state = '结题'

def do_open_dir_request(choose_project):
	if not choose_project.analysis_dir :
		while(1):
			quota = myinput("请输入配额：如果无需开通请填写0g\n")
			patt = re.compile('^\d+[GMTgmt]$')
			if re.search(patt , quota):
				choose_project.dir_quota = quota
				return 0 
			else:
				print("配额大小输入错误,请重新输入")
	else:
		print("目录已存在，无需申请")

def do_gannt_request( choose_project):
	my_week = datetime.date.today().weekday()
	if my_week < 3 and  my_week > 0  :
		print("今天不是周五、周六、周日,不能填哦")
		#release_file(filename)
		sys.exit()

	if choose_project.project_type != '个性化分析':
		if choose_project.sequence_finish == '是':
			pass
		else : 
			choose_project.sequence_finish = get_cost("数据是否完全下机：是[0] , 否[1]" , ['是' , '否'])
			choose_project.seq_finish_date = ''
			if choose_project.sequence_finish == '是' :
				choose_project.seq_finish_date = get_date("请输入测序完成日期(收到旭宁的邮件的日期,不是反馈数据量的日期")

	if choose_project.project_type == '商业' and choose_project.project_dalei != 'Filter': 
		if not choose_project.information_table_date : 
			choose_project.information_table_date = get_date("* 请输入收到确认通过的信息收集表的日期 , 没有请直接按回车\n请注意： 填写后将无法修改，请如实填写" , True)

	today = get_time()
	dayday = today 
	if choose_project.finish :
		dayday = choose_project.finish 
	if choose_project.delay == '是':
		tt = get_cost("请输入延期原因: {0}[0] , 重新输入[1]".format(choose_project.delay_cause) , [ 0 , 1 ])
		if tt == 1 :
			choose_project.delay_cause = input_delay_cause( choose_project , dayday  )
	else:
		project_delay = judge_delay( choose_project.end , today)
		choose_project.delay = '否'
		if project_delay : 
			choose_project.delay_cause = input_delay_cause( choose_project , dayday )
			choose_project.delay = '是'
	state = get_cost('请输入项目状态：暂停[0] , 停止[1] , 正常[2] ' , ['暂停' , '停止' , '正常'])
	if state == '正常':
		if not choose_project.finish:
		#	print(choose_project.finish)
			if choose_project.delay == '是':
				choose_project.state = '项目延期'
			else:
				choose_project.state = '运行中'
		else:
			choose_project.state = '结题'
			
	else:
		choose_project.state = state
	choose_project.gannt_write_date = today

def get_user_name(subProject , allProject ,project_bms):
	if subProject in allProject :
		[contract_id , user , name , dalei , xifen ] = get_bms_information(allProject[subProject])
	elif subProject in project_bms:
		[contract_id , user , u1 , u2 , name , dalei , xifen ] = project_bms[subProject]
	else:
		print('Error : no information')
		#release_file(filename)
		sys.exit()
	return user

def fill_a_finish_project(allProject , all_report_id , output , project_bms , supp_id , person_dict , project_dict):
	step = 0 
	subProject  , choose_project , project_type  = '' , '' ,''
	runner = get_runner_name( person_dict )
	
	subProject = input_sub_project_id( allProject )
	user = get_user_name( subProject , allProject ,project_bms)
	print("任务单名称为：{0}".format(get_renwudan(allProject[subProject])))
	
	task = get_cost( "请输入要执行的任务: \n开通目录申请[0]\n填写甘特图[1]\n填写完成项目统计[2]" , [0 , 1, 2])
	if task == 0 :
		if runner == user :
			print("您是报告制作人, 请继续填写")
			choose_project = get_choose_porject_object( 0 , allProject[subProject] )
			do_update_project_information(choose_project , project_dict)
			do_open_dir_request( choose_project) 
		else:
			print("信息制作人是{0}, 不能申请开通目录".format(user))
			#release_file(filename)
			sys.exit()
	elif task == 1 : 
		if runner == user :
			print("您是报告制作人, 请继续填写")
			project_type = get_cost("step2 请输入是对下列哪种项目类型填写甘特图： 标准分析/RD项目[0] 或者 个性化分析[1] ?" , [ 0 , 1 ])
			choose_project = get_choose_porject_object( project_type , allProject[subProject] ) 
			if choose_project == 'create_new':
				choose_project = do_create_new_supp_analysis( subProject ,  supp_id , allProject , project_bms )
			do_update_project_information(choose_project , project_dict)
			do_gannt_request( choose_project) 
		else:
			print("您不是报告制作人, 不能填写甘特图")
			#release_file(filename)
			sys.exit()
	elif task == 2 :
		project_type = get_cost("step2 请输入是对下列哪种项目类型进行备份： 标准分析/RD项目[0] 或者 个性化分析[1] ?" , [ 0 , 1 ])
		choose_project = get_choose_porject_object( project_type , allProject[subProject] ) 
		if choose_project == 'create_new':
			if runner == user : 
				choose_project = do_create_new_supp_analysis( subProject ,  supp_id , allProject , project_bms )
				do_modify_project_stat(choose_project , person_dict , user)
			else:
				print("你不是项目负责人，不能创建个性化分析，退出了。。。")
				#release_file(filename)
				sys.exit() 
		else:
			if runner == user : 
				print("您是报告制作人, 请继续填写")
				do_update_project_information(choose_project , project_dict )
				do_modify_project_stat(choose_project , person_dict , user)
			elif runner == choose_project.checker:
				choose_project.pass_check = get_pass("复核人是否一次性通过" , '不知道')
				choose_project.pass_pm = get_pass("项目管理是否一次通过" , '不知道' )
				choose_project.pass_qc = get_pass("质量部是否一次通过" , '不知道' )
				choose_project.submit_table = get_pass("是否提交复核表，研发和个性化分析可以不用提交；标准分析请如实填写  ", '不用提交')
			else:
				print("您既不是分析人员，也不是复核人员，别闹，退出了。。。")
				return 0 

	print("你的项目编号为：{0}".format(choose_project.report_id))
	#f_out = open('{0}.tmp'.format(output) , 'w')
	tag = 0
	conn = sqlite3.connect(output)
	if not choose_project.report_id in all_report_id :
		choose_project.insert(conn)
	else: 
		choose_project.update(conn)
	conn.commit()
	conn.close()
	backup(choose_project)

def release_file(filename):
	os.system("sqlite3  {0} .dump > {0}.sql && chmod 777 {0}.sql  ".format(filename ))
	os.system("cp {0} /home/liutao/backup/{1} && chmod 777 /home/liutao/backup/{1}  ".format(filename , os.path.basename(filename) ))
	
	print("更新成功")

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))

	parser.add_argument('-i','--input',help='input file',dest='input',type=open,default='{0}/current.xls'.format(bindir))
	parser.add_argument('-o','--output',help='output file',dest='output',default='/annoroad/data1/bakPROJECT/PROJECT/log/backup.db')
	#parser.add_argument('-m','--mm',help='output file',dest='mm',action='store_false')
	args=parser.parse_args()
	
	global filename
	filename = args.output 
	#check_file_lock(args.output)
	person_dict = read_person_list()
	project_dict = read_project_file()
	newProject = read_bms(args.input , person_dict )
	supp_id = update_new_project(newProject, args.output , person_dict)
	project_info , all_report_id  = read_project(args.output)
	fill_a_finish_project(project_info , all_report_id ,  args.output , newProject , supp_id , person_dict , project_dict  )
	release_file(args.output)

if __name__ == '__main__':
	main()
