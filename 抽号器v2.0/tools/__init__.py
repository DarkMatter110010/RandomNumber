import tkinter

if __name__ == '__main__':
    import operate
else:
    from tools import operate

def init():
    global root,label1,label2,label3,entry1,entry2,text1,button1,scrollbar1,listbox1
    
    root = tkinter.Tk()
    root.geometry('720x450+350+100')
    root.title('抽号器 v2.0')
    root.resizable(0,0)
    root.protocol("WM_DELETE_WINDOW",operate.closing)

    label1 = tkinter.Label(root,bg='white',text='开始学号',font = ('微软雅黑',12))
    label1.place(x=20,y=25, width=150, height=30)
    label2 = tkinter.Label(root,bg='white',text='终止学号',font = ('微软雅黑',12))
    label2.place(x=20,y=75, width=150, height=30)
    label3 = tkinter.Label(root,bg='white',font = ('微软雅黑',100))
    label3.place(x=230,y=175, width=240, height=250)
    label4 = tkinter.Label(root,bg='white',text='历史记录',font = ('微软雅黑',15))
    label4.place(x=20,y=175, width=170, height=40)

    entry1 = tkinter.Entry(root,font = ('微软雅黑',12))
    entry1.place(x=200, y=25, width=500, height=30)
    entry2 = tkinter.Entry(root,font = ('微软雅黑',12))
    entry2.place(x=200, y=75, width=500, height=30)

    text1 = tkinter.Text(root,font = ('微软雅黑',12))
    text1.place(x=20,y=125, width=680,height=30)

    button1=tkinter.Button(root,text='抽号',relief = 'raised',font=('微软雅黑',12),command = lambda: operate.show_number(entry1,entry2,label3,listbox1))
    button1.place(x=500,y=175,width=200,height=250)

    scrollbar1 = tkinter.Scrollbar(root) #滚动条
    scrollbar1.pack(side = tkinter.RIGHT,fill = tkinter.Y) #滚动条靠右侧延Y轴填充
    scrollbar1.place(x = 195,y = 175,width = 20,height = 250)

    listbox1 =tkinter.Listbox(root,relief = 'raised',font=('微软雅黑',12),yscrollcommand = scrollbar1.set) #列表，yscrollcommand参数是列表控制滚动条
    listbox1.place(x=20,y=225,width = 170,height = 200)

    scrollbar1.config(command=listbox1.yview) #滚动条控制列表

    operate.text(entry1,entry2)
    root.mainloop(0)
