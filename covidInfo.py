import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk

def return_html(url):
    html = requests.get(url)
    html = html.text
    return html

def covid_table(table_row):
    # Create a window
    table_window = Toplevel(root)
    table_window.title("State wise case table")

    # Scrollbar creation
    scroll = Scrollbar(table_window, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)

    # Create a table
    table = ttk.Treeview(table_window, yscrollcommand=scroll.set)
    scroll.config(command=table.yview)
    table.pack(fill=BOTH, expand=True, pady=15)

    # Define table structure
    columns = ("slno", "state", "confirmed", "recovery", "deaths")
    table["columns"] = columns
    for column in columns:
        table.column(column, anchor=CENTER)
    table["show"] = "headings"
    table.heading("state", text="State")
    table.heading("slno", text="Sl. NO.")
    table.heading("confirmed", text="Confirmed")
    table.heading("recovery", text="Recovered")
    table.heading("deaths", text="Deaths")


    # Fetch state wise data
    index = 1
    for row in table_row:
        data = row.find_all('td')
        state = data[0].get_text()
        confirmed = data[1].get_text()
        recovery = data[2].get_text()
        death = data[3].get_text()
        # Insert data intto the table
        table.insert("", index=END, values=(index, state, confirmed, recovery, death))
        index += 1

def state_wise():
    pass

if __name__ == '__main__':
    # Fetch data
    covidHTML = return_html(r"https://covidindia.org/")
    covidDataHTML = BeautifulSoup(covidHTML, 'html.parser')
    # Access table
    tableData = covidDataHTML.find_all('tbody')[0]
    # Access rows - Satae wise
    tableRow = tableData.find_all('tr')[0:35+1]


    root = Tk()
    root.title("CovidInfo | THE_ARYA")
    root.geometry("500x200")
    root.resizable(False, False)

    title = Label(root, text="Covid Info - India(State Wise)", font=('lucida', 20))
    title.pack(side='top', fill=X, pady=(15, 0))

    tableBtn = Button(root, text="Table", command=lambda :covid_table(tableRow), width="50", anchor=CENTER, relief=SOLID)
    tableBtn.pack(pady=15)

    stateBtn = Button(root, text="Choose State", command=state_wise, width="50", anchor=CENTER, relief=SOLID)
    stateBtn.pack(pady=10)

    root.mainloop()
