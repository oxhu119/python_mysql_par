# -*- coding: cp936 -*-
# ��������������bs_detail��������ؽ�����
#2015-04-28 humengjun@julong.cc

import MySQLdb as mdb
import sys

con = mdb.connect('localhost', 'root', '123456', 'boc')

with con:
    cur=con.cursor()
    cur.execute('''
SELECT  PARTITION_NAME from information_schema.PARTITIONS where table_name=\'bs_detail\'
''')
    rows=cur.fetchall()
    try:
        if len(rows)==0 :
            if raw_input("���ݿ�bs_detail���������Ϊ0�����ѯ������������س���Enter��������... "):
                sys.exit()
        else:
            par_list=[]
            days_list=[]
            name_plus=[]
            par_list=[','.join(row) for row in rows]
            days_list=[par[1:5]+'-'+par[5:7]+'-'+par[7:9] for par in par_list]
##            print par_list
##            print days_list
            for i in range(len(par_list)):
                name_plus.append('partition '+par_list[i]+' values in (to_days(\''+days_list[i]+'\'))')
##            print name_plus
            sql_begin='alter table boc.bs_detail partition by list (to_days(dt_busi))('
            sql_end=');'
            sql_rows=','.join(name_plus)
            sql_dropPK='alter table boc.bs_detail drop primary key;'
            sql_addPK='alter table boc.bs_detail add primary key(bank_no,storehouse_no,dt_busi,guid)'
##            print sql_rows
            result=sql_begin+sql_rows+sql_end
##            print result
            print '��ʼ����������������һ��ʾǰ�벻Ҫ�ж�...'
            cur.execute(result)
            print '����������ɣ���ʼ��������...'
            cur.execute(sql_dropPK)
            cur.execute(sql_addPK)
            print '�����������!'
            if raw_input("���ݿ��Ѿ��������س���Enter��������... "):
                sys.exit()
    except Exception,e:
        print e
