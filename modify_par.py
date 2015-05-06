# -*- coding: cp936 -*-
# 本程序用来调整bs_detail表分区并重建主键
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
            if raw_input("数据库bs_detail表分区数量为0，请查询分区情况，按回车（Enter）键继续... "):
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
            print '开始调整分区，出现下一提示前请不要中断...'
            cur.execute(result)
            print '分区调整完成，开始调整主键...'
            cur.execute(sql_dropPK)
            cur.execute(sql_addPK)
            print '主键调整完成!'
            if raw_input("数据库已就绪，按回车（Enter）键继续... "):
                sys.exit()
    except Exception,e:
        print e
