# Packages
import requests
from plyer import notification
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk


# Html fetcher
def return_html(url):
    # headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
    # html = requests.get(url, headers=headers)
    html = requests.get(url)
    html = html.text
    return html


# Notification function
def notify(state, table_row):
    for row in table_row:
        data = row.find_all('td')
        if data[1].get_text() == state:
            notification_title = f"Covid Cases in {state}"
            notification_message = f"Confirmed Cases: {data[2].get_text()}\nActive Cases: {data[3].get_text()}\nRecovered: {data[4].get_text()}\nDeaths: {data[5].get_text()}"
            break
    notification.notify(title=notification_title, message=notification_message, app_icon="./icon.ico", timeout=20)


# Covid table window
def covid_table(table_row):
    # Create a window
    table_window = Toplevel(root, bg=bg)
    table_window.title("State wise case table")
    table_window.wm_iconbitmap("icon.ico")

    # Scrollbar creation
    scroll = Scrollbar(table_window, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)

    # Create a table
    tree_style = ttk.Style()
    tree_style.theme_use("clam")
    tree_style.configure("Treeview",
                         background=fg,
                         foreground=bg,
                         rowheight=55,
                         font=("helvatica", 12, 'bold'),
                         relief=NONE
                         )
    tree_style.map("Treeview", background=[('selected', bg)], foreground=[('selected', fg)])
    table = ttk.Treeview(table_window, yscrollcommand=scroll.set, style="Treeview")
    scroll.config(command=table.yview)
    table.pack(fill=BOTH, expand=True)

    # Define table structure
    columns = ("slno", "state", "confirmed", "active", "recovery", "deaths")
    table["columns"] = columns
    for column in columns:
        if column == "slno":
            table.column(column, anchor=CENTER, width=50)
        elif column == "state":
            table.column(column, anchor=CENTER, width=500)
        else:
            table.column(column, anchor=CENTER)

    table["show"] = "headings"
    table.heading("slno", text="Sl. No.")
    table.heading("state", text="State/ Union territory")
    table.heading("confirmed", text="Confirmed")
    table.heading("active", text="Active")
    table.heading("recovery", text="Recovered")
    table.heading("deaths", text="Deaths")

    # Fetch state wise data
    index = 1
    for row in table_row:
        data = row.find_all('td')
        state = data[1].get_text()
        confirmed = data[2].get_text()
        active = data[3].get_text()
        recovery = data[4].get_text()
        death = data[5].get_text()
        # Insert data into the table
        table.insert("", index=END, values=(index, state, confirmed, active, recovery, death))
        index += 1

    tree_footer = Label(table_window,
                       text="Copyrights - THE_ARYA 2020",
                       anchor=CENTER, fg=btnbg, bg=btnfg,
                       cursor="spider")
    tree_footer.pack(side=BOTTOM, fill=X, pady=0, ipady=5)

# State wise option list window
def state_wise(table_row):
    homeFrame.pack_forget()
    global state_wise_frame, warn_message
    state_wise_frame = Frame(root, cursor="spider", bg=bg)
    state_wise_frame.pack()

    state_var = StringVar(state_wise_frame)
    state_list = ['Select State', 'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam',
                  'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadar Nagar Haveli', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
                  'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh',
                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
                  'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telengana', 'Tripura', 'Uttarakhand',
                  'Uttar Pradesh', 'West Bengal']
    state_var.set(state_list[0])
    state_options = OptionMenu(state_wise_frame, state_var, *state_list)
    state_options["relief"] = SOLID
    state_options["cursor"] = "hand2"
    state_options.configure(font=('lucida', 15))
    state_options.pack(fill=X, pady=(25, 0))
    state_options["bg"] = btnbg
    state_options["activebackground"] = activeBtn
    state_options["highlightbackground"] = activeBtn

    # Validate Selection
    def validate():
        if state_var.get() == "Select State":
            warn_message.config(text="Please select a State")
        else:
            warn_message.config(text="")
            notify(state_var.get(), table_row)

    info_button = Button(state_wise_frame,
                         text="Get Info", width="10",  anchor=CENTER,
                         cursor="hand2", relief=SOLID,
                         bg=btnbg, fg=btnfg,  activebackground=activeBtn,
                         font=('lucida', 15), command=validate)
    info_button.pack(side=LEFT, pady=25, padx=15)

    back_button = Button(state_wise_frame, text="Back", width="10", anchor=CENTER,
                         cursor="hand2", relief=SOLID,
                         bg=btnbg, fg=btnfg,  activebackground=activeBtn,
                         font=('lucida', 15), command=back)
    back_button.pack(side=RIGHT, pady=25, padx=15)

    warn_message = Label(root, font=('lucida', 12, 'bold'), fg="red", cursor="spider")
    warn_message.pack(fill=Y)


