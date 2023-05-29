# om ganganpatay namah
# om namah shivay
# jai shri ram
# Sutantra Dropse by RS Enterprises

import customtkinter
import tkinter
import datetime
import csv
import re
import pandas as pd
from PIL import ImageTk, Image
from tkcalendar import Calendar
# pip install tkcalendar

empcode="294453241933@29oct"
# important note
def important_note():
  tkinter.messagebox.showinfo("Information","*-->When same clients are available then check if  projects are different \n if different click YES otherwise NO")
# clearing the trees
def clear():
  for records in treev_total_data.get_children():
    treev_total_data.delete(records)
  for records in treev_today.get_children():
    treev_today.delete(records)
  for records in treev_tomorrow.get_children():
    treev_tomorrow.delete(records)

# data entry function
def Submit():
  global end_date_flag,data
  name=cname.get().strip()
  email=cemail.get().strip()
  text=textbox.get("1.0","end-1c").strip()
  fees=fee.get().strip()
  freename=fname.get().strip()
  freeemail=femail.get().strip()
  commis=commission.get().strip()
  ans=tkinter.messagebox.askyesno("Add Project","Are you sure you want to add this project\n Check the details carefully",icon="warning")
  if ans:
    data_c=data.loc[(data["CLIENT EMAIL"]==email) & (data["STATUS"]==1)]
    if not data_c.empty:
      email_query=tkinter.messagebox.askyesnocancel("Email exits already",f"client email exists with {data_c['EMP ID'].values}, \n contact them and then write very carefully")
      if email_query:
        pass
      else:
        submit_status.configure(text="error-client email exists",font=font)
        return
    # CHECKING IF DETAILS ARE THERE OR NOT
    data123=[name,text,freename,fees,commis,freeemail,email]
    for i in data123:
      if i=="" or i==" ":
        submit_status.configure(text="error-fill all fields",font=font)
        return
    data123=[fees,commis]
    for i in data123:
      for j in i:
        if j in [str(a) for a in range(0,10)] or j in ["."]:
          pass
        else:
          submit_status.configure(text="error-number field",font=font)
          return
    data123=[freeemail,email]
    pattern=r"^[\d a-z]?\w+[\.]?\w+@+\w+\.+\w+[\.]?\w+"
    for i in data123:
      if re.match(pattern,i):
        pass
      else:
        submit_status.configure(text="error-emails",font=font)
        return
    if end_date_flag==1:
      submit_status.configure(text="error-set deadline",font=font)
      return
    else:
        end=str(cal.get_date().strip())
  # WRITING INTO CSV
    data123=[name,email,text,fees,freename,commis,freeemail,datetime.datetime.now().strftime("%-m/%-d/%y"),end,empcode,1]
    with open("data.csv","a") as file:
      datawriter=csv.writer(file)
      datawriter.writerow(data123)
    #CLEANING THE ENTRY FIELDS
    widgets=[cname,cemail,fee,fname,commission,femail]
    for i in widgets:
      i.delete(0,"end")
    textbox.delete("1.0","end-1c")#to empty the text box
    end_date.configure(text="MM/DD/YYYY")
    # UPDATING THE LABEL
    submit_status.configure(text="ADDED")
    end_date_flag=1
    data=pd.read_csv("data.csv")
    show_data()

#date picker
def date_picker():
  global cal
  cal_root=customtkinter.CTk()
  cal_root.title("Choose deadline date")
  cal_root.geometry("300x300")
  cal = Calendar(cal_root, selectmode = 'day',
               year = int(datetime.datetime.now().strftime("%Y")),
               month = int(datetime.datetime.now().strftime("%m")),
               day = int(datetime.datetime.now().strftime("%d")))
  cal.pack()
  def date_ok():
    global end_date_flag
    end_date.configure(text=f"{cal.get_date()}")
    end_date_flag=0
    cal_root.destroy()
  customtkinter.CTkButton(cal_root,text="ok",command=date_ok).pack()
  cal_root.mainloop()

