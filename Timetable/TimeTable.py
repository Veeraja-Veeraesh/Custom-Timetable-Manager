#importing modules required
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as popup
import tkcalendar as tkcal
import addevent as ae
import config as sql

#initializing global variables
x, y = 80, 180  # for position of timetables for different dates
dateoftable = ''
dateslist = []  # contains all the dates for which tables have been made
btnnumber = 0   # the numeric id of the button on the root window

#stores information about the buttons in the root window
# stores values as {'btnobject1':[tkinter button object, date of table]}
btnobjdict = dict()

#creating the main window
root = tk.Tk()
root.title("Time Table")
root.geometry("1200x800")
root.resizable(False, False)
root.configure(bg='#082032')


#creating the styles for the buttons on the root window
style = ttk.Style()
style.theme_use('clam')
style.configure('root.TButton', background='#F0A500', foreground='white',
                borderwidth=3, focuscolor='white',
                font=('Bahnschrift SemiBold SemiCondensed', 13))
# for color change on mouse hover
style.map('root.TButton', background=[('active', '#ffc547')])


#button to create/update a new table
updatebtn = ttk.Button(root, text="+ Update Table", style='root.TButton')
updatebtn.place(x=525, y=50, width=150, height=50)

#retrieving the data stored in timetablebtn
sql.cursorobj.execute("SELECT * FROM timetablebtn ORDER BY sno")
records = sql.cursorobj.fetchall()

for row in records:

    #each row looks like this: {'sno': 1, 'btnobject': 'btnobject1', 'tabledate': '01-01-2021'}
    
    btnobj = row['btnobject']   #stores the values corresponding to the 'btnobject' key
    btnnumber = row['sno']      #stores the values corresponding to the 'sno' key

    btnobjdict[btnobj] = [ttk.Button(root, style='root.TButton'), row['tabledate']]
    btnobjdict[btnobj][0].place(x=x, y=y, width=150, height=120)
    btnobjdict[btnobj][0].configure(text=f'Table No: {row["sno"]} \nDate: {row["tabledate"]}')

    #boundary conditions to place each button at the specified location and update once the button is placed
    if x >= 900:
        x = 80
        y += 150
    else:
      x += 180


#function opens a new window to choose date and updates specified button in main window to that date
def updatetable():
    global dateoftable, dateslist, btnnumber, btnobjdict

    #initializing the window containing the date picker
    calframe = tk.Tk()
    calframe.title("Date Picker")
    calframe.resizable(False, False)
    calframe.geometry('400x400')

    tablenumlabel = ttk.Label(calframe, text="Timetable No: ")
    tablenumlabel.place(x=100, y=60)
    datepickedtxtlabel = ttk.Label(calframe, text="Date Picked: ")
    datepickedtxtlabel.place(x=100, y=100)

    tablenumentry = ttk.Entry(calframe, text="Enter timetable number")
    tablenumentry.place(x=220, y=60)
    datepickedlabel = ttk.Label(calframe, text="Pick Date below")
    datepickedlabel.place(x=220, y=100)

    datepickbtn = ttk.Button(calframe, text="Choose Date")
    datepickbtn.place(x=100, y=180)

    confirmbtn = ttk.Button(calframe, text="Confirm")
    confirmbtn.place(x=220, y=180)

    #for the user to pick a date on the calendar widget
    def choosedateclicked():

        calendarframe = tk.Tk()
        calendarframe.title("Choose Date")
        calendarframe.resizable(False, False)
        calendarframe.geometry('400x300')

        #to create a calendar widget
        cal = tkcal.Calendar(calendarframe, year=2021, month=1, day=1, selectmode='day',
                             showothermonthdays=False, date_pattern='dd-mm-yy')
        cal.place(x=80, y=20)

        pickdatebtn = ttk.Button(calendarframe, text="Pick Date")
        pickdatebtn.place(x=160, y=250)

        #executed when the pickdatebtn is clicked
        def pickdateclicked():
            global dateoftable

            dateoftable = cal.get_date()
            calendarframe.destroy()

            datepickedlabel.configure(text=dateoftable)

        pickdatebtn.configure(command=pickdateclicked)
        calendarframe.mainloop()

    #checks whether the entered credentials are correct and if correct uodates the table on clicking
    def confirmbtnclicked():
        global dateoftable, btnnumber, btnobjdict

        btnnumber = tablenumentry.get()

        # to make sure entered table number is a digit and doesn't go below 1 or exceed 24
        if (not btnnumber.isdigit()) or (int(btnnumber) < 1 or int(btnnumber) > 24):
            popup.showerror('Error', "Table Number does not exist")
            calframe.destroy()

        # to make sure entered date is not already taken by another button
        elif any(dateoftable in lst for lst in btnobjdict.values()):

            popup.showwarning('Warning', f'Specified date {dateoftable} already exists')
            calframe.destroy()

        else:
            dateslist.append(dateoftable)
            calframe.destroy()

            #updates the data of the specific button in the table present in the database
            sql.cursorobj.execute(f"UPDATE timetablebtn SET tabledate='{dateoftable}' WHERE btnobject='btnobject{btnnumber}'")
            sql.mysqlobj.commit()

            #updates the values in the dictionary
            btnobjdict[f'btnobject{btnnumber}'][0].configure(text=f'Table No: {btnnumber} \n Date: {dateoftable}')
            btnobjdict[f'btnobject{btnnumber}'][1] = dateoftable

            popup.showinfo("Success", f"Table No:{btnnumber}'s date updated to {dateoftable} ")

    #assigning the functions to the buttons
    datepickbtn.configure(command=choosedateclicked)
    confirmbtn.configure(command=confirmbtnclicked)

    calframe.mainloop()


