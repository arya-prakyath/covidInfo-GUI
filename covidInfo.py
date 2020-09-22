# Packages
import requests
from plyer import notification
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk


# Html fetcher
def return_html(url):
    html = requests.get(url)
    html = html.text
    return html


# Notification function
def notify(state, table_row):
    for row in table_row:
        data = row.find_all('td')
        if data[0].get_text() == state:
            title = f"Covid Cases in {state}"
            message = f"Confirmed Cases: {data[1].get_text()}\nRecovered: {data[2].get_text()}\nDeaths: {data[3].get_text()}"
            break
    notification.notify(title=title, message=message, app_icon="icon.ico", timeout=20)


# Covid table window
def covid_table(table_row):
    # Create a window
    table_window = Toplevel(root)
    table_window.title("State wise case table")
    table_window.wm_iconbitmap("icon.ico")

    # Scrollbar creation
    scroll = Scrollbar(table_window, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)

    # Create a table
    table = ttk.Treeview(table_window, yscrollcommand=scroll.set, selectmode=NONE)
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
        # Insert data into the table
        table.insert("", index=END, values=(" ", "", "", "", ""))
        table.insert("", index=END, values=(index, state, confirmed, recovery, death))
        index += 1


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

    info_button = Button(state_wise_frame, text="Get Info", width="10",  anchor=CENTER, cursor="hand2", relief=SOLID, bg=btnbg, fg=btnfg,  activebackground=activeBtn, font=('lucida', 15), command=validate)
    info_button.pack(side=LEFT, pady=25, padx=15)

    back_button = Button(state_wise_frame, text="Back", width="10", anchor=CENTER, cursor="hand2", relief=SOLID, bg=btnbg, fg=btnfg,  activebackground=activeBtn, font=('lucida', 15), command=back)
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
        covidHTML = return_html(r"https://covidindia.org/")
        covidDataHTML = BeautifulSoup(covidHTML, 'html.parser')
        # Access table
        tableData = covidDataHTML.find_all('tbody')[0]
        # Access rows - State wise
        tableRow = tableData.find_all('tr')[0:35+1]
    # No internet - error handling
    except Exception:
        connectionError = Label(root, text="Please connect to the internet and try again", font=('lucida', 12, 'bold'), fg="red")
        connectionError.pack(pady=25)
        closeBtn = Button(root, text="Close", font=('lucida', 12), width="50", anchor=CENTER, cursor="hand2",
                          relief=SOLID, bg=btnbg, fg=btnfg, activebackground=activeBtn, command=root.destroy)
        closeBtn.pack(pady=(15, 0))
    # No error - Goto Home page
    else:
        homeFrame = Frame(root, cursor="spider")
        homeFrame.pack(fill=BOTH, expand=True)

        tableBtn = Button(homeFrame, text="View Table", width="50", font=('lucida', 12), anchor=CENTER, cursor="hand2", relief=SOLID, bg=btnbg, fg=btnfg, activebackground=activeBtn, command=lambda: covid_table(tableRow))
        tableBtn.pack(pady=(25, 0))

        stateBtn = Button(homeFrame, text="Choose State", font=('lucida', 12), width="50", anchor=CENTER, cursor="hand2", relief=SOLID, bg=btnbg, fg=btnfg,  activebackground=activeBtn, command=lambda: state_wise(tableRow))
        stateBtn.pack(pady=(15, 0))

        closeBtn = Button(homeFrame, text="Close", font=('lucida', 12), width="50", anchor=CENTER, cursor="hand2", relief=SOLID, bg=btnbg, fg=btnfg,  activebackground=activeBtn, command=root.destroy)
        closeBtn.pack(pady=(15, 0))

    # Footer/ CopyRights
    footer = Label(root, text="Copyrights - THE_ARYA 2020", anchor=CENTER, fg="BLACK", bg="#99b3e6", cursor="spider")
    footer.pack(side=BOTTOM, fill=X, pady=0, ipady=5)

    root.mainloop()
