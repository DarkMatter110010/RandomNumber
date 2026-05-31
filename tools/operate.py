import random
import tkinter
from tkinter import messagebox

if __name__ == '__main__':
    exit()
else:
    import tools

flag = 1
def show_number(label3,label4,label5):
    global start,end,all_number,true_number,flag,new_number
    start = int(label4.cget('text'))
    end = int(label5.cget('text'))
    all_number = [i for i in range(start,end)]
    if flag == 1:
        new_number = all_number
        flag += 1
    else:
        pass
    checkbox2_value = tools.checkbox_var2.get()
    if checkbox2_value == 1:
        if len(new_number) > 0:
            pass
        else:
            new_number = all_number
        true_number = random.choice(new_number)
        new_number.remove(true_number)
        #print(new_number)
    elif checkbox2_value == 0:
        true_number = random.choice(all_number)
        #print(all_number)
    label3.text = true_number
    label3.configure(text = true_number)

def modify():
    global start,end,all_number,new_number
    start = int(tools.label4.cget('text'))
    end = int(tools.label5.cget('text'))
    all_number = [i for i in range(start,end)]
    new_number = all_number


def closing():
    if messagebox.askokcancel("Quit", "确定退出?"):
        tools.root.destroy()
        exit()

def updown():
    checkbox1_value = tools.checkbox_var1.get()
    if checkbox1_value == 1:
        tools.root.attributes('-topmost',True)
    else:
        tools.root.attributes('-topmost',False)

def probability():
    checkbox2_value = tools.checkbox_var2.get() 
    if checkbox2_value == 1:
        messagebox.showerror('Error','不重复状态下不可以设置概率')
    elif checkbox2_value == 0:
        messagebox.showinfo('Sorry','此功能未完成')
        pass

def getvalue(label,entry,page):
    try:
        newstart = int(entry.get())
    except:
        messagebox.showwarning('Unrecognized','参数异常')
    else:
        label.text = str(newstart)
        label.config(text = str(newstart))
    finally:
        page.destroy()
        modify()
        return True

def createstart():
    global startpage
    startpage = tkinter.Toplevel()
    startpage.title('更改起始学号')
    startpage.geometry('300x100+350+100')
    startpage.resizable(width = False,height = False)
    entry1 = tkinter.Entry(startpage,font = ('微软雅黑',12))
    entry1.pack()
    button1 = tkinter.Button(startpage,text = '确认',font = ('微软雅黑',12),command = lambda:getvalue(tools.label4,entry1,startpage))
    button1.pack()

def createend():
    global endpage
    endpage = tkinter.Toplevel()
    endpage.title('更改起始学号')
    endpage.geometry('300x100+350+100')
    endpage.resizable(width = False,height = False)
    entry1 = tkinter.Entry(endpage,font = ('微软雅黑',12))
    entry1.pack()
    button1 = tkinter.Button(endpage,text = '确认',font = ('微软雅黑',12),command = lambda:getvalue(tools.label5,entry1,endpage))
    button1.pack()
