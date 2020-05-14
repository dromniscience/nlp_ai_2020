import tkinter as tk
from PIL import Image, ImageTk
import get_topk
import generate
# 主界面
def ui_process():
    root =tk.Tk()
    root.geometry("300x400+5+5")
    root.title("ai写诗")
    
    title_label = tk.Label(text="ai写诗", bg = '#d3fbfb', fg="black",font = ('华文仿宋',16), width=30,\
        height = 1, relief = tk.RIDGE)

    button1 = tk.Button(text="寻找相似字", bg='white', fg="black",font = ('华文仿宋',12), width=40,\
        height = 2,command=lambda:choice_A(root))
    button2 = tk.Button(text="藏头诗", bg = 'white', fg="black",font = ('华文仿宋',12), width=40,\
        height = 2,command=lambda:choice_B(root))
    button3 = tk.Button(text="古诗多风格生成", bg = 'white', fg="black",font = ('华文仿宋',12), width=40,\
        height = 2,command=lambda:choice_C(root))
       
    title_label.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1, anchor=tk.CENTER)
    button1.place(relx = 0.5, rely = 0.3, relwidth=0.4, relheight=0.1, anchor=tk.CENTER)
    button2.place(relx = 0.5, rely = 0.5, relwidth=0.4, relheight=0.1, anchor=tk.CENTER)
    button3.place(relx = 0.5, rely = 0.7, relwidth=0.4, relheight=0.1, anchor=tk.CENTER)

    tk.mainloop()

# 主界面的第一个选项
def choice_A(root):
    root1 = tk.Toplevel(root)
    root1.geometry("500x600+5+5")
    title = tk.Label(root1,text="寻找相似的字", bg = '#d3fbfb', fg="black",font = ('华文仿宋',16), width=30,\
                        height = 1, relief = tk.RIDGE)
    word_entry = tk.Entry(root1,bd=4)
    word_label = tk.Label(root1,text="请输入一个字", font=('华文仿宋', 12))
    ans_label = tk.Label(root1,width=20, height=1, font=('华文仿宋', 12))
    enter_button = tk.Button(root1,text="确定", bg = 'white', fg="black",font = ('华文仿宋',16), width=40,\
                        height = 2, relief = tk.RIDGE,command=lambda:Button_process3(root1,word_entry.get()))
    title.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1, anchor=tk.CENTER)
    word_entry.place(relx = 0.6, rely = 0.4, relwidth = 0.3, relheight = 0.06, anchor=tk.CENTER)
    word_label.place(relx = 0.3, rely = 0.4, relwidth = 0.3, relheight = 0.1, anchor=tk.CENTER)
    ans_label.place(relx=0.5, rely=0.6, relheight = 0.1, relwidth=0.5, anchor=tk.CENTER)
    enter_button.place(relx = 0.5, rely = 0.9, relwidth = 0.2, relheight = 0.1, anchor=tk.CENTER)

# 主界面的第二个选项
def choice_B(root):
    root1 = tk.Toplevel(root)
    root1.geometry("300x400+5+5")
    L_titile = tk.Label(root1,text='藏头诗')
    L_titile.config(font='华文仿宋 -50 bold',fg='red')
    L_titile.place(x=150,y=60,anchor="center")

    B_0 = tk.Button(root1, text="老诗新赋", command=lambda:Button_process1(root1))
    B_0.place(x=80,y=200)
    B_1 = tk.Button(root1, text="主题诗歌", command=lambda:Button_process2(root1))
    B_1.place(x=160, y=200)

# 主界面的第三个选项
def choice_C(root):
    root1 = tk.Toplevel(root)
    root1.geometry("500x400+5+5")
    title = tk.Label(root1,text="风格迁移", bg = '#d3fbfb', fg="black",font = ('华文仿宋',16), width=30,\
                        height = 1, relief = tk.RIDGE) 
    word_entry = tk.Entry(root1,bd=4)  
    word_label = tk.Label(root1,text="请输入一句五言首句", font=('华文仿宋', 12))
    ans_label = tk.Label(root1,width=20, height=1, font=('华文仿宋', 12))
    enter_button = tk.Button(root1,text="确定", bg = 'white', fg="black",font = ('华文仿宋',16), width=40,\
                        height = 2, relief = tk.RIDGE,command=lambda:Button_process4(root1,word_entry.get()))
                        
    title.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1, anchor=tk.CENTER)
    word_entry.place(relx = 0.6, rely = 0.4, relwidth = 0.3, relheight = 0.1, anchor=tk.CENTER)
    word_label.place(relx = 0.3, rely = 0.4, relwidth = 0.3, relheight = 0.1, anchor=tk.CENTER)
    ans_label.place(relx=0.5, rely=0.6, relheight = 0.1, relwidth=0.5, anchor=tk.CENTER)
    enter_button.place(relx = 0.5, rely = 0.8, relwidth = 0.2, relheight = 0.1, anchor=tk.CENTER)

