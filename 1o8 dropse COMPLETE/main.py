#om ganganpatay namah
#har har mahadev
#jai shri ram
# Sutantra Dropse login by RS Enterprises

import customtkinter
import tkinter
import datetime
import csv
import pandas as pd
from PIL import ImageTk, Image
import admin
import staff_work

def login():
  emp_data_login=pd.read_csv("emp_dropse_data.csv")
  un=username.get()
  pw=password.get()
  DATA=emp_data_login.loc[(emp_data_login["USERNAME"]==un) &(emp_data_login["PASSWORD"]==pw)] 
  if not(DATA.empty):
    login_page.destroy()
    staff_work.staff_work(un)
    
  elif un=="admin@jaishriram" and pw==merachabhi:
    login_page.destroy()
    admin.admin()
  else:
    login_label.configure(text="wrong credentials")
  



customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

login_page=customtkinter.CTk()
login_page.title("1o8 Dropse login")
login_page.geometry("400x300")
login_page.config(padx=10,pady=10)
login_page.resizable(False,False)#to fix the width and height and disabing the maximize button
font=("Times New Roman",15,"bold")
login_page.configure(padx=20,pady=20)
# frames
main_frame=customtkinter.CTkFrame(login_page)
main_frame.place(x=0,y=0,relheight=1,relwidth=1)
# entry boxes and button
merachabhi="jaishriram4871"
customtkinter.CTkLabel(main_frame,text="Username",font=font).grid(row=0,column=0,padx=(20, 0), pady=(20, 20))
customtkinter.CTkLabel(main_frame,text="password",font=font).grid(row=1,column=0,padx=(20, 0), pady=(20, 20))
username=customtkinter.CTkEntry(main_frame,placeholder_text="username",width=210)
username.grid(row=0,column=1,padx=(20, 0), pady=(20, 20))
password=customtkinter.CTkEntry(main_frame,placeholder_text="password",show="*",width=210)
password.grid(row=1,column=1,padx=(20, 0), pady=(20, 20))

customtkinter.CTkButton(main_frame,text="Login",command=login).grid(row=3,column=1,padx=(20, 0), pady=(20, 20))

login_label=customtkinter.CTkLabel(main_frame,text="",font=font)
login_label.grid(row=4,column=1,padx=(20, 0), pady=(20, 20))

login_page.mainloop()