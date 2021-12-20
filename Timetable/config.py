import sys
import pymysql
import tkinter as tk
import tkinter.messagebox as popup


try:
    mysqlobj = pymysql.connect(host='remotemysql.com',
                            port=3306,
                            user='QMb15ojgak',
                            password='YBv2VEPTM3',
                            db='QMb15ojgak',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)


    cursorobj = mysqlobj.cursor()
    cursorobj.execute('USE QMb15ojgak')

except Exception:
    tk.Tk().withdraw() #hides the extra tkinter root window created when popup is executed
    popup.showerror('ERROR', 'Could not connect to database: QMb15ojgak')
    sys.exit()         #to stop execution if connection not established
