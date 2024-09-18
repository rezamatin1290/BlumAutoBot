"""
a program that users the blum card

account link, number of card for used
show number of card, start


show: 
    number of cards


"""

from tkinter import *

window = Tk()

l1 = Label(window, text="Account Link: ")
l1.grid(row=0, column=0, padx=10, pady=2, sticky="w")

l2 = Label(window, text="number cards:")
l2.grid(row=0, column=2 ,padx=10, pady=10, sticky="w")

account_link = StringVar()
e1 = Entry(window, textvariable=account_link)
e1.grid(row=0, column=1, padx=3, pady=10)

number_card = StringVar()
e2 = Entry(window, textvariable=number_card)
e2.grid(row=0, column=3, padx=10, pady=10)

show_msg = Listbox(window, height=6, width=35)
show_msg.grid(row=2, column=0, rowspan=6, columnspan=2)

sb = Scrollbar(window)
sb.grid(row=2, column=2, rowspan=6)

show_msg.configure(yscrollcommand=sb.set)
sb.configure(command=show_msg.yview)



show_ncard = Button(window, text="show number of card", width=22)
show_ncard.grid(row = 2 , column=3, padx=10, pady=10,)


button_start = Button(window, text="Start", width=20)
button_start.grid(row = 3 , column=3, padx=10, pady=7)

window.mainloop()