# 第一个选项用户输入后进入的函数
def Button_process3(root1,word):
    k_top=get_topk.jiekou(word)
    lst=[]
    text = tk.Text(root1, width=20, height=6)
    text.config(font='华文仿宋 -25 bold',fg='black')
    text.place(x=150,y=330)
    
    for i in range(5):
        lst.append([])
        for j in range(2):
            lst[i].append(str(k_top[i][j]))
    print(lst[0][0][7:13])
    
    final_text="相似度      近义词\n"+lst[0][0][7:13]+"       "+lst[0][1]+"\n"+lst[1][0][7:13]+\
    "       "+lst[1][1]+"\n"+lst[2][0][7:13]+"       "+lst[2][1]+"\n"+lst[3][0][7:13]+"       "+\
    lst[3][1]+"\n"+lst[4][0][7:13]+"       "+lst[4][1]
    text.insert("insert",final_text)
    text.config(state='disabled')
    
# 第三个选项用户输入后进入的函数
def Button_process4(root1,word):
    root2=tk.Toplevel(root1)
    root2.geometry("1000x800+50+50")
    title=tk.Label(root2,text="用“"+word+"”生成的诗歌")
    title.config(font='华文仿宋 -40 bold',fg='red')
    title.place(x=500,y=60,anchor="center")
    poem_list=generate.jiekou(word)
    print(poem_list)
    words=""
    length=len(poem_list)
    for i in poem_list:
        if i=="。" or i=="，" or i=="<E>":
            continue
        else:
            words+=i
            
    poem1=word+"\n"+words[0:5]+"\n"+words[5:10]+"\n"+words[10:15]
    module1=tk.Label(root2,text=poem1)
    module1.config(font='华文仿宋 -30 bold',fg='black')
    module1.place(x=200,y=200,anchor="center")
    
    poem2=word+"\n"+words[15:20]+"\n"+words[20:25]+"\n"+words[25:30]
    module2=tk.Label(root2,text=poem2)
    module2.config(font='华文仿宋 -30 bold',fg='black')
    module2.place(x=450,y=200,anchor="center")
    
    poem3=word+"\n"+words[30:35]+"\n"+words[35:40]+"\n"+words[40:45]
    module3=tk.Label(root2,text=poem3)
    module3.config(font='华文仿宋 -30 bold',fg='black')
    module3.place(x=700,y=200,anchor="center")

# 第二个选项中九首老诗的界面，分别从Button_process1_0到Button_process1_8
def Button_process1_0(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='长干行')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='妾发初覆额\n折花门前剧\n郎骑竹马来\n绕床弄青梅\n')
    revised = tk.Label(root3,text='妾发初覆额\n折花压翠钿\n郎船下蕲阳\n绕鼻吹衣裳\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)

def Button_process1_1(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='相思')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='红豆生南国\n春来发几枝\n愿君多采撷\n此物最相思\n')
    revised = tk.Label(root3,text='红豆生南国\n春风吹欲开\n愿作双燕子\n此山与谁诉\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
def Button_process1_2(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='旅夜书怀')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='细草微风岸\n危樯独夜舟\n星垂平野阔\n月涌大江流\n')
    revised = tk.Label(root3,text='细草微风岸\n危堤别离情\n星山断肠断\n月满敝箧中\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
def Button_process1_3(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='登鹳雀楼')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='白日依山尽\n黄河入海流\n欲穷千里目\n更上一层楼\n')
    revised = tk.Label(root3,text='白日依山尽\n黄昏鹿门前\n欲知秋江水\n更有双燕子\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
def Button_process1_4(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='登岳阳楼')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='昔闻洞庭水\n今上岳阳楼\n吴楚东南坼\n乾坤日夜浮\n')
    revised = tk.Label(root3,text='昔闻洞庭水\n今日江水边\n吴船下蘋渚\n乾坤双鸳鸯\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
    
def Button_process1_5(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='辋川闲居赠裴秀才迪')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='寒山转苍翠\n秋水日潺湲\n倚杖柴门外\n临风听暮蝉\n')
    revised = tk.Label(root3,text='寒山转苍翠\n秋风吹不知\n倚船下蕲阳\n临风吹衣裳\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
    
def Button_process1_6(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='竹里馆')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='独坐幽篁里\n弹琴复长啸\n深林人不知\n明月来相照\n')
    revised = tk.Label(root3,text='独坐幽篁里\n弹指未有情\n深院隔江水\n明月照晚风\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
    
def Button_process1_7(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='登乐游原')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='向晚意不适\n驱车登古原\n夕阳无限好\n只是近黄昏\n')
    revised = tk.Label(root3,text='向晚意不适\n驱马上水流\n夕阳春风起\n只恐吹飞去\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
    
def Button_process1_8(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root3,text='山居秋暝')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root3,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root3,text='空山新雨后\n天气晚来秋\n明月松间照\n清泉石上流\n')
    revised = tk.Label(root3,text='空山新雨后\n天高一剑杵\n明月下蘋渚\n清江烟雾里\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    revised.config(font='华文仿宋 -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)

