#coding:utf-8
'''
Created on 2019/7/14

@author: rickon
'''

import sqlite3
import os

def exec_sql(filepath):
    pathdir = os.listdir(filepath)
    for dir in pathdir:
        if os.path.splitext(dir)[1] == '.sql':
            try:
                db = sqlite3.connect('../db.sqlite3')
                cur = db.cursor()
                with open(dir, 'r+',encoding='utf8') as f:
                    sql_list = f.read().split(';')[:-1]
                    sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]
                    for sql_item in sql_list:
                        #print(sql_item)
                        cur.execute(sql_item)
            except Exception as e:
                print(e)
            finally:
                cur.close()
                db.commit()
                db.close()


if __name__ == "__main__":
    exec_sql('.')