# Function for BACK button
def back():
    global state_wise_frame, warn_message
    state_wise_frame.destroy()
    warn_message.destroy()
    homeFrame.pack(fill=BOTH, expand=True)


if __name__ == '__main__':
    # Create GUI
    root = Tk()
    root.title("CovidInfo | THE_ARYA")
    root.wm_iconbitmap("icon.ico")
    root.geometry("500x300+200+200")
    root.resizable(False, False)

    # Colors
    bg = "#FBEAEB"
    fg = "#1D1B1B"
    btnbg = "#a6a6a6"
    btnfg = "#1D1B1B"
    activeBtn = "#4d4d4d"
    root['bg'] = bg
    root['cursor'] = "spider"

    title = Label(root, text="Covid Info - India(State Wise)", font=('lucida', 20), bg=bg, fg=fg, cursor="spider")
    title.pack(side='top', fill=X, pady=(25, 0))

    # Fetch data
    # Check for internet connection
    try:
        # covidHTML = return_html(r"https://covidindia.org/")
        covidHTML = return_html(r"https://prsindia.org/covid-19/cases")
        covidDataHTML = BeautifulSoup(covidHTML, 'html.parser')
        # Access table
        tableData = covidDataHTML.find_all('tbody')[0]
        # Access rows - State wise
        tableRow = tableData.find_all('tr')[0:35+1]

    # No internet - error handling
    except Exception:
        connectionError = Label(root,
                                text="Some error occured. Please try to connect to the internet and try again",
                                font=('lucida', 12, 'bold'), fg="red")
        connectionError.pack(pady=25)
        closeBtn = Button(root, text="Close", font=('lucida', 12),
                          width="50", anchor=CENTER, cursor="hand2", relief=SOLID,
                          bg=btnbg, fg=btnfg, activebackground=activeBtn,
                          command=root.quit)
        closeBtn.pack(pady=(15, 0))

    # No error - Goto Home page
    else:
        homeFrame = Frame(root, cursor="spider")
        homeFrame.pack(fill=BOTH, expand=True)

        tableBtn = Button(homeFrame, text="View Table", width="50",
                          font=('lucida', 12), anchor=CENTER,
                          cursor="hand2", relief=SOLID, bg=btnbg,
                          fg=btnfg, activebackground=activeBtn,
                          command=lambda: covid_table(tableRow))
        tableBtn.pack(pady=(25, 0))

        stateBtn = Button(homeFrame, text="Choose State",
                          font=('lucida', 12), width="50", anchor=CENTER,
                          cursor="hand2", relief=SOLID,
                          bg=btnbg, fg=btnfg,
                          activebackground=activeBtn,
                          command=lambda: state_wise(tableRow))
        stateBtn.pack(pady=(15, 0))

        closeBtn = Button(homeFrame, text="Close",
                          font=('lucida', 12), width="50",
                          anchor=CENTER, cursor="hand2", relief=SOLID,
                          bg=btnbg, fg=btnfg,
                          activebackground=activeBtn, command=root.quit)
        closeBtn.pack(pady=(15, 0))

    # Footer/ CopyRights
    footer = Label(root, text="Copyrights - THE_ARYA 2020", anchor=CENTER, fg="BLACK", bg="#99b3e6", cursor="spider")
    footer.pack(side=BOTTOM, fill=X, pady=0, ipady=5)

    root.mainloop()
