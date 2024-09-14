from tkinter import *
import qrcode
from PIL import Image,ImageTk
from resizeimage import resizeimage
from tkinter import ttk, messagebox
import mysql.connector
import uuid
import random
import string


class Qr_Generator:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x500+200+50")
        self.root.title('QR Generator | Developed by TBJ')
        self.root.resizable(False, False)

        title = Label(self.root, text='Employee Information Form', font=('times new roman', 40), bg='#053246', fg='white', anchor='w').place(x=0, y=0, relwidth=1)

        # Variables
        self.var_empid = StringVar()  # Employee ID
        self.var_name = StringVar()   # Employee Name
        self.var_mobile = StringVar()  # Employee Mobile
        self.var_salary = StringVar()  # Employee Salary

        # Employee Frame
        emp_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        emp_frame.place(x=50, y=100, width=500, height=380)

        emp_title = Label(emp_frame, text='Employee Detail', font=('goudy old style', 20), bg='#043256', fg='white').place(x=0, y=0, relwidth=1)

        # Employee ID Input Field (Read-only, auto-generated after data insertion)
        lbl_empid = Label(emp_frame, text='Employee ID:', font=('times new roman', 15, 'bold'), bg='white').place(x=20, y=100)
        txt_empid = Entry(emp_frame, textvariable=self.var_empid, font=('times new roman', 15), bg='lightyellow', state='readonly')
        txt_empid.place(x=200, y=100)


        lbl_name = Label(emp_frame, text='Name:', font=('times new roman', 15, 'bold'), bg='white').place(x=20, y=140)
        txt_name = Entry(emp_frame, textvariable=self.var_name, font=('times new roman', 15), bg='lightyellow').place(x=200, y=140)

        lbl_mobile = Label(emp_frame, text='Mobile No.:', font=('times new roman', 15, 'bold'), bg='white').place(x=20, y=180)
        txt_mobile = Entry(emp_frame, textvariable=self.var_mobile, font=('times new roman', 15), bg='lightyellow').place(x=200, y=180)

        lbl_salary = Label(emp_frame, text='Salary:', font=('times new roman', 15, 'bold'), bg='white').place(x=20, y=220)
        txt_salary = Entry(emp_frame, textvariable=self.var_salary, font=('times new roman', 15), bg='lightyellow').place(x=200, y=220)

        # Employee Search Input Field for Retrieving Data
        lbl_search_id = Label(emp_frame, text='Search by Emp. ID:', font=('times new roman', 15, 'bold'), bg='white').place(x=20, y=60)
        self.var_search_id = StringVar()
        txt_search_id = Entry(emp_frame, textvariable=self.var_search_id, font=('times new roman', 15), bg='lightyellow')
        txt_search_id.place(x=200, y=60)

        # Button to trigger the retrieval of employee data based on the search ID
        btn_search = Button(emp_frame, text='Search', font=('times new roman', 15), command=self.retrieve_data, bg='#2196f2', fg='white')
        btn_search.place(x=410, y=60, width=70, height=25)

        
        # Add Buttons
        btn_generate = Button(emp_frame, text='QR Generate', font=('times new roman', 18), command=self.generate, bg='#2196f2', fg='white').place(x=90, y=249, width=180, height=30)
        btn_clear = Button(emp_frame, text='Clear', font=('times new roman', 18), command=self.clear, bg='#607d8b', fg='white').place(x=280, y=249, width=120, height=30)
        btn_insert = Button(emp_frame, text='Insert', font=('times new roman', 18), command=self.Add, bg='#2196f2', fg='white').place(x=90, y=280, width=100, height=30)
        btn_update = Button(emp_frame, text='Update', font=('times new roman', 18), command=self.update, bg='#2196f2', fg='white').place(x=200, y=280, width=90, height=30)
        btn_delete = Button(emp_frame, text='Delete', font=('times new roman', 18), command=self.delete, bg='#2196f2', fg='white').place(x=300, y=280, width=100, height=30)

        # Refresh button to retrieve employee data by ID
        # btn_refresh = Button(emp_frame, text='Refresh', font=('times new roman', 15), command=self.clear, bg='#607d8b', fg='white')
        # btn_refresh.place(x=400, y=270)


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
        
        self.lbl5_msg = Label(self.qr_frame, text='', font=('times new roman', 10, 'bold'), bg='white')
        self.lbl5_msg.place(x=85, y=250)

        self.lbl6_msg = Label(self.qr_frame, text='', font=('times new roman', 10, 'bold'), bg='white')
        self.lbl6_msg.place(x=85, y=280)

        self.lbl7_msg = Label(self.qr_frame, text='', font=('times new roman', 10, 'bold'), bg='white')
        self.lbl7_msg.place(x=85, y=310)

        self.lbl8_msg = Label(self.qr_frame, text='', font=('times new roman', 10, 'bold'), bg='white')
        self.lbl8_msg.place(x=85, y=340)
        
    def generate_emp_id(self):
        # Generate a random 4-digit number
        digits = ''.join(random.choices(string.digits, k=4))
        
        # Generate a random uppercase letter
        letter = random.choice(string.ascii_uppercase)
        
        # Combine the digits and letter to form the Employee ID
        emp_id = digits + letter
        return emp_id

        
    def retrieve_data(self):
        emp_id = self.var_search_id.get()  # Get the entered Employee ID

        if emp_id == '':
            messagebox.showerror("Error", "Please enter an Employee ID to search")
            return

        mysqldb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jonty"
        )
        mycursor = mysqldb.cursor()

        try:
            # Fetch employee details by Employee ID
            sql_select = "SELECT empname, mobile, salary FROM emp_info WHERE id = %s"
            mycursor.execute(sql_select, (emp_id,))
            row = mycursor.fetchone()

            if row:
                self.var_empid.set(emp_id)  # Set the Employee ID in the readonly field
                self.var_name.set(row[0])   # Set the name
                self.var_mobile.set(row[1])  # Set the mobile
                self.var_salary.set(row[2])  # Set the salary
                self.msg = "Data retrieved successfully!"
            else:
                messagebox.showerror("Error", "No employee found with this ID")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
        finally:
            mysqldb.close()

        
    def Add(self):
        # Generate a new Employee ID (4 digits + 1 letter)
        new_emp_id = self.generate_emp_id() 
    
        # self.var_empid.set(emp_id)  # Set the generated UUID to the Employee ID field

        empnamee = self.var_name.get()
        mobilee = self.var_mobile.get()
        salaryy = self.var_salary.get()

        mysqldb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jonty"
        )
        mycursor = mysqldb.cursor()

        # Create the table if it doesn't exist
        try:
            sql_create_table = """CREATE TABLE IF NOT EXISTS emp_info (
                            id VARCHAR(5) PRIMARY KEY,
                            empname VARCHAR(100),
                            mobile VARCHAR(15),
                            salary DECIMAL(10,2)
                        );
                        """
            mycursor.execute(sql_create_table)
            mysqldb.commit()
        except Exception as e:
            print(e)
            mysqldb.rollback()
            mysqldb.close()
        
        # Insert data into the table
        try:
            sql_insert = "INSERT INTO emp_info (id, empname, mobile, salary) VALUES (%s, %s, %s, %s)"
            val = (new_emp_id, empnamee, mobilee, salaryy)
            mycursor.execute(sql_insert, val)
            mysqldb.commit()
            messagebox.showinfo("information", "Employee inserted successfully")

            # Clear the form fields after successful insertion
            self.var_empid.set(new_emp_id)  # Display the generated Employee ID (read-only field)
            self.var_name.set('')
            self.var_mobile.set('')
            self.var_salary.set('')
            self.var_empid.focus_set()

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            mysqldb.rollback()
        finally:
            mysqldb.close()

    def update(self):
        emp_id = self.var_empid.get()  # Get the Employee ID from the readonly field
        empnamee = self.var_name.get()
        mobilee = self.var_mobile.get()
        salaryy = self.var_salary.get()

        if emp_id == '':
            messagebox.showerror("Error", "No Employee ID found to update")
            return

        mysqldb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jonty"
        )
        mycursor = mysqldb.cursor()

        try:
            # Update employee details
            sql_update = "UPDATE emp_info SET empname = %s, mobile = %s, salary = %s WHERE id = %s"
            val = (empnamee, mobilee, salaryy, emp_id)
            mycursor.execute(sql_update, val)
            mysqldb.commit()
            messagebox.showinfo("information", "Employee updated successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            mysqldb.rollback()
        finally:
            mysqldb.close()


    def delete(self):
        emp_id = self.var_empid.get()  # Get the Employee ID from the readonly field

        if emp_id == '':
            messagebox.showerror("Error", "No Employee ID found to delete")
            return

        mysqldb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jonty"
        )
        mycursor = mysqldb.cursor()

        try:
            # Delete employee record
            sql_delete = "DELETE FROM emp_info WHERE id = %s"
            mycursor.execute(sql_delete, (emp_id,))
            mysqldb.commit()
            messagebox.showinfo("information", "Employee deleted successfully")
            self.clear()  # Clear the form fields after deletion

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            mysqldb.rollback()
        finally:
            mysqldb.close()


    

    def clear(self):
        self.var_search_id.set('')
        self.var_empid.set('')
        self.var_name.set('')
        self.var_mobile.set('')
        self.var_salary.set('')
        
        self.lbl5_msg.config(text="")
        self.lbl6_msg.config(text="")
        self.lbl7_msg.config(text="")
        self.lbl8_msg.config(text="")

        self.msg = ''
        self.lbl_msg.config(text=self.msg)
        self.qr_code.config(image='')
        

    def generate(self):
        idd = self.var_empid.get()
        empnamee = self.var_name.get()
        mobilee = self.var_mobile.get()
        salaryy = self.var_salary.get()
        if self.var_name.get()=='' or self.var_mobile.get()=='' or self.var_salary.get()=='':
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

            self.lbl5_msg.config(text=self.var_empid.get())
            self.lbl6_msg.config(text=self.var_name.get())
            self.lbl7_msg.config(text=self.var_mobile.get())
            self.lbl8_msg.config(text=self.var_salary.get())

        
root = Tk()
obj = Qr_Generator(root)
root.mainloop()
        
    
