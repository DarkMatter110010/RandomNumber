import tkinter as tk
from tkinter import messagebox
import random,sys

class ProbabilityEditor:
    def __init__(self, master, min_value, max_value, prob_entries):
        self.master = master
        self.min_value = min_value
        self.max_value = max_value

        self.probs = prob_entries

        self.scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(master, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        self.scrollbar.config(command=self.canvas.yview)
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.scales = []

        for i, prob in enumerate(prob_entries, start=min_value):
            label = tk.Label(self.frame, text=str(i) + ":")
            label.grid(row=i - min_value, column=0, padx=10, pady=2, sticky="w")
            scale = tk.Scale(self.frame, from_=0, to=50, orient=tk.HORIZONTAL, length = 300, command=lambda val, index=i: self.update_prob(val, index))
            scale.set(prob)
            scale.grid(row=i - min_value, column=1, padx=5, pady=2)
            self.scales.append(scale)

        self.save_button = tk.Button(master, text="保存", command=self.save_probabilities)
        self.save_button.pack(pady=5)

    def update_prob(self, val, index):
        self.probs[index - self.min_value] = int(val)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save_probabilities(self):
        messagebox.showinfo("Save", "保存成功！")
        self.master.destroy()

class NumberPickerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("抽号器v5.0（升级版）")
        self.master.geometry('360x240')
        self.master.protocol("WM_DELETE_WINDOW",self.closing)

        self.min_label = tk.Label(master, bg = 'white', text="起始值：", font = ('微软雅黑',12))
        self.min_label.place(x = 20,y = 20,width = 80,height = 30)

        self.min_entry = tk.Entry(master, font = ('微软雅黑',12))
        self.min_entry.place(x = 120, y = 20,width = 50,height = 30)

        self.max_label = tk.Label(master, bg = 'white', text="终止值：", font = ('微软雅黑',12))
        self.max_label.place(x = 190,y = 20,width = 80,height = 30)

        self.max_entry = tk.Entry(master, font = ('微软雅黑',12))
        self.max_entry.place(x = 290, y = 20,width = 50,height = 30)

        self.fill()

        self.show_label = tk.Label(master, bg = 'white', font = ('微软雅黑',70))
        self.show_label.place(x = 20,y = 70,width = 150,height = 150)
        
        self.edit_prob_button = tk.Button(master, text="编辑概率",font = ('微软雅黑',12),command=self.edit_probabilities)
        self.edit_prob_button.place(x = 190,y = 140,width = 150,height = 30)

        self.start_button = tk.Button(master, text="抽号",font = ('微软雅黑',16), command=self.start_picking)
        self.start_button.place(x = 190,y = 70,width = 150,height = 50)

        self.checkbox_var1 = tk.IntVar()
        self.checkbox1 = tk.Checkbutton(master, text="置顶", variable=self.checkbox_var1,command = self.updown)
        self.checkbox1.place(x = 190,y = 190,width = 50,height = 30)

        self.prob_entries = []
    
    def edit_probabilities(self):
        min_value = int(self.min_entry.get())
        max_value = int(self.max_entry.get())

        prob_editor_window = tk.Toplevel(self.master)
        prob_editor_window.title("概率编辑器")

        # 获取当前的概率值并传递给概率编辑器
        current_probs = [1] * (max_value - min_value + 1)
        prob_editor = ProbabilityEditor(prob_editor_window, min_value, max_value, current_probs)
        self.prob_entries = current_probs

    def start_picking(self):
        try:
            min_value = int(self.min_entry.get())
            max_value = int(self.max_entry.get())

            if min_value >= max_value:
                messagebox.showerror("Error", "数值异常，请重新输入")
                return

            numbers = []
            for i, prob in enumerate(self.prob_entries, start=min_value):
                numbers.extend([i]*prob)

            try:
                picked_number = random.choice(numbers)
            except IndexError:
                messagebox.showerror('IndexError','请设置概率')
            except:
                messagebox.showerror('Error','出现错误')
            else:
                self.show_label.config(text = picked_number)
        except ValueError:
            messagebox.showerror("Error", "数值无效，请重新输入")
    
    def updown(self):
        checkbox_value1 = self.checkbox_var1.get()
        if checkbox_value1 == 1:
            self.master.attributes('-topmost',True)
        else:
            self.master.attributes('-topmost',False)
    
    def closing(self):
        if messagebox.askokcancel("Quit", "确定退出?"):
            self.master.destroy()
            sys.exit()

    def fill(self):
        with open('number.ini',mode = 'r',encoding = 'UTF-8') as f:
            n_range = f.readlines() #抽号默认范围
            f.close()
        s_range = n_range[0] #起始值
        e_range = n_range[-1] #终止值

        self.min_entry.insert(0,s_range)
        self.max_entry.insert(0,e_range)

def main():
    root = tk.Tk()
    app = NumberPickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
