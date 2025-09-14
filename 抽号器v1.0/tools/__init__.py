import tkinter

if __name__ == '__main__':
    import operate
else:
    from tools import operate

def init():
    global root,label1,label2,label3,entry1,entry2,button1
    
    root = tkinter.Tk()
    root.geometry('650x400+350+100')
    root.title('抽号器 v1.0')
    root.resizable(0,0)
    root.protocol("WM_DELETE_WINDOW",operate.closing)

    label1 = tkinter.Label(root,bg='white',text='开始学号',font = ('微软雅黑',12))
    label1.place(x=20,y=25, width=150, height=30)
    label2 = tkinter.Label(root,bg='white',text='终止学号',font = ('微软雅黑',12))
    label2.place(x=20,y=75, width=150, height=30)
    label3 = tkinter.Label(root,bg='white',font = ('微软雅黑',100))
    label3.place(x=20,y=175, width=240, height=200)
    label4 = tkinter.Label(root,bg='white',text='跳过学号',font = ('微软雅黑',12))
    label4.place(x=20,y=125, width=150, height=30)

    entry1 = tkinter.Entry(root,font = ('微软雅黑',12))
    entry1.place(x=200, y=25, width=420, height=30)
    entry2 = tkinter.Entry(root,font = ('微软雅黑',12))
    entry2.place(x=200, y=75, width=420, height=30)
    entry3 = tkinter.Entry(root,font = ('微软雅黑',12))
    entry3.place(x=200, y=125, width=420, height=30)

    button1=tkinter.Button(root,text='抽号',relief = 'raised',font=('微软雅黑',12),command = lambda: operate.show_number(entry1,entry2,label3))
    button1.place(x=300,y=175,width=320,height=200)

    operate.text(entry1,entry2)
    root.mainloop(0)
