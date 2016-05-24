awk '{print "update PROJECT set BACKUP_DATE=\""$2"\" where REPORT_ID=\""$1"\";"}' mm
peew
awk '{print "update PROJECT set BOOL_SEQ=\""$2"\" where REPORT_ID=\""$1"\";"}' mm
