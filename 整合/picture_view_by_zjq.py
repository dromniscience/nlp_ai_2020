import tkinter as tk 


#根窗体实例root
root = tk.Tk() 
root.title("ai写诗")
root.geometry('480x480') #窗口大小


class WordFrame():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.title = tk.Label(self.frame, text="寻找相似的字", bg = '#d3fbfb', fg="black",font = ('华文仿宋',16), width=30,\
                        height = 1, relief = tk.RIDGE) #标题
        self.word_entry = tk.Entry(self.frame, bd=4)   #输入字的框
        self.word_label = tk.Label(self.frame, text="请输入一个字", font=('华文仿宋', 12))
        self.ans_label = tk.Label(self.frame, width=20, height=1, font=('华文仿宋', 12))
        self.exit_button = tk.Button(self.frame, text="退出", bg = 'white', fg="black",font = ('华文仿宋',16), width=40,\
                        height = 2, relief = tk.RIDGE)
        self.enter_button = tk.Button(self.frame, text="确定", bg = 'white', fg="black",font = ('华文仿宋',16), width=40,\
                        height = 2, relief = tk.RIDGE)

        #布局
        self.title.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1, anchor=tk.CENTER)
        self.word_entry.place(relx = 0.6, rely = 0.4, relwidth = 0.3, relheight = 0.1, anchor=tk.CENTER)
        self.word_label.place(relx = 0.3, rely = 0.4, relwidth = 0.3, relheight = 0.1, anchor=tk.CENTER)
        self.ans_label.place(relx=0.5, rely=0.6, relheight = 0.1, relwidth=0.5, anchor=tk.CENTER)
        #self.ans_label.config(text="1,2,3,4,5")
        self.enter_button.place(relx = 0.3, rely = 0.8, relwidth = 0.2, relheight = 0.1, anchor=tk.CENTER)
        self.exit_button.place(relx =0.6, rely=0.8, relwidth=0.2, relheight=0.1, anchor=tk.CENTER)

class StartFrame():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        #添加组件
        self.title_label = tk.Label(self.frame, text="ai写诗", bg = '#d3fbfb', fg="black",font = ('华文仿宋',16), width=30,\
        height = 1, relief = tk.RIDGE)

        self.button1 = tk.Button(self.frame, text="寻找相似字", bg='white', fg="black",font = ('华文仿宋',12), width=40,\
        height = 2)
        self.button2 = tk.Button(self.frame, text="藏头诗", bg = 'white', fg="black",font = ('华文仿宋',12), width=40,\
        height = 2)
        self.button3 = tk.Button(self.frame, text="古诗风格迁移", bg = 'white', fg="black",font = ('华文仿宋',12), width=40,\
        height = 2)
        #添加布局
        self.title_label.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1, anchor=tk.CENTER)
        self.button1.place(relx = 0.5, rely = 0.3, relwidth=0.4, relheight=0.1, anchor=tk.CENTER)
        self.button2.place(relx = 0.5, rely = 0.5, relwidth=0.4, relheight=0.1, anchor=tk.CENTER)
        self.button3.place(relx = 0.5, rely = 0.7, relwidth=0.4, relheight=0.1, anchor=tk.CENTER)


word_frame = WordFrame(root)
start_frame = StartFrame(root)
#start_frame.frame.destroy()
#start_frame.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
word_frame.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

root.mainloop()