#executes when any one of the time table buttons in the root window is clicked
def tableclick(btnobj):
    global btnobjdict

    #creates a new window once table is clicked
    tableframe = tk.Tk()
    tableframe.title(btnobjdict[btnobj][1])
    tableframe.resizable(False, False)
    tableframe.geometry('600x600')
    tableframe.configure(bg='#082032')

    #creating the style for the buttons in the new window
    stylewin2 = ttk.Style(tableframe)
    stylewin2.theme_use('clam')
    stylewin2.configure('win2.TButton', background='#F0A500', foreground='white',
                        focuscolor='white',
                        font=('Bahnschrift SemiBold SemiCondensed', 12))
    # color change on mouse hover
    stylewin2.map('win2.TButton', background=[('active', '#ffc547')])

    addtaskbtn = ttk.Button(tableframe, text='+ Add Event', style='win2.TButton')
    addtaskbtn.place(x=120, y=530)
    # using lambda to pass parameters to function that gets executed when this button is clicked
    addtaskbtn.configure(command=lambda x=(btnobj, tableframe): ae.addtaskbtnclick(x[0], x[1]))

    deletetaskbtn = ttk.Button(tableframe, text='X Delete Event', style='win2.TButton')
    deletetaskbtn.place(x=240, y=530)
    deletetaskbtn.config(command=lambda x=(btnobj, tableframe): ae.deletetaskbtnclick(x[0], x[1]))

    # to update the window once a task is added or deleted
    refreshbtn = ttk.Button(
        tableframe, text='O Refresh Window', style='win2.TButton')
    refreshbtn.place(x=360, y=530)
    refreshbtn.configure(command=lambda x=(btnobj, tableframe): ae.refreshbtnclick(x[0], x[1]))

    tableframe.mainloop()


sql.cursorobj.execute("SELECT * FROM timetablebtn ORDER BY sno")
records = sql.cursorobj.fetchall()

#assigning the tableclick function to all the buttons in the root window
for row in records:
    btnobj = row['btnobject']
    btnobjdict[btnobj][0].configure(command=lambda x=btnobj: tableclick(x))


#configuring the button to perform actions on clciking
updatebtn.configure(command=updatetable)


root.mainloop()

#closing cnnection to database
sql.mysqlobj.close()
