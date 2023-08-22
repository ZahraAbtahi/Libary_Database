# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk
import pandas as pd
import tkinter as tk
from awesometkinter.bidirender import add_bidi_support, render_text
import pyodbc


class connection:
    def __init__(self,servername,database):
        self.servername = servername
        self.database = database

    def connect(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=' + self.servername + ''
                        'Database=' + self.database + ''
                        'Trusted_Connection=yes;')
        cursor = conn.cursor()

        return (cursor,conn)

class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x550")
        self.master.configure(bg='#219ebc')
        self.master.title('کتابخانه')
        self.id = 1
        self.mainpage = self.login

        self.pfont_label = ('B Nazanin',12,'bold')
        self.pfont_button = ('B Nazanin',10,'bold')
        self.pfont_entry = ('B Nazanin',12)
        self.pfont_check = ('B Nazanin',10,'bold')
        self.login()
    
    def open_connection(self):
        c = connection('DESKTOP-L786VIN\LETGO;','library;')
        cursor,conn = c.connect()
        return cursor,conn
    
    def close_connection(self,cursor,conn):
        cursor.close()
        conn.close()
    
    def login(self):
        def check_login():
            found = 0
            mod = ismod.get()
            u,p = user.get(),passw.get()
            if(len(u) == 0 and len(p)==0):
                return

            cursor,c = self.open_connection()
            if(mod):
                cursor.execute('select * from moderator where moderatorid='+u+' and password='+p)
                
            else:
                cursor.execute('select * from member where memberid='+u+' and password='+p)
            
            for num, recode in enumerate(cursor, start=1):
                if(num==1):
                    found = 1
                elif(num>1):
                    found = 0
                    break
            
            if(mod and found):
                self.id = u
                self.moderator()
            elif(mod==0 and found):
                self.id = u
                self.member()
            
            self.close_connection(cursor,c)
        user = tk.StringVar()
        passw = tk.StringVar()
        ismod = tk.IntVar()
        for i in self.master.winfo_children():
            i.destroy()
        
        self.frame1 = Frame(self.master, bg = '#219ebc')
        self.frame1.pack(side=LEFT, expand = 1, pady = 10, padx = 10)

        self.l1 = Label(self.frame1, text = "نام کاربری",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 0, column = 2, sticky = E, pady = 2,padx=1)

        self.l2 = Label(self.frame1, text = "رمزعبور",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 2, sticky = E, pady = 2,padx=1)

        self.e1 = Entry(self.frame1, textvariable=user, width=20,font=self.pfont_entry,fg='#03045e').grid(row = 0, column = 0, pady = 2,padx=2)
        self.e2 = Entry(self.frame1, textvariable=passw, width=20,font=self.pfont_entry,fg='#03045e',show='*').grid(row = 1, column = 0, pady = 2,padx=2)

        self.b1 = Button(self.frame1,command=lambda: check_login(), text = "ورود",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 3, column = 2, sticky = S, pady = 5,padx=1)
        self.b2 = Button(self.frame1,command=self.not_Member ,text = "عضو نیستم",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 3, column = 1, sticky = S, pady = 5,padx=1)

        self.c1 = Checkbutton(self.frame1, variable=ismod,text = "مسئول هستم",bg = "#219ebc",fg='#03045e',font=self.pfont_check,activebackground='#219ebc',activeforeground='#03045e').grid(row = 2, column = 0, sticky = W, columnspan = 2, pady = 1,padx=1)
    
    def not_Member(self):
        def search(lb):
            query = "select title,sectorname,publicationname,publicationdate,a.name,a.family from author as a, book as b where b.bookid = a.bookid"
            a,b,c = author.get(),book.get(),section.get()
            if(len(a)):
                query += " and a.family = N'"+a+"' "
            if(len(b)):
                query += " and title = N'"+b+"' "
            if(len(c)):
                query += " and sectorname = N'"+c+"' "
            cursor,c = self.open_connection()
            cursor.execute(query)
            self.put_intobox(lb,cursor)
            self.close_connection(cursor,c)
        
        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = Frame(self.master,bg = '#219ebc')
        self.frame2.pack()

        cursor,c = self.open_connection()
        sectors = []
        lib = []

        cursor.execute('SELECT * FROM sector')
        sectors = cursor.fetchall()

        for i in range(len(sectors)):
            sectors[i] = sectors[i].sectorname
        cursor.execute('SELECT * FROM CentralLibary')
        lib = cursor.fetchone()
        
        self.close_connection(cursor,c)

        author = tk.StringVar()
        book = tk.StringVar()
        section = tk.StringVar()

        self.b1 = Button(self.frame2,command=self.mainpage ,text = "برگشت",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 0, sticky = NW, pady = (5,20), padx=1)

        self.b2 = Button(self.frame2, command=lambda: search(self.lb1), text = "مشاهده نتایج", font=self.pfont_button, width=10, bg='#1d3557', fg='#a8dadc', activebackground='#a8dadc', activeforeground='#03045e').grid(row = 5, column = 3, sticky = W, pady = (25,5),padx=(10,5),columnspan=1)
        self.cmb1 = ttk.Combobox(self.frame2, textvariable=section, font=self.pfont_check, width=20, values=sectors).grid(row = 5, column = 1, sticky=W, pady = (25,5),padx=(1,2),columnspan=2)
        self.l1 = Label(self.frame2, width=5, text = ":نام بخش",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 5, column = 2, sticky = W, pady = (25,5),padx=(2,2),columnspan=1)
        
        self.l12 = Label(self.frame2, width=5, text = ":نویسنده" ,bg = "#219ebc", fg='#03045e',font=self.pfont_label).grid(row = 6, column = 2, sticky = W, pady = 2,padx=(1,5),columnspan=1)
        self.l13 = Label(self.frame2, width=5, text = ":نام کتاب", bg = "#219ebc", fg='#03045e',font=self.pfont_label).grid(row = 6, column = 4, sticky = W, pady = 2,padx=(1,5),columnspan=1)
        self.e1 = Entry(self.frame2, textvariable=author,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 6, column = 1, pady = 2,sticky = W,padx=(1,1),columnspan=1)
        self.e2 = Entry(self.frame2, textvariable=book,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 6, column = 3, pady = 2,sticky = W,padx=(5,1),columnspan=1)

        self.lb1 = Listbox(self.frame2, font=self.pfont_check, width=70, fg='#a8dadc')
        self.lb1.grid(row = 7, column = 1, sticky = W, pady = (20,5), padx=1, columnspan=5, rowspan=4)
        
        self.l2 = Label(self.frame2, text = "کتاب ها",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 7, column = 4, sticky = NW, pady = (20,2),padx=2,columnspan=1)
        self.l3 = Label(self.frame2, text = "::اطلاعات کتابخانه",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 3, sticky = NE, pady = 2,padx=(10,5))
        self.l4 = Label(self.frame2, text = ":نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 2, sticky = E, pady = 2,padx=2)
        self.l5 = Label(self.frame2, text = ":آدرس",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 2, sticky = E, pady = 2,padx=2)
        self.l6 = Label(self.frame2, text = ":تلفن",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 2, sticky = E, pady = 2,padx=2)
        self.l7 = Label(self.frame2, text = ":تعداد اعضا",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 4, column = 2, sticky = E, pady = 2,padx=2)

        self.l8 = Label(self.frame2, text = lib[0],bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 1, sticky = W, pady = 2,padx=2)
        self.l9 = Label(self.frame2, text = lib[1],bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 1, sticky = W, pady = 2,padx=2)
        self.l10 = Label(self.frame2, text = lib[2],bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 1, sticky = W, pady = 2,padx=2)
        self.l11 = Label(self.frame2, text = lib[3],bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 4, column = 1, sticky = W, pady = 2,padx=2)
    
    def member(self):
        def change_page(self,name):
            for i in self.master.winfo_children():
                i.destroy()
            self.frame3 = Frame(self.master,bg = '#219ebc')
            self.frame3.pack()

            if(name == "search_book"):
                search_book(self,self.frame3)
            elif(name == "main"):
                main(self,self.frame3)
        
        def search_book(self,frame3):
            def search(lb):
                query = "select title,sectorname,publicationname,publicationdate,a.name,a.family from author as a, book as b ,translator as tr where b.bookid = a.bookid and tr.bookid = b.bookid"
                a,b,c,d,e,f,g = num.get(),name.get(),pubname.get(),date.get(),section.get(),wr.get(),tr.get()
                if(len(a)):
                    query += " and b.bookid = N'"+a+"' "
                if(len(b)):
                    query += " and title = N'"+b+"' "
                if(len(c)):
                    query += " and publicationname = N'"+c+"' "
                if(len(d)):
                    query += " and publicationdate = N'"+d+"' "
                if(len(e)):
                    query += " and sectorname = N'"+e+"' "
                if(len(f)):
                    query += " and a.family = N'"+f+"' "
                if(len(g)):
                    query += " and tr.family = N'"+g+"' "

                cursor,c = self.open_connection()
                cursor.execute(query)
                self.put_intobox(lb,cursor)
                self.close_connection(cursor,c)
            num = tk.StringVar()
            name = tk.StringVar()
            pubname = tk.StringVar()
            date = tk.StringVar()
            section = tk.StringVar()
            wr = tk.StringVar()
            tr = tk.StringVar()

            cursor,c = self.open_connection()
            sectors = []
            cursor.execute('SELECT * FROM sector')
            sectors = cursor.fetchall()
            for i in range(len(sectors)):
                sectors[i] = sectors[i].sectorname
            self.close_connection(cursor,c)

            self.b1 = Button(frame3,command=lambda: change_page(self,"main") ,text = "برگشت",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 0, sticky = NW, pady = (5,20), padx=1)
            
            self.l0 = Label(frame3, text = "مشخصات کتاب",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 5, sticky = W, pady = (20,5),padx=2,columnspan=5)
            self.l1 = Label(frame3, text = ":شماره",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l2 = Label(frame3, text = ":نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 3, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l3 = Label(frame3, text = ":نام انتشارات",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l4 = Label(frame3, text = ":تاریخ انتشار",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l5 = Label(frame3, text = ":نام بخش",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 3, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l6 = Label(frame3, text = ":نویسنده",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l7 = Label(frame3, text = ":مترجم",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 4, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)

            self.e1 = Entry(frame3, width=10, textvariable=num,font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 0, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e2 = Entry(frame3, width=10, textvariable=name,font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 2, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e3 = Entry(frame3, width=10, textvariable=pubname,font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e4 = Entry(frame3, width=10, textvariable=date,font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 0, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.cmb1 = ttk.Combobox(self.frame3, textvariable=section, font=self.pfont_check, width=10, values=sectors).grid(row = 3, column = 2, sticky=W, pady = (5,5),padx=2,columnspan=1)
            self.e6 = Entry(frame3, width=10, textvariable=wr,font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e7 = Entry(frame3, width=10, textvariable=tr,font=self.pfont_entry, fg='#03045e').grid(row = 4, column = 0, pady = (5,5),sticky = W,padx=2,columnspan=1)
            
            self.lb1 = Listbox(frame3, font=self.pfont_check, width=80, fg='#a8dadc')
            self.lb1.grid(row = 5, column = 1, sticky = W, pady = (20,5), padx=1, columnspan=6, rowspan=4)
            self.b1 = Button(frame3,text = "جستجو",command= lambda: search(self.lb1),font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 4, column = 5, sticky = NW, pady = (5,5), padx=1)
            
        def main(self,frame3):
            def res(resv):
                cursor,c = self.open_connection()
                r = resv.get()
                cursor.execute('insert into reservation values ('+str(r)+','+str(self.id)+',GETDATE())')
                c.commit()
                self.close_connection(cursor,c)
                
            def bor(borv):
                cursor,c = self.open_connection()
                cursor.execute('select max(borrowid)+1 as m from Borrow')
                mxborrow = cursor.fetchone()
                b = borv.get()
                cursor.execute('select moderatorid as m from Book b,moderator m where m.sectorname=b.sectorname and bookid = '+str(b))
                mid = cursor.fetchone()
                cursor.execute('insert into borrow (borrowid,bookid,memberid,moderatorid) values ('+str(mxborrow.m)+','+str(b)+','+str(self.id)+','+str(mid.m)+')')
                c.commit()
                self.close_connection(cursor,c)

            cursor,c = self.open_connection()

            cursor.execute('SELECT * FROM member where memberid = '+str(self.id))
            member = cursor.fetchone()
            cursor.execute('select borrowid,b.bookid,sectorname,borrowdate,deliverydate,IsDelivered,approval from borrow as b,member as m,book as bo  where b.bookid=bo.bookid and m.memberid=b.memberid and m.memberid ='+str(self.id))
            borrow = cursor.fetchall()
            self.close_connection(cursor,c)

            self.b0 = Button(frame3,command= self.login ,text = "خروج",font=self.pfont_button,width=10,bg='red',fg='#1d3557',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 0, sticky = N, pady = (5,20), padx=1,columnspan=3)
            self.b1 = Button(frame3,command=lambda: change_page(self,"search_book") ,text = "کتابخانه",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 2, sticky = N, pady = (5,20), padx=1,columnspan=3)
            
            self.l0 = Label(frame3, text = "مشخصات فردی",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 5, sticky = W, pady = (20,5),padx=2,columnspan=6)

            self.l1 = Label(frame3, text = ":نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label,width=8).grid(row = 2, column = 5, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l2 = Label(frame3, text = ":نام خانوادگی",bg = "#219ebc",fg='#03045e',font=self.pfont_label,width=8).grid(row = 2, column = 3, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l3 = Label(frame3, text = ":تلفن",bg = "#219ebc",fg='#03045e',font=self.pfont_label,width=8).grid(row = 2, column = 1, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l4 = Label(frame3, text = ":آدرس",bg = "#219ebc",fg='#03045e',font=self.pfont_label,width=8).grid(row = 3, column = 1, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l5 = Label(frame3, text = ":تاریخ ثبت نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label,width=8).grid(row = 3, column = 3, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l6 = Label(frame3, text = ":تعداد امانت ها",bg = "#219ebc",fg='#03045e',font=self.pfont_label,width=8).grid(row = 3, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l7 = Label(frame3, text = member[1],bg = "#219ebc",fg='#03045e',font=self.pfont_entry,width=8).grid(row = 2, column = 4, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l8 = Label(frame3, text = member[2],bg = "#219ebc",fg='#03045e',font=self.pfont_entry,width=8).grid(row = 2, column = 2, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l9 = Label(frame3, text = member[3],bg = "#219ebc",fg='#03045e',font=self.pfont_entry,width=8).grid(row = 2, column = 0, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l10 = Label(frame3, text = member[4],bg = "#219ebc",fg='#03045e',font=self.pfont_entry,width=8).grid(row = 3, column = 0, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l11 = Label(frame3, text = member[5],bg = "#219ebc",fg='#03045e',font=self.pfont_entry,width=8).grid(row = 3, column = 2, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l12 = Label(frame3, text = member[7],bg = "#219ebc",fg='#03045e',font=self.pfont_entry,width=8).grid(row = 3, column = 4, sticky = E, pady = (5,5),padx=2,columnspan=1)

            self.l12 = Label(frame3, text = ":امانت ها",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 4, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.lb1 = Listbox(frame3, font=self.pfont_check, width=50, fg='#a8dadc')
            self.lb1.grid(row = 4, column = 1, sticky = W, pady = (20,5), padx=1, columnspan=3, rowspan=4)
            self.put_intobox(self.lb1,borrow)

            borv = tk.StringVar()
            resv= tk.StringVar()
            self.l1 = Label(frame3, text = ":(شماره کتاب)رزرو کتاب",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 8, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=2)
            self.e1 = Entry(frame3, textvariable=resv, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 8, column = 3, pady = 2,sticky = W,padx=(1,1),columnspan=1)
            self.b2 = Button(frame3,command=lambda: res(resv) ,text = "رزرو",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 8, column = 2, sticky = NW, pady = (5,5), padx=1,columnspan=1)
            self.l1 = Label(frame3, text = ":(شماره کتاب)امانت کتاب",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 9, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=2)
            self.e1 = Entry(frame3, textvariable=borv, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 9, column = 3, pady = 2,sticky = W,padx=(1,1),columnspan=1)
            self.b2 = Button(frame3,command=lambda: bor(borv) ,text = "امانت گرفتن",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 9, column = 2, sticky = NW, pady = (5,5), padx=1,columnspan=1)

        for i in self.master.winfo_children():
            i.destroy()
        self.frame3 = Frame(self.master,bg = '#219ebc')
        self.frame3.pack()
        main(self,self.frame3)

    def moderator(self):
        def change_page(self,name):
            for i in self.master.winfo_children():
                i.destroy()
            self.frame4 = Frame(self.master,bg = '#219ebc')
            self.frame4.pack()

            if(name == "books"):
                books(self,self.frame4,self.id)
            elif(name == "members"):
                members(self,self.frame4)
            elif(name == "main"):
                main(self,self.frame4,self.id)
            elif(name == "moderators"):
                moderators(self,self.frame4)

        def main(self,frame4,id):
            def accept_request(bor):
                b = bor.get()
                cursor,c = self.open_connection()
                cursor.execute('exec approvalinggg '+str(self.id)+','+b+',1')
                c.commit()
                self.close_connection(cursor,c)

            cursor,c = self.open_connection()
            #cursor.execute("CREATE PROC approvalinggg @modid int, @barid int, @act bit as declare @tmp nvarchar(6); set @tmp = (select moderatorid from borrow where borrowid = @barid);if @tmp = @modid begin UPDATE borrow SET approval = @act WHERE borrowid = @barid;end")
            cursor.execute('SELECT * FROM moderator where moderatorid = '+str(self.id))
            mod = cursor.fetchone()
            cursor.execute("SELECT borrowid,bookid,memberid,sectorname,IsDelivered,approval FROM borrow b, moderator m where m.moderatorid = b.moderatorid and sectorname = N'"+mod[4]+"' and m.moderatorid = "+str(self.id))
            bor = cursor.fetchall()
            self.close_connection(cursor,c)

            acbor = tk.StringVar()

            self.b0 = Button(frame4,command= self.login ,text = "خروج",font=self.pfont_button,width=10,bg='red',fg='#1d3557',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 0, sticky = W, pady = (5,20), padx=1,columnspan=2)
            self.b1 = Button(frame4,command=lambda: change_page(self,"books") ,text = "کتابخانه",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 2, sticky = W, pady = (5,20), padx=1,columnspan=2)
            self.b2 = Button(frame4,command=lambda: change_page(self,"members") ,text = "اعضا",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 4, sticky = W, pady = (5,20), padx=1,columnspan=2)
            if self.boss == 1:
                self.b3 = Button(frame4,command=lambda: change_page(self,"moderators") ,text = "مسئولان",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 5, sticky = E, pady = (5,20), padx=1,columnspan=1)

            self.l0 = Label(frame4, text = "مشخصات فردی",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 5, sticky = W, pady = (20,5),padx=2,columnspan=6)
            self.l1 = Label(frame4, text = ":نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l2 = Label(frame4, text = ":نام خانوادگی",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 3, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l3 = Label(frame4, text = ":تلفن",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 1, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l4 = Label(frame4, text = ":نام بخش",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 1, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l5 = Label(frame4, text = ":نوع فعالیت",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 3, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l6 = Label(frame4, text = mod[1],bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 4, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l7 = Label(frame4, text = mod[2],bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 2, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l8 = Label(frame4, text = mod[3],bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 0, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l9 = Label(frame4, text = mod[4],bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 0, sticky = E, pady = (5,5),padx=2,columnspan=1)
            if self.boss:
                self.l10 = Label(frame4, text = "رییس",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 2, sticky = E, pady = (5,5),padx=2,columnspan=1)
            else:
                self.l10 = Label(frame4, text = "مسئول",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 2, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.l12 = Label(frame4, text = ":درخواست های امانت",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 4, column = 5, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.lb1 = Listbox(frame4, font=self.pfont_check, width=60, fg='#a8dadc')
            self.lb1.grid(row = 4, column = 0, sticky = W, pady = (20,5), padx=1, columnspan=5, rowspan=4)
            self.put_intobox(self.lb1,bor)

            self.l1 = Label(frame4, text = ":شماره درخواست",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 8, column = 5, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.e1 = Entry(frame4, textvariable=acbor,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 8, column = 4, pady = 2,sticky = W,padx=(1,1),columnspan=1)
            self.b4 = Button(frame4,command=lambda: accept_request(acbor) ,text = "تایید",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 8, column = 2, sticky = NW, pady = (5,5), padx=1,columnspan=2)
        
        def members(self,frame4):
            def search_mem(lb):
                query = "select memberid,name,family,phone,registerydate from member where 1=1"
                a,b,c,d,e,f = num.get(),name.get(),lname.get(),date.get(),add.get(),pho.get()
                if(len(a)):
                    query += " and m.memberid = N'"+a+"' "
                if(len(b)):
                    query += " and m.name = N'"+b+"' "
                if(len(c)):
                    query += " and m.family = N'"+c+"' "
                if(len(d)):
                    query += " and registerydate = N'"+d+"' "
                if(len(e)):
                    query += " and address = N'"+e+"' "
                if(len(f)):
                    query += " and phone = N'"+f+"' "

                cursor,c = self.open_connection()
                cursor.execute(query)
                self.put_intobox(lb,cursor)
                self.close_connection(cursor,c)
            
            def add_mem(lb):
                b,h,e,f = name.get(),lname.get(),add.get(),pho.get()
                cursor,c = self.open_connection()
                cursor.execute('select max(memberid)+1 as m from member')
                mxid = cursor.fetchone()
                
                cursor.execute("insert into member(memberid,name,family,registerydate,phone,address) values("+str(mxid.m)+",N'"+str(b)+"',N'"+str(h)+"',GETDATE(),"+str(f)+",N'"+str(e)+"')")
                c.commit()
                cursor.execute('select * from member where memberid ='+str(mxid.m))
                self.put_intobox(lb,cursor)
                self.close_connection(cursor,c)
            
            def del_mem():
                cursor,c = self.open_connection()
                cursor.execute("delete from member where memberid ="+str(dell.get()))
                c.commit()
                self.close_connection(cursor,c)


            num = tk.StringVar()
            name = tk.StringVar()
            lname = tk.StringVar()
            pho = tk.StringVar()
            add = tk.StringVar()
            date = tk.StringVar()
            dell = tk.StringVar()

            self.b1 = Button(frame4,command=lambda: change_page(self,"main") ,text = "برگشت",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 0, sticky = NW, pady = (5,20), padx=1)
            
            self.l0 = Label(frame4, text = "مشخصات عضو",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 5, sticky = W, pady = (20,5),padx=2,columnspan=5)
            self.l1 = Label(frame4, text = ":شماره",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l2 = Label(frame4, text = ":نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l3 = Label(frame4, text = ":نام خانوادگی",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 3, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l4 = Label(frame4, text = ":تلفن",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l5 = Label(frame4, text = ":آدرس",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 3, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l6 = Label(frame4, text = ":تاریخ ثبت نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)

            self.e1 = Entry(frame4, textvariable=num,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 0, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e2 = Entry(frame4, textvariable=name,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e3 = Entry(frame4, textvariable=lname,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 2, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e4 = Entry(frame4, textvariable=pho,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 0, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e5 = Entry(frame4, textvariable=add,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 2, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e6 = Entry(frame4, textvariable=date,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=1)

            self.b2 = Button(frame4,command=lambda: search_mem(self.lb1),text = "جستجو",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 4, column = 5, sticky = NW, pady = (5,5), padx=1)
            self.b3 = Button(frame4,command=lambda: add_mem(self.lb1),text = "اضافه کردن عضو",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 4, column = 4, sticky = NW, pady = (5,5), padx=1)
            self.lb1 = Listbox(frame4, font=self.pfont_check, width=50, fg='#a8dadc')
            self.lb1.grid(row = 5, column = 1, sticky = W, pady = (20,5), padx=1, columnspan=4, rowspan=4)

            self.l1 = Label(frame4, text = ":شماره عضو",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 9, column = 5, sticky = E, pady = (5,5),padx=2,columnspan=1)
            self.e7 = Entry(frame4, textvariable=dell,width=10, font=self.pfont_entry, fg='#03045e').grid(row = 9, column = 4, pady = 2,sticky = E,padx=(1,1),columnspan=1)
            self.b4 = Button(frame4,command=del_mem,text = "حذف کردن عضو",font=self.pfont_button,width=10,bg='red',fg='#1d3557',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 9, column = 3, sticky = NW, pady = (5,5), padx=1)
            
        def books(self,frame4,id):
            self.b1 = Button(frame4,command=lambda: change_page(self,"main") ,text = "برگشت",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 0, sticky = NW, pady = (5,20), padx=1)
            
            self.l0 = Label(frame4, text = "مشخصات کتاب",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 5, sticky = W, pady = (20,5),padx=2,columnspan=5)
            self.l1 = Label(frame4, text = ":شماره",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l2 = Label(frame4, text = ":نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 3, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l3 = Label(frame4, text = ":نام انتشارات",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l4 = Label(frame4, text = ":تاریخ انتشار",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l5 = Label(frame4, text = ":نام بخش",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 3, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l6 = Label(frame4, text = ":نویسنده",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l7 = Label(frame4, text = ":مترجم",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 4, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)

            self.e1 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 0, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e2 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 2, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e3 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e4 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 0, sticky = W, pady = (5,5),padx=2,columnspan=1)
            if(self.boss == False):
                self.l8 = Label(frame4, text = "نام بخش",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 2, sticky = W, pady = (5,5),padx=2,columnspan=1)
            else:
                self.e5 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 2, pady = (5,5),sticky = W,padx=2,columnspan=1)
            self.e6 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e7 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 4, column = 0, pady = (5,5),sticky = W,padx=2,columnspan=1)
            
            self.b2 = Button(frame4,text = "جستجو",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 4, column = 5, sticky = NW, pady = (5,5), padx=1)
            self.b3 = Button(frame4,text = "اضافه کردن کتاب",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 4, column = 4, sticky = NW, pady = (5,5), padx=1)
            self.b4 = Button(frame4,text = "حذف کردن کتاب",font=self.pfont_button,width=10,bg='red',fg='#1d3557',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 4, column = 4, sticky = NW, pady = (5,5), padx=1)
            self.Lb1 = Listbox(frame4, font=self.pfont_check, width=50, fg='#a8dadc').grid(row = 5, column = 1, sticky = W, pady = (20,5), padx=1, columnspan=4, rowspan=4)

            self.b5 = Button(frame4,text = "حذف کتاب های قدیمی",font=self.pfont_button,width=20,bg='red',fg='#1d3557',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 9, column = 4, sticky = E, pady = (5,5), padx=1,columnspan=2)

        def moderators(self,frame4):
            self.b1 = Button(frame4,command=lambda: change_page(self,"main") ,text = "برگشت",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 0, column = 0, sticky = NW, pady = (5,20), padx=1)
            
            self.l0 = Label(frame4, text = "مشخصات مسئول",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 1, column = 5, sticky = W, pady = (20,5),padx=2,columnspan=5)
            self.l1 = Label(frame4, text = ":شماره",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l2 = Label(frame4, text = ":نام",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 5, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l3 = Label(frame4, text = ":نام خانوادگی",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 2, column = 3, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l4 = Label(frame4, text = ":تلفن",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 1, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.l5 = Label(frame4, text = ":نام بخش",bg = "#219ebc",fg='#03045e',font=self.pfont_label).grid(row = 3, column = 3, sticky = W, pady = (5,5),padx=2,columnspan=1)

            self.e1 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 0, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e2 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 4, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e3 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 2, column = 2, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e4 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 0, sticky = W, pady = (5,5),padx=2,columnspan=1)
            self.e5 = Entry(frame4, width=10, font=self.pfont_entry, fg='#03045e').grid(row = 3, column = 2, sticky = W, pady = (5,5),padx=2,columnspan=1)

            self.b2 = Button(frame4,text = "جستجو",font=self.pfont_button,width=10,bg='#1d3557',fg='#a8dadc',activebackground='#a8dadc',activeforeground='#03045e').grid(row = 4, column = 5, sticky = NW, pady = (5,5), padx=1)
            self.Lb1 = Listbox(frame4, font=self.pfont_check, width=50, fg='#a8dadc').grid(row = 5, column = 1, sticky = W, pady = (20,5), padx=1, columnspan=4, rowspan=4)
        
        cursor,c = self.open_connection()
        cursor.execute('select isboss from moderator where moderatorid = '+str(self.id))
        self.boss = cursor.fetchone().isboss
        self.close_connection(cursor,c)

        for i in self.master.winfo_children():
            i.destroy()
        self.frame4 = Frame(self.master,bg = '#219ebc')
        self.frame4.pack()
        main(self,self.frame4,self.id)

    def put_intobox(self,lb,arr):
        lb.delete(0,END)
        for num, recode in enumerate(arr, start=1):
            lb.insert(num,recode)



root = Tk()
app(root)
root.mainloop()
