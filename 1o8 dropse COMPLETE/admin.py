# om ganganpatay namah
# om namah shivay
# jai shri ram
# 1o8 Dropse ADMIN balaji by RS Enterprises

import customtkinter
import tkinter
import datetime
import csv
import re
import pandas as pd

def admin():  
  def delete_emp():
    global emp_data
    grabbed=treev_total_data.focus()#to get the data of the row selected
    values=treev_total_data.item(grabbed,"values")
    
    string=f"Are you sure you want to remove {values[3]} {values[0]}\n Doing this will remove all his details permanently"
    ans=tkinter.messagebox.askyesno("Remove Employee",string,icon="warning")
    if ans:
      selection=treev_total_data.selection()#to get the selected the row
      treev_total_data.delete(selection)
      emp_data= emp_data.loc[emp_data["CID"]!=values[3]]
      emp_data.to_csv("emp_dropse_data.csv",index=False)
      emp_data=pd.read_csv("emp_dropse_data.csv")
      employee_detail()
  
  # clearing the trees for projects
  def clear_p():
    for records in late_data.get_children():
      late_data.delete(records)
    for records in done_data.get_children():
      done_data.delete(records)
    for records in pending_data.get_children():
      pending_data.delete(records)
      
  # ckearing the trees for emp data
  def clear():
    for records in treev_total_data.get_children():
      treev_total_data.delete(records)
  
  # adding tghe employees
  def employee():
    global emp_data
    ans=tkinter.messagebox.askyesno("Add Employee","Are you sure you want to add the employee \n Doing this will let him use this software\n so cross check all the details",icon="warning")
    if ans:
      name_=cname.get().strip()
      email_=cemail.get().strip()
      phone_=ph.get().strip()
      com_id_=cid.get().strip()
      password_=pw.get().strip()
      data=[name_,email_,phone_,com_id_,password_]
      for i in data:
        if i=="":
          submit_status.configure(text="error-fill all fields")
          return
      data=[email_]
      pattern=r"^[\d a-z]?\w+[\.]?\w+@+\w+\.+\w+[\.]?\w+"
      for i in data:
        if re.match(pattern,i):
          pass
        else:
          submit_status.configure(text="error-emails")
          return
      if len(phone_)==10:
        for i in phone_:
          if i in [str(j) for j in range(0,10)]:
            pass
          else:
            submit_status.configure(text="error-phone number integers")
            return
      else:
        submit_status.configure(text="error-phone no. len not 10")
        return
      data=emp_data.loc[emp_data["CID"]==com_id_]
      if not data.empty:
        submit_status.configure(text="this cid exists")
        return
      data=emp_data.loc[emp_data["PHONE"]==int(phone_)]
      if not data.empty:
        submit_status.configure(text="this phone number exists")
        return
      data=[name_,email_,phone_,com_id_,password_,phone_+"@"+"dropse"+name_[1:5],datetime.datetime.now().strftime("%-m/%-d/%y"),0]
      with open("emp_dropse_data.csv","a") as file:
        datawriter=csv.writer(file)
        datawriter.writerow(data)
      #CLEANING THE ENTRY FIELDS
      widgets=[cname,cemail,ph,cid,pw]
      for i in widgets:
        i.delete(0,"end")
      # UPDATING THE LABEL
      submit_status.configure(text="ADDED")
      emp_data=pd.read_csv("emp_dropse_data.csv")
      employee_detail()
    
  # SHOWING employee detail
  def employee_detail():
    global data_
    try:
      clear()
    except:
      None
    data_=emp_data
    treev_total_data["column"] = list(data_.columns)
    treev_total_data["show"] = "headings"
    for column in treev_total_data["columns"]:
        treev_total_data.heading(column, text=column) # let the column heading = column name
    
    df_rows = data_.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        treev_total_data.insert("", 0, values=row)#0 since adding at the end
  
  # work details
  def work_detail():
    try:
      clear_p()
    except:
      None
    workdata_=work_data
  
    # pending
    
    workdata_pending=workdata_.loc[workdata_["STATUS"]==1]
    pending_data["column"] = list(workdata_pending.columns)
    pending_data["show"] = "headings"
    for column in pending_data["columns"]:
        pending_data.heading(column, text=column) # let the column heading = column name
    
    df_rows = workdata_pending.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        pending_data.insert("", 0, values=row)#0 since adding at the end
    
    # done
    
    workdata_done=workdata_.loc[workdata_["STATUS"]==0]
    done_data["column"] = list(workdata_done.columns)
    done_data["show"] = "headings"
    for column in done_data["columns"]:
        done_data.heading(column, text=column) # let the column heading = column name
    
    df_rows = workdata_done.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        done_data.insert("", 0, values=row)#0 since adding at the end
  
    # late_data
    def strip(str_data):
      list=str_data.split("/")
      time=datetime.datetime(int(list[2]),int(list[0]),int(list[1])).strftime("%m/%d/%y")
      time=datetime.datetime.strptime(f"{time}","%m/%d/%y")
      return time
      # it is done since directly doing was giving error that %r format is not defined
    today=datetime.datetime.now().strftime("%-m/%-d/%y")
    today=datetime.datetime.strptime(f"{today}","%m/%d/%y")
    workdata_late=workdata_.loc[(workdata_["STATUS"]==1) &(work_data["END"].apply(strip)<today)]
    late_data["column"]=list(workdata_late.columns)
    late_data["show"]="headings"
    for column in late_data["columns"]:
        late_data.heading(column, text=column) # let the column heading = column name
    
    df_rows = workdata_late.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        late_data.insert("", 0, values=row)#0 since adding at the end
    
    
    # updating total label
    total_projects_pending_label.configure(text=f"{len(workdata_pending)}")
    total_projects_done_label.configure(text=f"{len(workdata_done)}")
    total_projects_late_label.configure(text=f"{len(workdata_late)}")
  
    # getting emp info
    emp_search_tag=emp_search.get()
    if len(emp_search_tag)!=0:
      workdata_pending_len=len(workdata_pending.loc[workdata_pending["EMP ID"]==emp_search_tag])
      workdata_done_len=len(workdata_done.loc[workdata_done["EMP ID"]==emp_search_tag])
      workdata_late_len=len(workdata_late.loc[workdata_late["EMP ID"]==emp_search_tag])
      pending_label.configure(text=workdata_pending_len)
      done_label.configure(text=workdata_done_len)
      late_label.configure(text=workdata_late_len)
      if not emp_data.loc[emp_data["USERNAME"]==emp_search_tag,"EMAIL"].empty:
        email_label_tag=emp_data.loc[emp_data["USERNAME"]==emp_search_tag,"EMAIL"].values[0]#since index and datatype will also be printed if not done
        email_label.configure(text=email_label_tag) 
      else:
        email_label.configure(text="not exist") 
      if not emp_data.loc[emp_data["USERNAME"]==emp_search_tag,"NAME"].empty:
        name_label_tag=emp_data.loc[emp_data["USERNAME"]==emp_search_tag,"NAME"].values[0]#since index and datatype will also be printed if not done
        name_label.configure(text=name_label_tag) 
      else:
        name_label.configure(text="not exist")#since values[0] will give error if the dataframe is of size 0         
      username_label.configure(text=emp_search_tag)
    else:
      pass

  # closing window
  def confirm():
    ans=tkinter.messagebox.askyesno("Eit","Want to Exit! \n you will be logged out")
    if ans:
      root.destroy()
  # making the root
  customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
  customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
  
  root=customtkinter.CTk()
  root.title("1o8 Dropse ADMIN Balaji")
  Width= root.winfo_screenwidth()#
  Height= root.winfo_screenheight()# both doe
  root.geometry("%dx%d" % (Width, Height))
  root.config(padx=10,pady=10)
  font=("Times New Roman",15,"bold")
  
  top_frame = tkinter.Frame(root,bg="#333333")
  top_frame.place(relwidth=1,height=50)
  
  total_data_frame = customtkinter.CTkFrame(root)
  total_data_frame.place(relx=0,rely=0.12,relwidth=0.52,relheight=0.88)
  
  right_tabs = customtkinter.CTkTabview(root)
  right_tabs.place(relx=0.53,rely=0.12,relwidth=0.47,relheight=0.88)
  
  right_tabs.add("Details")
  right_tabs.add("Pending")
  right_tabs.add("Done")
  right_tabs.add("Going late")
  right_tabs.add("Add employee")
  
  pending_frame=customtkinter.CTkFrame(right_tabs.tab("Pending"))
  pending_frame.place(relheight=1,relwidth=1)
  done_frame=customtkinter.CTkFrame(right_tabs.tab("Done"))
  done_frame.place(relheight=1,relwidth=1)
  late_frame=customtkinter.CTkFrame(right_tabs.tab("Going late"))
  late_frame.place(relheight=1,relwidth=1)
  
  # top_frame
  
  top_frame.configure(padx=2,pady=2)
  customtkinter.CTkLabel(top_frame,text="RS Enterprises",font=font).grid(row=0,column=0,padx=20, pady=0)
  customtkinter.CTkLabel(top_frame,text="1o8 Dropse",font=font).grid(row=0,column=1,padx=20, pady=10)
  customtkinter.CTkButton(top_frame,text="Delete employee",font=font,command=delete_emp).grid(row=0,column=2,padx=20, pady=10)
  emp_search= customtkinter.CTkEntry(top_frame, placeholder_text="emp username",width=250)
  emp_search.grid(row=0, column=3,padx=20, pady=10)
  customtkinter.CTkButton(top_frame,text="search",font=font,command=work_detail).grid(row=0,column=4,padx=20, pady=10)
  customtkinter.CTkLabel(top_frame,text="Jai Shri Ram",font=font).grid(row=0,column=5,padx=20,pady=10)
  
  # details
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="Hi! Balaji",font=font).grid(row=0,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="Total Projects Pending",font=font).grid(row=1,column=0)
  total_projects_pending_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  total_projects_pending_label.grid(row=1,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="Total Projects Done",font=font).grid(row=2,column=0)
  total_projects_done_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  total_projects_done_label.grid(row=2,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="Total Projects late",font=font).grid(row=3,column=0)
  total_projects_late_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  total_projects_late_label.grid(row=3,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="-----------------------",font=font).grid(row=4,column=0)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="Username",font=font).grid(row=5,column=0)
  username_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  username_label.grid(row=5,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="email",font=font).grid(row=6,column=0)
  email_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  email_label.grid(row=6,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="name",font=font).grid(row=7,column=0)
  name_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  name_label.grid(row=7,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="projects done",font=font).grid(row=8,column=0)
  done_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  done_label.grid(row=8,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="projects pending",font=font).grid(row=9,column=0)
  pending_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  pending_label.grid(row=9,column=1)
  customtkinter.CTkLabel(right_tabs.tab("Details"),text="projects late",font=font).grid(row=10,column=0)
  late_label=customtkinter.CTkLabel(right_tabs.tab("Details"),text="",font=font)
  late_label.grid(row=10,column=1)
  # adding the employee tab
  
  customtkinter.CTkLabel(right_tabs.tab("Add employee"),text="name",font=font).grid(row=0,column=0)
  cname = customtkinter.CTkEntry(right_tabs.tab("Add employee"), placeholder_text="name",width=240)
  cname.grid(row=0, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add employee"),text="email",font=font).grid(row=1,column=0)
  cemail = customtkinter.CTkEntry(right_tabs.tab("Add employee"), placeholder_text="email",width=240)
  cemail.grid(row=1, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add employee"),text="phone number",font=font).grid(row=2,column=0)
  ph = customtkinter.CTkEntry(right_tabs.tab("Add employee"), placeholder_text="phone number",width=240)
  ph.grid(row=2, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add employee"),text="company emp id",font=font).grid(row=3,column=0)
  cid = customtkinter.CTkEntry(right_tabs.tab("Add employee"), placeholder_text="company emp id",width=240)
  cid.grid(row=3, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add employee"),text="password",font=font).grid(row=4,column=0)
  pw = customtkinter.CTkEntry(right_tabs.tab("Add employee"), placeholder_text="password",show="*",width=240)
  pw.grid(row=4, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkButton(right_tabs.tab("Add employee"),command=employee,text="Submit").grid(row=5,column=1)
  submit_status=customtkinter.CTkLabel(right_tabs.tab("Add employee"),text="---------",font=font)
  submit_status.grid(row=6,column=1)
  
  # tree for total emp
  treev_total_data = tkinter.ttk.Treeview(total_data_frame, selectmode ='browse')#extended helps to select multiple and none to none
  treev_total_data.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(total_data_frame, orient="vertical", command=treev_total_data.yview)#command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(total_data_frame, orient="horizontal", command=treev_total_data.xview)#command means update xaxis view of the widget
  treev_total_data.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
  treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
  treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
  
  # tree for pending
  
  pending_data = tkinter.ttk.Treeview(pending_frame, selectmode ='browse')#extended helps to select multiple and none to none
  pending_data.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(pending_frame, orient="vertical", command=pending_data.yview)#command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(pending_frame, orient="horizontal", command=pending_data.xview)#command means update xaxis view of the widget
  pending_data.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
  treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
  treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
  
  # tree for done
  
  done_data = tkinter.ttk.Treeview(done_frame, selectmode ='browse')#extended helps to select multiple and none to none
  done_data.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(done_frame, orient="vertical", command=done_data.yview)#command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(done_frame, orient="horizontal", command=done_data.xview)#command means update xaxis view of the widget
  done_data.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
  treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
  treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
  
  # tree for late
  
  late_data = tkinter.ttk.Treeview(late_frame, selectmode ='browse')#extended helps to select multiple and none to none
  late_data.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(late_frame, orient="vertical", command=late_data.yview)#command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(late_frame, orient="horizontal", command=late_data.xview)#command means update xaxis view of the widget
  late_data.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
  treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
  treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
  
  # styling the tree view
  style = tkinter.ttk.Style(root)
  style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")
  
  style.map('Treeview',background=[('selected',"red")])#to change the color of selected
  # 
  # 
  global emp_data
  emp_data=pd.read_csv("emp_dropse_data.csv")
  employee_detail()

  global work_data
  work_data=pd.read_csv("data.csv")
  work_detail()
  root.protocol("WM_DELETE_WINDOW",confirm)
  root.mainloop()

if __name__=="__main__":
  admin()