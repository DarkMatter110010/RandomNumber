import tkinter as tk
from tkinter import ttk, messagebox, filedialog, BooleanVar
import os,sys,json
from random import choices

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("抽号器v6.0")
        self.root.geometry("800x600+600+100")
        self.root.resizable(False, False)

        # 加载配置文件
        self.setting_file = "settings.json"
        self.number_file = "number.json"
        self.settings = self.load_settings()
        self.numbers = self.load_numbers()

        # 应用置顶设置
        if self.settings.get("top", False):
            self.root.wm_attributes("-topmost", True)

        # 创建界面
        self.create_widgets()
        self.create_menu()

    def load_settings(self):
        """加载 setting.json，若不存在则创建默认"""
        if not os.path.exists(self.setting_file):
            default_settings = {
                "top": True,
                "sidebar": True
            }
            with open(self.setting_file, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, ensure_ascii=False, indent=4)
            return default_settings
        else:
            with open(self.setting_file, 'r', encoding='utf-8') as f:
                return json.load(f)

    def load_numbers(self):
        """加载 number.json，若不存在则创建 1~50 权重为1 的默认数据"""
        if not os.path.exists(self.number_file):
            default_numbers = {str(i): 1 for i in range(1, 51)}
            with open(self.number_file, 'w', encoding='utf-8') as f:
                json.dump(default_numbers, f, ensure_ascii=False, indent=4)
            return default_numbers
        else:
            with open(self.number_file, 'r', encoding='utf-8') as f:
                return json.load(f)

    def save_numbers(self, data):
        """保存 number.json"""
        with open(self.number_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_settings(self):
        """保存 setting.json"""
        with open(self.setting_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        """创建主界面组件"""
        # numlabel：显示抽中的学号
        self.numlabel = tk.Label(
            self.root,
            font=("微软雅黑", 200),
            relief="sunken",
            anchor="center",
            bg = 'white'
        )
        self.numlabel.place(x=30, y=100, width=550, height=470)

        # numbutton：抽号按钮
        self.numbutton = tk.Button(
            self.root,
            text="抽号",
            font=("微软雅黑", 50),
            command=self.draw_number,
            bg = 'white',
            bd = 3
        )
        self.numbutton.place(x=600,y=100, width=180, height=470)

        start_num = min(int(k) for k in self.numbers.keys())
        end_num = max(int(k) for k in self.numbers.keys())
        
        self.startlabel = tk.Label(
            self.root,
            text=f"起始学号: {start_num}",
            font=("微软雅黑", 35)
        )
        self.startlabel.place(x=30, y=30,width = 355,height = 50)

        self.endlabel = tk.Label(
            self.root,
            text=f"结束学号: {end_num}",
            font=("微软雅黑", 35)
        )
        self.endlabel.place(x=415, y=30,width = 355,height = 50)

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="修改起末学号", command=self.modify_range)
        file_menu.add_command(label="修改概率", command=self.modify_probability)

        # 设置菜单
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="设置", menu=settings_menu)
        settings_menu.add_command(label="主设置", command=self.open_settings)

        # 扩展菜单（暂不链接）
        extend_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="扩展", menu=extend_menu)

    def modify_range(self):
        """修改起末学号"""
        top = tk.Toplevel(self.root)
        top.title("修改起末学号")
        top.geometry("300x150")
        top.resizable(False, False)

        top.transient(self.root)
        top.grab_set()
        self.apply_settings_to_window(top)

        tk.Label(top, text="起始学号:").place(x=30, y=30)
        tk.Label(top, text="结束学号:").place(x=30, y=70)

        start_entry = tk.Entry(top)
        end_entry = tk.Entry(top)

        current_start = min(int(k) for k in self.numbers.keys())
        current_end = max(int(k) for k in self.numbers.keys())

        start_entry.insert(0, str(current_start))
        end_entry.insert(0, str(current_end))

        start_entry.place(x=100, y=30, width=100)
        end_entry.place(x=100, y=70, width=100)

        def apply_change():
            try:
                new_start = int(start_entry.get())
                new_end = int(end_entry.get())
                if new_start > new_end:
                    messagebox.showerror("错误", "起始学号不能大于结束学号！")
                    return
                if new_start < 1 or new_end > 999:
                    messagebox.showerror("错误", "学号范围应在 1~999 之间！")
                    return

                # 生成新字典，权重全为1
                new_numbers = {str(i): 1 for i in range(new_start, new_end + 1)}
                self.save_numbers(new_numbers)
                self.numbers = new_numbers

                # 更新 label 显示
                self.startlabel.config(text=f"起始学号: {new_start}")
                self.endlabel.config(text=f"结束学号: {new_end}")

                messagebox.showinfo("成功", "学号范围已修改，概率已重置为默认。")
                top.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的整数！")

        tk.Button(top, text="确定", command=apply_change).place(x=120, y=110, width=60)

    def modify_probability(self):
        """修改概率（权重）"""
        top = tk.Toplevel(self.root)
        top.title("修改概率")
        top.geometry("300x400")
        top.resizable(False, False)

        top.transient(self.root)
        top.grab_set()
        self.apply_settings_to_window(top)

        # 创建带滚动条的Canvas
        canvas = tk.Canvas(top)
        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scrollbar.pack(side = tk.RIGHT,fill = tk.Y)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 放置滑块
        sliders = {}
        for idx, (num, weight) in enumerate(sorted(self.numbers.items(), key=lambda x: int(x[0]))):
            tk.Label(scrollable_frame, text=f"学号 {num}").grid(row=idx, column=0, padx=10, pady=5, sticky='w')
            scale = tk.Scale(
                scrollable_frame,
                from_=0, to=50,
                orient="horizontal",
                length=180
            )
            scale.set(weight)
            scale.grid(row=idx, column=1, padx=10, pady=5)
            sliders[num] = scale

        # 确定按钮
        def save_weights():
            updated = {num: int(scale.get()) for num, scale in sliders.items()}
            self.save_numbers(updated)
            self.numbers = updated
            messagebox.showinfo("成功", "权重已更新！")
            top.destroy()

        btn_frame = tk.Frame(top)
        btn_frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(btn_frame, text="保存", command=save_weights).pack()

        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def draw_number(self):
        """抽号函数"""
        if not self.numbers:
            messagebox.showwarning("警告", "当前无学号数据！")
            return

        # 构建带权重的列表
        population = []
        weights = []
        for num, weight in self.numbers.items():
            population.append(num)
            weights.append(weight)

        try:
            result = choices(population, weights=weights, k=1)[0]
            self.numlabel.config(text=result)
        except Exception as e:
            messagebox.showerror("错误", f"抽号失败: {str(e)}")

    def open_settings(self):
        """打开设置窗口"""
        top = tk.Toplevel(self.root)
        top.title("设置")
        top.geometry("250x120")
        top.resizable(False, False)
        top.transient(self.root)
        top.grab_set()
        self.apply_settings_to_window(top)

        # 置顶复选框
        top_var = BooleanVar(value=self.settings.get("top", False))
        top_check = tk.Checkbutton(
            top,
            text="置顶",
            variable=top_var,
            command=lambda: self.toggle_top(top_var.get())
        )
        top_check.place(x=20, y=20)

        # 侧边栏最小化复选框
        sidebar_var = BooleanVar(value=self.settings.get("sidebar", False))
        sidebar_check = tk.Checkbutton(
            top,
            text="关闭时最小化到侧边栏",
            variable=sidebar_var,
            command=lambda: self.toggle_sidebar(sidebar_var.get())
        )
        sidebar_check.place(x=20, y=60)

    def toggle_top(self, is_top):
        """切换置顶状态"""
        self.settings["top"] = is_top
        self.save_settings()
        self.root.wm_attributes("-topmost", is_top)

    def toggle_sidebar(self, is_sidebar):
        """切换侧边栏最小化状态"""
        self.settings["sidebar"] = is_sidebar
        self.save_settings()

    def minimize_to_sidebar(self):
        """最小化到侧边栏"""
        self.root.withdraw()  # 隐藏主窗口

        # 创建侧边小窗口
        self.sidebar_window = tk.Toplevel()
        self.sidebar_window.overrideredirect(True)  # 无边框
        
        self.screen_width = self.root.winfo_screenwidth()
        self.sidebar_window.geometry("30x30+{}+300".format(self.screen_width-30))
        self.sidebar_window.wm_attributes("-topmost", True)

        # 创建按钮
        btn = tk.Button(
            self.sidebar_window,
            text="◀",
            font=("微软雅黑", 10),
            command=self.restore_from_sidebar
        )
        btn.pack(fill="both", expand=True)

    def restore_from_sidebar(self):
        """从侧边栏恢复主窗口"""
        self.sidebar_window.destroy()
        self.root.deiconify()  # 显示主窗口
        self.root.lift()  # 置顶
    
    def apply_settings_to_window(self, window):
        """将 settings.json 中的 top 设置应用到任意窗口"""
        current_settings = self.load_settings()
        if current_settings.get("top", False):
            window.wm_attributes("-topmost", True)
        else:
            window.wm_attributes("-topmost", False)

    def on_closing(self):
        """窗口关闭事件"""
        if self.settings.get("sidebar", False):
            self.minimize_to_sidebar()
        else:
            self.root.quit()
            self.root.destroy()
            sys.exit()


def main():
    root = tk.Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()