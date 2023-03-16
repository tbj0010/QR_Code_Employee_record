from tkinter import *
import qrcode
from PIL import Image,ImageTk
from resizeimage import resizeimage
from tkinter import ttk, messagebox
import mysql.connector

class Qr_Generator:
    def __init__(self,root):
        self.root = root
        self.root.geometry("900x500+200+50")
        self.root.title('QR Generator | Developed by TBJ')
        self.root.resizable(False,False)

        title = Label(self.root,text='    Employee Information Form',font=('times new roman',40),bg='#053246',fg='white',anchor='w').place(x=0,y=0,relwidth=3)

        self.var_empid=StringVar()
        self.var_name=StringVar()
        self.var_mobile=StringVar()
        self.var_salary=StringVar()
        
        emp_frame = Frame(self.root,bd=2,relief=RIDGE,bg='white')
        emp_frame.place(x=50,y=100,width=500,height=380)

        emp_title = Label(emp_frame,text='Employee Detail',font=('goudy old style',20),bg='#043256',fg='white').place(x=0,y=0,relwidth=1)

        lbl_emp = Label(emp_frame,text='Employee ID :',font=('times new roman',15,'bold'),bg='white').place(x=20,y=60)
        lbl_emp1 = Label(emp_frame,text='Name :',font=('times new roman',15,'bold'),bg='white').place(x=20,y=100)
        lbl_emp2 = Label(emp_frame,text='Mobile No. :',font=('times new roman',15,'bold'),bg='white').place(x=20,y=140)
        lbl_emp3 = Label(emp_frame,text='Salary :',font=('times new roman',15,'bold'),bg='white').place(x=20,y=180)

        txt_emp = Entry(emp_frame,textvariable=self.var_empid,font=('times new roman',15),bg='lightyellow').place(x=200,y=60)
        txt_emp1 = Entry(emp_frame,textvariable=self.var_name,font=('times new roman',15),bg='lightyellow').place(x=200,y=100)
        txt_emp2 = Entry(emp_frame,textvariable=self.var_mobile,font=('times new roman',15),bg='lightyellow').place(x=200,y=140)
        txt_emp3 = Entry(emp_frame,textvariable=self.var_salary,font=('times new roman',15),bg='lightyellow').place(x=200,y=180)

        btn_generate = Button(emp_frame,text='QR Generate',font=('times new roman',18),command=self.generate,bg='#2196f2',fg='white').place(x=90,y=230,width=180,height=30)
        btn_clear = Button(emp_frame,text='clear',font=('times new roman',18),command=self.clear,bg='#607d8b',fg='white').place(x=280,y=230,width=120,height=30)
        btn_Insert = Button(emp_frame,text='Insert',font=('times new roman',18),command=self.Add,bg='#2196f2',fg='white').place(x=90,y=270,width=100,height=30)
        btn_Update = Button(emp_frame,text='Update',font=('times new roman',18),command=self.update,bg='#2196f2',fg='white').place(x=200,y=270,width=90,height=30)
        btn_Delete = Button(emp_frame,text='Delete',font=('times new roman',18),command=self.delete,bg='#2196f2',fg='white').place(x=300,y=270,width=100,height=30)

        self.msg = ''
        self.lbl_msg = Label(emp_frame,text=self.msg,font=('times new roman',20,'bold'),bg='white',fg='green')
        self.lbl_msg.place(x=0,y=310,relwidth=1)

        self.qr_frame = Frame(self.root,bd=2,relief=RIDGE,bg='white')
        self.qr_frame.place(x=600,y=100,width=250,height=380)

        qr_title = Label(self.qr_frame,text='Employee QR Code',font=('goudy old style',20),bg='#043256',fg='white').place(x=0,y=0,relwidth=1)

        self.qr_code = Label(self.qr_frame,text='No QR\nAvailable',font=('times new roman',15),bg='#3f51b5',fg='white',bd=1,relief=RIDGE)
        self.qr_code.place(x=35,y=60,width=180,height=180)

        lbl1_msg = Label(self.qr_frame,text='ID     :',font=('times new roman',10,'bold'),bg='white')
        lbl1_msg.place(x=35,y=250)
        lbl2_msg = Label(self.qr_frame,text='Name   :',font=('times new roman',10,'bold'),bg='white')
        lbl2_msg.place(x=35,y=280)
        lbl3_msg = Label(self.qr_frame,text='Mobile :',font=('times new roman',10,'bold'),bg='white')
        lbl3_msg.place(x=35,y=310)
        lbl4_msg = Label(self.qr_frame,text='Salary :',font=('times new roman',10,'bold'),bg='white')
        lbl4_msg.place(x=35,y=340)
        
    def Add(self):
        idd = self.var_empid.get()
        empnamee = self.var_name.get()
        mobilee = self.var_mobile.get()
        salaryy = self.var_salary.get()
     
        mysqldb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jonty"
            )
        mycursor=mysqldb.cursor()
     
        try:
           sql = "INSERT INTO  emp_info (id,empname,mobile,salary) VALUES (%s, %s, %s, %s)"
           val = (idd,empnamee,mobilee,salaryy)
           mycursor.execute(sql, val)
           mysqldb.commit()
           lastid = mycursor.lastrowid
           messagebox.showinfo("information", "Employee inserted successfully...")
           self.var_empid.delete(0, END)
           self.var_name.delete(0, END)
           self.var_mobile.delete(0, END)
           self.var_salary.delete(0, END)
           self.var_empid.focus_set()
        except Exception as e:
           print(e)
           mysqldb.rollback()
           mysqldb.close()

    def update(self):
        idd = self.var_empid.get()
        empnamee = self.var_name.get()
        mobilee = self.var_mobile.get()
        salaryy = self.var_salary.get()
     
        mysqldb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jonty"
            )
        mycursor=mysqldb.cursor()
     
        try:
           sql = "Update  emp_info set empname= %s,mobile= %s,salary= %s where id= %s"
           val = (empnamee,mobilee,salaryy,idd)
           mycursor.execute(sql, val)
           mysqldb.commit()
           lastid = mycursor.lastrowid
           messagebox.showinfo("information", "Record Updateddddd successfully...")
     
           self.var_empid.delete(0, END)
           self.var_name.delete(0, END)
           self.var_mobile.delete(0, END)
           self.var_salary.delete(0, END)
           self.var_empid.focus_set()
     
        except Exception as e:
           print(e)
           mysqldb.rollback()
           mysqldb.close()

    def delete(self):
        idd = self.var_empid.get()
     
        mysqldb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jonty"
            )
        mycursor=mysqldb.cursor()
     
        try:
            
            sql = "delete from emp_info where id = %s"
            val = (idd,)
            mycursor.execute(sql, val)
            mysqldb.commit()
            lastid = mycursor.lastrowid
            messagebox.showinfo("information", "Record Deleteeeee successfully...")
     
            self.var_empid.delete(0, END)
            self.var_name.delete(0, END)
            self.var_mobile.delete(0, END)
            self.var_salary.delete(0, END)
            self.var_empid.focus_set()

        except Exception as e:
            print(e)
            mysqldb.rollback()
            mysqldb.close()
 

    def clear(self):
        self.var_empid.set('')
        self.var_name.set('')
        self.var_mobile.set('')
        self.var_salary.set('')

        self.msg = ''
        self.lbl_msg.config(text=self.msg)
        self.qr_code.config(image='')
        

    def generate(self):
        idd = self.var_empid.get()
        empnamee = self.var_name.get()
        mobilee = self.var_mobile.get()
        salaryy = self.var_salary.get()
        if self.var_empid.get()=='' or self.var_name.get()=='' or self.var_mobile.get()=='' or self.var_salary.get()=='':
            self.msg = 'All Fields Are Mendatory!!'
            self.lbl_msg.config(text=self.msg,fg='red')
        else:
            qr_data=(f'Employee ID:{self.var_empid.get()}\nName:{self.var_name.get()}\nMobile No.:{self.var_mobile.get()}\nSalary:{self.var_salary.get()}')
            qr_code=qrcode.make(qr_data)
            print(qr_code)
            qr_code=resizeimage.resize_cover(qr_code,[180,180])
            qr_code.save('Emp_'+str(self.var_empid.get())+'.png')
            
            self.im=ImageTk.PhotoImage(file='Emp_'+str(self.var_empid.get())+'.png')
            self.qr_code.config(image=self.im)
            
            self.msg = 'QR Generated Successfully!!!'
            self.lbl_msg.config(text=self.msg,fg='green')

        lbl5_msg = Label(self.qr_frame,text=self.var_empid.get(),font=('times new roman',10,'bold'),bg='white')
        lbl5_msg.place(x=85,y=250)
        lbl6_msg = Label(self.qr_frame,text=self.var_name.get(),font=('times new roman',10,'bold'),bg='white')
        lbl6_msg.place(x=85,y=280)
        lbl7_msg = Label(self.qr_frame,text=self.var_mobile.get(),font=('times new roman',10,'bold'),bg='white')
        lbl7_msg.place(x=85,y=310)
        lbl8_msg = Label(self.qr_frame,text=self.var_salary.get(),font=('times new roman',10,'bold'),bg='white')
        lbl8_msg.place(x=85,y=340)

        
root = Tk()
obj = Qr_Generator(root)
root.mainloop()
        
    
