import tkinter

if __name__ == '__main__':
    exit()
else:
    from tools import operate

def init():
    global root,label1,label2,label3,label4,label5,button1,button2,button3,button4,checkbox_var1,checkbox1,checkbox_var2,checkbox2
    
    root = tkinter.Tk()
    root.geometry('350x300+350+100')
    root.title('抽号器 v4.0')
    root.resizable(0,0)
    root.protocol("WM_DELETE_WINDOW",operate.closing)

    label1 = tkinter.Label(root,bg='white',text='开始学号',font = ('微软雅黑',12))
    label1.place(x=20,y=10, width=100, height=30)
    label2 = tkinter.Label(root,bg='white',text='终止学号',font = ('微软雅黑',12))
    label2.place(x=20,y=50, width=100, height=30)
    label3 = tkinter.Label(root,bg='white',font = ('微软雅黑',80))
    label3.place(x=20,y=90, width=160, height=155)
    label4 = tkinter.Label(root,bg='white',font = ('微软雅黑',12),text='1')
    label4.place(x=135, y=10, width=80, height=30)
    label5 = tkinter.Label(root,bg='white',font = ('微软雅黑',12),text='50')
    label5.place(x=135, y=50, width=80, height=30)

    button1=tkinter.Button(root,text='抽号',relief = 'raised',font=('微软雅黑',20),command = lambda: operate.show_number(label3,label4,label5))
    button1.place(x=200,y=90,width=130,height=155)
    button2=tkinter.Button(root,text='修改概率',relief = 'raised',font=('微软雅黑',12),command = lambda: operate.probability(label4,label5))
    button2.place(x=200,y=260,width=130,height=30)
    button3=tkinter.Button(root,text='修改开始值',relief = 'raised',font=('微软雅黑',12),command = operate.createstart)
    button3.place(x=230,y=10,width=100,height=30)
    button4=tkinter.Button(root,text='修改终止值',relief = 'raised',font=('微软雅黑',12),command = operate.createend)
    button4.place(x=230,y=50,width=100,height=30)

    checkbox_var1 = tkinter.IntVar()
    checkbox1 = tkinter.Checkbutton(root, text = "置顶", variable = checkbox_var1,command = operate.updown)
    checkbox1.place(x = 20,y = 260,width = 60,height = 30)
    checkbox_var2 = tkinter.IntVar()
    checkbox2 = tkinter.Checkbutton(root, text = "不重复", variable = checkbox_var2)
    checkbox2.place(x = 100,y = 260,width = 60,height = 30)

    root.mainloop(0)
