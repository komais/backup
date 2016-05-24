import httplib2
import urllib.parse 
import time
import copy
import re
import datetime
import argparse


pat1 = re.compile('^\s+$')

__author__ = 'liutao'
__mail__='taoliu@annoroad.com'

header={'Content-type': 'application/x-www-form-urlencoded',
        'cache-control':'no-cache',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22'}
h=httplib2.Http('d:/tmp/cache')


def login():
    body = {"user": "lt" , 'pwd' : 'lt' , 'login' : '登陆'} 

    url = 'http://192.168.60.23/bms/index.php'
    response , content = h.request( url , 'POST' , headers = header ,
                                body = urllib.parse.urlencode(body))
    return response['set-cookie'].split(';')[0]

def insert_sub_project(cookie , sub_project_id , finish_date , dutyer , require_content):
    url = 'http://192.168.60.23/bms/insertsubprojectinfo.php?contractnum=ngs_bioinfo'
    head=copy.deepcopy(header)
    head['Cookie']=cookie
    body = {"contractnum" : "ngs_bioinfo" , "subprojectnum" : sub_project_id , "state":"" ,
            "date14" :  finish_date , "species" : ""  , "projectprincipal" : "刘涛" ,
            "experimentprincipal" : "------" , "analysisprincipal" : dutyer , "date1" : "" ,
            "sampletype": "" , "date2" : '' , 'detectionsituation' : '' ,
            "samplenum" : '' , "uploadusername" : '' , 'uploadpassword' :  '' , 'date9' :  '' ,
            'date10':'' , 'date11' : ''  ,  'date12':'' , 'date13' : '' ,'samplename' : '' ,
            'subprojectrequire' : require_content , 'comment': '' , 'insert' : '插入' , 'MM_insert':'form'}
    response,content=h.request(url,'POST',headers=head,body=urllib.parse.urlencode(body))
    return(response,content)

def add_sample(cookie , sub_project_id , finish_date , dutyer ,require_content , start_date , project_name):
    url = 'http://192.168.60.23/bms/insertjoborder.php'
    head=copy.deepcopy(header)
    head['Cookie']=cookie
    body = {"contractnum" : "ngs_bioinfo"  ,
            "subprojectnum" :sub_project_id ,
            "projectprincipal" : '刘涛'  ,
            "experimentprincipal" : "------"   ,
            "analysisprincipal" : dutyer ,
            "date14" : finish_date ,
            "subprojectrequire" : require_content ,
            "samplenumget" : "-1" ,
            "inputtext" : '' ,
            "submit" : "提交"}
    response,content=h.request(url,'POST',headers=head,body=urllib.parse.urlencode(body))

    today = datetime.date.today()
    today = today.strftime('%Y-%m-%d')
    body = {"date1": today ,
            "projectname":"科技服务研发项目",
            "contractnum":"ngs_bioinfo",
            "subprojectnum":sub_project_id ,
            "jobordername" : sub_project_id + project_name ,
            "projectprincipal": '刘涛'  ,
            "experimentprincipal":"------",
            "date2" : start_date ,
            "analysisprincipal": dutyer ,
            "date14": finish_date ,
            "subprojectrequire" : require_content ,
            "string6":"",
            "samplename1":"",
            "samplenum1":"",
            "libtype1":"", 
            "libnum1":"",
            "size1":"",
            "sequencetype1":"",
            "datarequire1":"",
            "insert":"下单",
            "samplenumget":"1",
            "MM_insert":"form"}
    response,content=h.request(url,'POST',headers=head,body=urllib.parse.urlencode(body))
    return response , content

	
def reformat_date(day):
	return time.strftime("%Y-%m-%d" , time.strptime( day  , "%Y/%m/%d") )
        

def xiadan(  sub_project_id , finish_date , dutyer , require , start_date , project_name):
    #sub_project_id , finish_date , dutyer , require = 'test-2test-2' , '2016-06-13' , '刘涛' , 'dddddddddddddddddd'
    cookie= login()
    response, content = insert_sub_project(cookie , sub_project_id , finish_date , dutyer , require)
    #print(content.decode())
    if content.decode().find('Duplicate entry') > -1: print(sub_project_id , "replicate")
    response, content = add_sample(cookie , sub_project_id , finish_date , dutyer , require , start_date , project_name)
    
def main():
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input file',dest='input',type=open , required = True)
	args=parser.parse_args()
	
	for line in args.input:
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		sub_project_id , project_name, dutyer, start_date, finish_date , require = tmp[0] , tmp[1] , tmp[2] , tmp[3] ,tmp[4] , tmp[5]
		
		xiadan(  sub_project_id , reformat_date(finish_date) , dutyer , require , reformat_date(start_date) , project_name)
		print(tmp , 'ok')
if __name__ == '__main__':
	main()


	
	
	

	

	