# displaying data
def show_data():
  global data_
  try:
    clear()
  except:
    None
  data_=data.loc[(data["EMP ID"]==empcode) & (data["STATUS"]==1)]
  
  today=datetime.datetime.now().strftime("%-m/%-d/%y")
  today_data=data_.loc[data["END"]==str(today)][["CLIENT NAME","CLIENT EMAIL","PROJECT","FREELANCER","FREELANCER EMAIL"]]
  
  tomorrow=datetime.datetime.now()+datetime.timedelta(days=1)
  tomorrow=tomorrow.strftime("%-m/%-d/%y")
  tomorrow_data=data_.loc[data["END"]==str(tomorrow)][["CLIENT NAME","CLIENT EMAIL","PROJECT","FREELANCER","FREELANCER EMAIL"]]


  #updating the total data frame
  treev_total_data["column"] = list(data_.columns)
  treev_total_data["show"] = "headings"
  for column in treev_total_data["columns"]:
      treev_total_data.heading(column, text=column) # let the column heading = column name
  
  df_rows = data_.to_numpy().tolist() # turns the dataframe into a list of lists
  for row in df_rows:
      treev_total_data.insert("", 0, values=row)#0 since adding at the end
    
  # updating the tomorrow frame
  treev_tomorrow["column"] = list(tomorrow_data.columns)
  treev_tomorrow["show"] = "headings"
  for column in treev_tomorrow["columns"]:
      treev_tomorrow.heading(column, text=column) # let the column heading = column name
  
  df_rows = tomorrow_data.to_numpy().tolist() # turns the dataframe into a list of lists
  for row in df_rows:
      treev_tomorrow.insert("", 0, values=row)##0 since adding at the end
  #updating the today frame
  treev_today["column"] = list(today_data.columns)
  treev_today["show"] = "headings"
  for column in treev_today["columns"]:
      treev_today.heading(column, text=column) # let the column heading = column name
  
  df_rows = today_data.to_numpy().tolist() # turns the dataframe into a list of lists
  for row in df_rows:
      treev_today.insert("", 0, values=row)#0 since adding at the end
   #updating the late frame
  def strip(str_data):
    list=str_data.split("/")
    time=datetime.datetime(int(list[2]),int(list[0]),int(list[1])).strftime("%m/%d/%y")
    time=datetime.datetime.strptime(f"{time}","%m/%d/%y")
    return time
    # it is done since directly doing was giving error that %r format is not defined
  today=datetime.datetime.strptime(f"{today}","%m/%d/%y")
  workdata_late=data_.loc[(data_["END"].apply(strip)<today)]
  treev_late["column"]=list(workdata_late.columns)
  treev_late["show"]="headings"
  for column in treev_late["columns"]:
      treev_late.heading(column, text=column) # let the column heading = column name
  
  df_rows = workdata_late.to_numpy().tolist() # turns the dataframe into a list of lists
  for row in df_rows:
      treev_late.insert("", 0, values=row)#0 since adding at the end

  total_projects_label_pending.configure(text=f"{len(data_)}")
  total_projects_label_tomorrow.configure(text=f"{len(tomorrow_data)}")
  total_projects_label_today.configure(text=f"{len(today_data)}")
  total_projects_label_late.configure(text=f"{len(workdata_late)}")

# deleting one Resource
def delete_one():
  global data
  ans=tkinter.messagebox.askyesno("Task done","Are you sure this task is done be sure",icon="warning")
  if ans:
    grabbed=treev_total_data.focus()#to get the data of the row selected
    values=treev_total_data.item(grabbed,"values")
    selection=treev_total_data.selection()#to get the selected the row
    treev_total_data.delete(selection)
    data.loc[(data["CLIENT NAME"]==values[0])&(data["CLIENT EMAIL"]==values[1])&(data["PROJECT"]==values[2])&((data["FEE"]==int(values[3])) | (data["FEE"]==float(values[3])))&(data["FREELANCER"]==values[4])&((data["COMMISSION"]==int(values[5]))|(data["COMMISSION"]==float(values[5])))&(data["FREELANCER EMAIL"]==values[6])&(data["START"]==values[7])&(data["END"]==values[8])&(data["EMP ID"]==values[9])&(data["STATUS"]==1),"STATUS"]=0
    data.to_csv("data.csv",index=False)
    data=pd.read_csv("data.csv")
    show_data()
  
# deleting multiple
def delete_all():
  global data
  ans=tkinter.messagebox.askyesno("All task done","Are you sure that all these tasksare done",icon="warning")
  if ans:
    data.loc[(data["EMP ID"]==empcode)&(data["STATUS"]==1),"STATUS"]=0
    for records in treev_total_data.get_children():
      treev_total_data.delete(records)
    data.to_csv("data.csv",index=False)
    data=pd.read_csv("data.csv")
    show_data()

# closing the window
def confirm():
  ans=tkinter.messagebox.askyesno("exit","Are you sure you want to LOGOUT",icon="warning")
  if ans:
    root.destroy()

