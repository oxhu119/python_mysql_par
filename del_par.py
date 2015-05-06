# -*- coding: cp936 -*-
# 本程序用来删除bs_detail表中超92天及大于当前日期的分区
#2015-04-28 humengjun@julong.cc

import MySQLdb as mdb
import sys

con = mdb.connect('localhost', 'root', '123456', 'boc')

with con:
    cur=con.cursor()
    cur.execute('''select partition_name from information_schema.partitions \
where table_name=\'bs_detail\' and (to_days(substring(partition_name,2,8 )\
)<to_days(now())-92 or to_days(substring(partition_name,2,8 ))>to_days(now()))\
''')
    rows=cur.fetchall()
    try:
        if len(rows)==0 :
            if raw_input("没有分区需要清理，按回车（Enter）键继续... "):
                sys.exit()
        else:
            for row in rows:
                cur.execute('alter table bs_detail drop partition %s' %row)
                print '分区%s已删除' %row
            if raw_input("分区清理结束，共清理分区%s个，按回车（Enter）键继续... " %len(rows)):
                sys.exit()
            
    except Exception,e:
        print e