# 第二个选项中三首主题诗的界面，分别从Button_process2_0到Button_process2_2
def Button_process2_0(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    
    title = tk.Label(root3,text='北大五四\n')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=80,anchor="center")
    original = tk.Label(root3,text='北方有佳人\n大江湖上红\n五月明月夜\n四海断肠断\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    original.place(x=165,y=100)
    
def Button_process2_1(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    
    title = tk.Label(root3,text='我喜欢你\n')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=80,anchor="center")
    original = tk.Label(root3,text='我本楚狂人\n喜知秋水边\n欢情照荷花\n你我梦中人\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    original.place(x=165,y=100)

def Button_process2_2(root2):
    
    root3 = tk.Toplevel(root2)
    root3.geometry("500x400+50+50")
    
    title = tk.Label(root3,text='春夏秋冬\n')
    title.config(font='华文仿宋 -50 bold',fg='black')
    title.place(x=250,y=80,anchor="center")
    original = tk.Label(root3,text='春江花月夜\n夏虫鸣杜鹃\n秋风吹衣裳\n冬赏无限好\n')
    original.config(font='华文仿宋 -30 bold',fg='blue')
    original.place(x=165,y=100)

# 第二个选项中的第一个子选项
def Button_process1(root1):
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    
    L_titile = tk.Label(root2,text='请选择要改编的诗歌')
    L_titile.config(font='华文仿宋 -30 bold',fg='red')
    L_titile.place(x=250,y=60,anchor="center")
    
    B_0 = tk.Button(root2, text="长干行", command=lambda:Button_process1_0(root2))
    B_0.place(x=40,y=100)
    B_1 = tk.Button(root2, text="相思", command=lambda:Button_process1_1(root2))
    B_1.place(x=40,y=170)
    B_2 = tk.Button(root2, text="旅夜书怀", command=lambda:Button_process1_2(root2))
    B_2.place(x=40,y=240)
    B_3 = tk.Button(root2, text="登鹳雀楼", command=lambda:Button_process1_3(root2))
    B_3.place(x=200, y=100)
    B_4 = tk.Button(root2, text="登岳阳楼", command=lambda:Button_process1_4(root2))
    B_4.place(x=200,y=170)
    B_5 = tk.Button(root2, text="辋川闲居赠裴秀才迪", command=lambda:Button_process1_5(root2))
    B_5.place(x=200, y=240)
    B_6 = tk.Button(root2, text="竹里馆", command=lambda:Button_process1_6(root2))
    B_6.place(x=360,y=100)
    B_7 = tk.Button(root2, text="登乐游原", command=lambda:Button_process1_7(root2))
    B_7.place(x=360, y=170)
    B_8 = tk.Button(root2, text="山居秋暝", command=lambda:Button_process1_8(root2))
    B_8.place(x=360, y=240)

# 第二个选项中的第二个子选项
def Button_process2(root1):
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    L_titile = tk.Label(root2,text='请选择藏头诗的主题')
    L_titile.config(font='华文仿宋 -30 bold',fg='red')
    L_titile.place(x=250,y=60,anchor="center")
    
    B_0 = tk.Button(root2, text="北大五四", command=lambda:Button_process2_0(root2))
    B_0.place(x=220,y=120)
    B_1 = tk.Button(root2, text="我喜欢你", command=lambda:Button_process2_1(root2))
    B_1.place(x=220,y=190)
    B_2 = tk.Button(root2, text="春夏秋冬", command=lambda:Button_process2_2(root2))
    B_2.place(x=220,y=260)
    
# 进入主界面
if __name__ == "__main__":
    print("开始")
    ui_process()