# changing the password
def change_pw():
  def change():
    old_password=old_pw.get()
    new_password=new_pw.get()
    pw_change_data=pd.read_csv("emp_dropse_data.csv")
    pw_check_data=pw_change_data.loc[(pw_change_data["PASSWORD"]==old_password)&(pw_change_data["USERNAME"]==empcode)]
    if pw_check_data.empty:
      tkinter.messagebox.showerror("Password not matched","old password not matched")
      old_pw.delete(0,"end")
    else:
      pw_change_data.loc[(pw_change_data["PASSWORD"]==old_password)&(pw_change_data["USERNAME"]==empcode),"PASSWORD"]=new_password
      pw_change_data.to_csv("emp_dropse_data.csv",index=False)
      pw_root.destroy()
      tkinter.messagebox.showinfo("changed","password changed")
  pw_root=customtkinter.CTk()
  pw_root.title("change password")
  pw_root.geometry("280x200")
  pw_root.configure(padx=10,pady=10)
  pw_root.resizable(False,False)
  pw_frame=customtkinter.CTkFrame(pw_root)
  pw_frame.place(relheight=1,relwidth=1)
  old_pw=customtkinter.CTkEntry(pw_frame,placeholder_text="write old password",show="*",width=240)
  old_pw.grid(row=0, column=0,padx=(5, 0), pady=(5, 5))
  new_pw=customtkinter.CTkEntry(pw_frame,placeholder_text="write new password",show="*",width=240)
  new_pw.grid(row=1, column=0,padx=(5, 0), pady=(5, 5))
  customtkinter.CTkButton(pw_frame,text="Change",font=font,command=change).grid(row=2,column=0,padx=(5, 0), pady=(5, 5))

# making the root
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root=customtkinter.CTk()
root.title("Sutantra Dropse")
Width= root.winfo_screenwidth()#
Height= root.winfo_screenheight()# both doe
root.geometry("%dx%d" % (Width, Height))
root.config(padx=10,pady=10)
font=("Times New Roman",15,"bold")
# making the frames
top_frame = tkinter.Frame(root,bg="#333333")
top_frame.place(relwidth=1,height=50)

total_data_frame = customtkinter.CTkFrame(root)
total_data_frame.place(relx=0,rely=0.12,relwidth=0.52,relheight=0.88)

right_tabs = customtkinter.CTkTabview(root)
right_tabs.place(relx=0.53,rely=0.12,relwidth=0.47,relheight=0.88)

right_tabs.add("Namaskar!")
right_tabs.add("Today")
right_tabs.add("Tomorrow")
right_tabs.add("Late")
right_tabs.add("Add Project")

today_frame=customtkinter.CTkFrame(right_tabs.tab("Today"))# CAN BE making a tab scrollable
today_frame.place(relheight=1,relwidth=1)

tomorrow_frame=customtkinter.CTkFrame(right_tabs.tab("Tomorrow"))# CAN BE making a tab scrollable
tomorrow_frame.place(relheight=1,relwidth=1)

late_frame=customtkinter.CTkFrame(right_tabs.tab("Late"))# CAN BE making a tab scrollable
late_frame.place(relheight=1,relwidth=1)
# top frame
top_frame.configure(padx=2,pady=2)
img=Image.open("logo.PNG")
img=img.resize((50,47))
img = ImageTk.PhotoImage(img)#HighDPI displays error
label = customtkinter.CTkLabel(top_frame, image = img,text="")
label.grid(row=0,column=0,padx=20, pady=0)
customtkinter.CTkLabel(top_frame,text="Sutantra Dropse",font=font).grid(row=0,column=1,padx=20, pady=10)
customtkinter.CTkButton(top_frame,text="Task completed",font=font,command=delete_one).grid(row=0,column=2,padx=20, pady=10)
customtkinter.CTkButton(top_frame,text="All Task completed",font=font,command=delete_all).grid(row=0,column=3,padx=20, pady=10)
customtkinter.CTkButton(top_frame,text="Important note",font=font,command=important_note).grid(row=0,column=4,padx=20, pady=10)
customtkinter.CTkButton(top_frame,text="Change password",font=font,command=change_pw).grid(row=0,column=5,padx=20, pady=10)

#namaskar
customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text=empcode,font=font).grid(row=0,column=0,padx=20, pady=10)
customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text="total projects pending",font=font).grid(row=1,column=0,padx=20, pady=10)
customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text="total projects for today",font=font).grid(row=2,column=0,padx=20, pady=10)
customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text="total projects for tomorrow",font=font).grid(row=3,column=0,padx=20, pady=10)
customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text="total late projects",font=font).grid(row=4,column=0,padx=20, pady=10)
total_projects_label_pending=customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text="",font=font)
total_projects_label_pending.grid(row=1,column=1,padx=20, pady=10)
total_projects_label_tomorrow=customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text="",font=font)
total_projects_label_tomorrow.grid(row=3,column=1,padx=20, pady=10)
total_projects_label_today=customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text="",font=font)
total_projects_label_today.grid(row=2,column=1,padx=20, pady=10)
total_projects_label_late=customtkinter.CTkLabel(right_tabs.tab("Namaskar!"),text="",font=font)
total_projects_label_late.grid(row=4,column=1,padx=20, pady=10)


