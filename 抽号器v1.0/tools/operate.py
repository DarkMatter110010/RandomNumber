import random
from tkinter import messagebox

if __name__ == '__main__':
    from number import *
else:
    import tools
    from tools.number import *


def make_list(start:int,end:int,pass_number:list):
    all_number = [i for i in range(start,end + 1)]

    for student in Prank_person:
        idx = Prank_person.index(student)
        for i in range(0,Prank_time[idx]):
            all_number.append(student)

    for student in pass_number:
        while student in all_number:
            all_number.remove(student)

    return all_number


def show_number(entry1,entry2,label3):
    global a,b,c,d,true_number
    a = int(entry1.get())
    b = int(entry2.get())
    c = Pass_list
    true_number = random.choice(make_list(a,b,c))
    label3.text = true_number
    label3.configure(text = true_number)


def closing():
    if __name__ == '__main__':
        print('Error')
    else:
        Root = tools.root
    if messagebox.askokcancel("Quit", "确定退出?"):
        Root.destroy()


def text(entry1,entry2):
    entry1.delete(0,'end')
    entry2.delete(0,'end')
    entry1.insert(0,'1')
    entry2.insert(0,'52')
