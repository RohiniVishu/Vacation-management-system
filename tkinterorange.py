#even for semantic and syntax error both, the squiggly line will come
import tkinter as tk  # all libraries stored in tk 
from tkinter import messagebox
import csv

#load the dataset
#file_path=r"C:\Users\Pallavi\traveldest" #if you put r you dont need to change the slash direction
def load_destinations(file_path):
    destinations=[]
    try:                                           #exception handling blocks. 
        with open(file_path,mode='r') as file:
            reader=csv.DictReader(file)    #each row is made into a dictionary. key is header, value is value.
            for row in reader:             #all values in string, we should convert to int or float
            #parse numeric fields         #reader is a group of dictionaries values
                row['popularity']=float(row['popularity'])
                row['price']=float(row['price'])
                for key in row:
                    if row[key] in{"0","1"}:
                        row[key]=int(row[key]) #if 0 or 1, we'll convert it to integer
                destinations.append(row)     #list of dictionaries
        return destinations
    except FileNotFoundError:       #catching exceptions like filenotfound error.
        messagebox.showerror("error",f"file '{file_path}' not found.")  #catches the error and displays in the gui. not in the terminal itself.
        return[]                #file_path should be in single quotes not double           #file_path is file_path only now. file path value given later
        #error stored in return empty list
        #explicitly for each error we can give messagebox, or in general we can give for all error
    except Exception as e:
        messagebox.showerror("error",f"error loading file:{e}")
        return[]
#function to filter destinations based on preferences
def filter_destinations():
    #get the current values of preferences
    preference_values={key:var.get() for key, var in preferences.items()}

    #filter destinations
    filtered_destinations=[]
    for destination in destinations :
        match= True
        for key, value in preference_values.items():
            if value==1 and destination[key]!=1:
                match=False                           #if both not 1 then false. if both 1 then true
                break
        if match:
                filtered_destinations.append(destination)
    #display results
    result_text.delete("1.0",tk.END)
    if not filtered_destinations:
        result_text.insert(tk.END,"no matches found for your preferences.\n") 
        result_text.insert(tk.END,"here are the top popular destinations:\n\n")
        sorted_destinations=sorted(destinations,key=lambda x:x["popularity"],reverse=True)[:5]

    else:
        result_text.insert(tk.END,'top picks based on your preferences:\n\n')
        sorted_destinations=sorted(filtered_destinations,key=lambda x:x["popularity"],reverse=True)[:5]

    for i, destination in enumerate(sorted_destinations,start=1):
        result_text.insert(
            tk.END,
            f"{i}.destination:{destination['competitorname']}\n"
            f"popularity:{destination['popularity']}\n"
            f"price: ${destination['price']}\n\n")
#function to clear preferences
def clear_preferences():
    for var in preferences.values():
        var.set(0)
    result_text.delete("1.0",tk.END)
#load travel destination data
file_path="traveldest.csv" #ensure this file exists
destinations=load_destinations(file_path)

#initialize the GUI
root=tk.Tk()
root.title("travel destination finder")
root.geometry("500x600")
#checkboc variables stored in the preference dictionary
preferences={
    "tropical":tk.IntVar(),
    "cold":tk.IntVar(),
    "adventure":tk.IntVar(),
    "relaxation":tk.IntVar(),
    "cultural":tk.IntVar(),
    "nature":tk.IntVar(),
    "shopping":tk.IntVar(),
    "modern":tk.IntVar(),
    "historic":tk.IntVar()
}        
#layout
tk.Label(root,text="select your travel preferences:", font=("arial",16,"bold")).pack(pady=10)
#pack and pady in this itself because we havent assigned a variable to above
for key,var in preferences.items():
    tk.Checkbutton(root, text=key.capitalize(), variable=var).pack(anchor="w",padx=20)
#buttons
tk.Button(root, text="final destinations", command=filter_destinations,font=("arial",12)).pack(pady=10)
tk.Button(root,text="clear preferences",command=clear_preferences,font=("arial",12)).pack(pady=5)

#results
tk.Label(root, text="results:",font=("arial",14)).pack(pady=10)
result_text=tk.Text(root,wrap="word",height=20,width=50,font=("arial",12))
result_text.pack(pady=10)

#run the application
root.mainloop()


