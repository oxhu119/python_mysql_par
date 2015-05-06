# -*- coding: cp936 -*-
# ����������ɾ��bs_detail���г�92�켰���ڵ�ǰ���ڵķ���
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
            if raw_input("û�з�����Ҫ�������س���Enter��������... "):
                sys.exit()
        else:
            for row in rows:
                cur.execute('alter table bs_detail drop partition %s' %row)
                print '����%s��ɾ��' %row
            if raw_input("����������������������%s�������س���Enter��������... " %len(rows)):
                sys.exit()
            
    except Exception,e:
        print e
