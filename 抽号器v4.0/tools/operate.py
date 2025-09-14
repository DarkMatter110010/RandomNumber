import sys
import random
import tkinter
from tkinter import messagebox

if __name__ == '__main__':
    exit()
else:
    import tools

def passing_parameters(label4,label5):#由于无法直接调用label4常量，故用此函数接收参数
    global start,end,all_number,use_number
    start = int(label4.cget('text'))
    end = int(label5.cget('text'))
    all_number = [i for i in range(start,end+1)]
    use_number = all_number
    all_probability = list()
    for i in range(len(all_number)):
        all_probability.append(1)
    return all_probability #元素是int

flag1 = 1 #控制new_number是否重置
flag3 = 1 #控制use_number是否重置
def show_number(label3,label4,label5):
    #all_number是放置全员学号的列表
    #new_number是不重复状态下剩余成员学号列表
    #use_number是配合概率使用时的成员列表（已根据概率增删学号）
    #true_number是抽中的学号
    global start,end,all_number,true_number,new_number,use_number,flag1,flag3
    
    try:
        probability_page.destroy()
        startpage.destroy()
        endpage.destroy()
    except:
        pass

    if flag3 == 1:
        passing_parameters(label4,label5)
        flag3 += 1
    else:
        pass

    if flag1 == 1:
        new_number = all_number
        flag1 += 1
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
        true_number = random.choice(use_number)
        #print(all_number)
        #print(use_number)
    label3.text = true_number
    label3.configure(text = true_number)

def modify():
    global start,end,all_number,new_number,flag2
    start = int(tools.label4.cget('text'))
    end = int(tools.label5.cget('text'))
    all_number = [i for i in range(start,end)]
    new_number = all_number
    flag2 = 1


def closing():
    if messagebox.askokcancel("Quit", "确定退出?"):
        tools.root.destroy()
        sys.exit()

def updown():
    checkbox1_value = tools.checkbox_var1.get()
    if checkbox1_value == 1:
        tools.root.attributes('-topmost',True)
    else:
        tools.root.attributes('-topmost',False)

def more(listbox1,useList):#用于probability
    global use_number,flag3
    key = listbox1.curselection()[0] #查找选中项
    useList[key] += 1 #增加概率数
    listbox1.delete(key) #更新效果
    listbox1.insert(key,str(key+1)+' ——概率：'+str(useList[key])) #更新效果
    use_number.append(key+1) #正确学号 = 索引 + 1
    #print(use_number)
    #print(all_number)
    flag3 += 1

def less(listbox1,useList):#用于probability
    global use_number,flag3
    key = listbox1.curselection()[0] #查找选中项
    if useList[key] > 0:
        useList[key] -= 1 #减小概率数
        listbox1.delete(key) #更新效果
        listbox1.insert(key,str(key+1)+' ——概率：'+str(useList[key])) #更新效果
        use_number.remove(key+1) #正确学号 = 索引 + 1
    #print(use_number)
    #print(all_number)
    flag3 += 1

flag2 = 1 #控制useList（概率列表）是否重置
def probability(label4,label5):
    global flag2,useList,use_number,all_number
    
    try:
        startpage.destroy()
        endpage.destroy()
    except:
        pass

    checkbox2_value = tools.checkbox_var2.get() 
    if checkbox2_value == 1:
        messagebox.showerror('Error','不重复状态下不可以设置概率')
    elif checkbox2_value == 0:
        global probability_page
        probability_page = tkinter.Toplevel()
        probability_page.geometry('350x350+350+100')
        probability_page.title('修改概率')
        probability_page.resizable(0,0)

        # 添加一个滚动条Scrollbar,靠右，填充。
        scrollbar1 = tkinter.Scrollbar(probability_page)
        scrollbar1.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar1.place(x = 320, y = 20,width = 10,height = 260)

        # listbox 生成列表选框,selectmode设置选择模式，SINGLE单选，EXTENDED多选
        listbox1 = tkinter.Listbox(probability_page,selectmode=tkinter.SINGLE, yscrollcommand=scrollbar1.set)
        listbox1.pack(fill=tkinter.BOTH)
        listbox1.place(x = 20,y = 20,width = 280,height = 260)
        
        #滚动条控制列表
        scrollbar1.config(command=listbox1.yview)

        button1 = tkinter.Button(probability_page,text = '增加',font = ('微软雅黑',12),command = lambda: more(listbox1,useList))
        button1.place(x = 20,y = 300,width = 50,height = 30)
        button2 = tkinter.Button(probability_page,text = '减小',font = ('微软雅黑',12),command = lambda: less(listbox1,useList))
        button2.place(x = 100,y = 300,width = 50,height = 30)
        if flag2 == 1:
            useList = passing_parameters(label4,label5)
            flag2 += 1
        else:
            pass

        for i in all_number:
            idx = all_number.index(i)
            other = useList[idx]
            listbox1.insert(tkinter.END,str(i)+' ——概率：'+str(other))


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
    
    try:
        probability_page.destroy()
        endpage.destroy()
    except:
        pass

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
    
    try:
        probability_page.destroy()
        startpage.destroy()
    except:
        pass

    endpage = tkinter.Toplevel()
    endpage.title('更改终止学号')
    endpage.geometry('300x100+350+100')
    endpage.resizable(width = False,height = False)
    entry1 = tkinter.Entry(endpage,font = ('微软雅黑',12))
    entry1.pack()
    button1 = tkinter.Button(endpage,text = '确认',font = ('微软雅黑',12),command = lambda:getvalue(tools.label5,entry1,endpage))
    button1.pack()