#add project


customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="client name",font=font).grid(row=0,column=0)
cname = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="client name",width=240)
cname.grid(row=0, column=1,padx=(5, 0), pady=(5, 5))

customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="client email",font=font).grid(row=1,column=0)
cemail = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="client email",width=240)
cemail.grid(row=1, column=1,padx=(5, 0), pady=(5, 5))

customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="project",font=font).grid(row=2,column=0)
textbox = customtkinter.CTkTextbox(right_tabs.tab("Add Project"), width=250,height=100)
textbox.grid(row=2, column=1, padx=(20, 0), pady=(20, 0))

customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="fee $",font=font).grid(row=3,column=0)
fee = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="fee",width=240)
fee.grid(row=3, column=1,padx=(5, 0), pady=(5, 5))

customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="freelancer",font=font).grid(row=4,column=0)
fname = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="freelancer name",width=240)
fname.grid(row=4, column=1,padx=(5, 0), pady=(5, 5))

customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="freelancer commission %",font=font).grid(row=5,column=0)
commission = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="commission",width=240)
commission.grid(row=5, column=1,padx=(5, 0), pady=(5, 5))

customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="freelancer email",font=font).grid(row=6,column=0)
femail = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="freelancer email",width=240)
femail.grid(row=6, column=1,padx=(5, 0), pady=(5, 5))

end_date_flag=1
customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="deadline end",font=font).grid(row=7,column=0)
end_date=customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="MM/DD/YYYY",font=font)
end_date.grid(row=7,column=1)
customtkinter.CTkButton(right_tabs.tab("Add Project"),command=date_picker,text="Pick Date").grid(row=7,column=2)

customtkinter.CTkButton(right_tabs.tab("Add Project"),command=Submit,text="Submit").grid(row=8,column=1)
submit_status=customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="---------",font=font)
submit_status.grid(row=9,column=1)


# total data frame
treev_total_data = tkinter.ttk.Treeview(total_data_frame, selectmode ='browse')#extended helps to select multiple and none to none
treev_total_data.place(relheight=1, relwidth=1)

treescrolly = tkinter.Scrollbar(total_data_frame, orient="vertical", command=treev_total_data.yview) # command means update the yaxis view of the widget
treescrollx = tkinter.Scrollbar(total_data_frame, orient="horizontal", command=treev_total_data.xview) # command means update the xaxis view of the widget
treev_total_data.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
  
# today_frame
treev_today = tkinter.ttk.Treeview(today_frame, selectmode ='browse')#extended helps to select multiple and none to none
treev_today.place(relheight=1, relwidth=1)

treescrolly = tkinter.Scrollbar(today_frame, orient="vertical", command=treev_today.yview) # command means update the yaxis view of the widget
treescrollx = tkinter.Scrollbar(today_frame, orient="horizontal", command=treev_today.xview) # command means update the xaxis view of the widget
treev_today.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
# tomorrow_frame
treev_tomorrow = tkinter.ttk.Treeview(tomorrow_frame, selectmode ='browse')#extended helps to select multiple and none to none
treev_tomorrow.place(relheight=1, relwidth=1)

treescrolly = tkinter.Scrollbar(tomorrow_frame, orient="vertical", command=treev_tomorrow.yview) # command means update the yaxis view of the widget
treescrollx = tkinter.Scrollbar(tomorrow_frame, orient="horizontal", command=treev_tomorrow.xview) # command means update the xaxis view of the widget
treev_tomorrow.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
# late_frame
treev_late = tkinter.ttk.Treeview(late_frame, selectmode ='browse')#extended helps to select multiple and none to none
treev_late.place(relheight=1, relwidth=1)

treescrolly = tkinter.Scrollbar(late_frame, orient="vertical", command=treev_late.yview) # command means update the yaxis view of the widget
treescrollx = tkinter.Scrollbar(late_frame, orient="horizontal", command=treev_late.xview) # command means update the xaxis view of the widget
treev_late.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
# styling the tree view
style = tkinter.ttk.Style(root)
style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")

style.map('Treeview',background=[('selected',"red")])#to change the color of selected

data=pd.read_csv("data.csv")
show_data()

root.protocol("WM_DELETE_WINDOW",confirm)
root.mainloop()
