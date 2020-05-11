import tkinter as tk

from PIL import Image, ImageTk
def ui_process():
    root =tk.Tk()
    root.geometry("300x400+5+5")

#标签   
    L_titile = tk.Label(root,text='藏头诗')
    L_titile.config(font='Arial -50 bold',fg='red')
    L_titile.place(x=150,y=60,anchor="center")

#按钮
    B_0 = tk.Button(root, text="老诗新赋", command=lambda:Button_process1(root))
    B_0.place(x=80,y=200)
    B_1 = tk.Button(root, text="主题诗歌", command=lambda:Button_process2(root))
    B_1.place(x=160, y=200)


    tk.mainloop()

def Button_process1_0(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='长干行')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='妾发初覆额\n折花门前剧\n郎骑竹马来\n绕床弄青梅\n')
    revised = tk.Label(root2,text='妾发初覆额\n折花压翠钿\n郎船下蕲阳\n绕鼻吹衣裳\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)

def Button_process1_1(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='相思')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='红豆生南国\n春来发几枝\n愿君多采撷\n此物最相思\n')
    revised = tk.Label(root2,text='红豆生南国\n春风吹欲开\n愿作双燕子\n此山与谁诉\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
def Button_process1_2(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='旅夜书怀')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='细草微风岸\n危樯独夜舟\n星垂平野阔\n月涌大江流\n')
    revised = tk.Label(root2,text='细草微风岸\n危堤别离情\n星山断肠断\n月满敝箧中\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
def Button_process1_3(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='登鹳雀楼')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='白日依山尽\n黄河入海流\n欲穷千里目\n更上一层楼\n')
    revised = tk.Label(root2,text='白日依山尽\n黄昏鹿门前\n欲知秋江水\n更有双燕子\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
def Button_process1_4(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='登岳阳楼')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='昔闻洞庭水\n今上岳阳楼\n吴楚东南坼\n乾坤日夜浮\n')
    revised = tk.Label(root2,text='昔闻洞庭水\n今日江水边\n吴船下蘋渚\n乾坤双鸳鸯\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
    
def Button_process1_5(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='辋川闲居赠裴秀才迪')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='寒山转苍翠\n秋水日潺湲\n倚杖柴门外\n临风听暮蝉\n')
    revised = tk.Label(root2,text='寒山转苍翠\n秋风吹不知\n倚船下蕲阳\n临风吹衣裳\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
    
def Button_process1_6(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='竹里馆')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='独坐幽篁里\n弹琴复长啸\n深林人不知\n明月来相照\n')
    revised = tk.Label(root2,text='独坐幽篁里\n弹指未有情\n深院隔江水\n明月照晚风\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
    
def Button_process1_7(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='登乐游原')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='向晚意不适\n驱车登古原\n夕阳无限好\n只是近黄昏\n')
    revised = tk.Label(root2,text='向晚意不适\n驱马上水流\n夕阳春风起\n只恐吹飞去\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
    
def Button_process1_8(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    load=Image.open("timg.png")
    render=ImageTk.PhotoImage(load)
    title = tk.Label(root2,text='山居秋暝')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=60,anchor="center")
    img=tk.Label(root2,image=render)
    img.image=render
    img.place(x=235,y=200)
    original = tk.Label(root2,text='空山新雨后\n天气晚来秋\n明月松间照\n清泉石上流\n')
    revised = tk.Label(root2,text='空山新雨后\n天高一剑杵\n明月下蘋渚\n清江烟雾里\n')
    original.config(font='Arial -30 bold',fg='blue')
    revised.config(font='Arial -30 bold',fg='red')
    original.place(x=60,y=150)
    revised.place(x=300,y=150)
    
def Button_process2_0(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    
    title = tk.Label(root2,text='北大五四\n')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=80,anchor="center")
    original = tk.Label(root2,text='北方有佳人\n大江湖上红\n五月明月夜\n四海断肠断\n')
    original.config(font='Arial -30 bold',fg='blue')
    original.place(x=165,y=100)
    
def Button_process2_1(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    
    title = tk.Label(root2,text='我喜欢你\n')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=80,anchor="center")
    original = tk.Label(root2,text='我本楚狂人\n喜知秋水边\n欢情照荷花\n你我梦中人\n')
    original.config(font='Arial -30 bold',fg='blue')
    original.place(x=165,y=100)

def Button_process2_2(root1):
    
    root2 = tk.Toplevel(root1)
    root2.geometry("500x400+50+50")
    
    title = tk.Label(root2,text='春夏秋冬\n')
    title.config(font='Arial -50 bold',fg='black')
    title.place(x=250,y=80,anchor="center")
    original = tk.Label(root2,text='春江花月夜\n夏虫鸣杜鹃\n秋风吹衣裳\n冬赏无限好\n')
    original.config(font='Arial -30 bold',fg='blue')
    original.place(x=165,y=100)


    
#按钮对应函数入口
def Button_process1(root):
    root1 = tk.Toplevel(root)
    root1.geometry("500x400+50+50")
    
    L_titile = tk.Label(root1,text='请选择要改编的诗歌')
    L_titile.config(font='Arial -30 bold',fg='red')
    L_titile.place(x=250,y=60,anchor="center")
    
    B_0 = tk.Button(root1, text="长干行", command=lambda:Button_process1_0(root1))
    B_0.place(x=40,y=100)
    B_1 = tk.Button(root1, text="相思", command=lambda:Button_process1_1(root1))
    B_1.place(x=40,y=170)
    B_2 = tk.Button(root1, text="旅夜书怀", command=lambda:Button_process1_2(root1))
    B_2.place(x=40,y=240)
    B_3 = tk.Button(root1, text="登鹳雀楼", command=lambda:Button_process1_3(root1))
    B_3.place(x=200, y=100)
    B_4 = tk.Button(root1, text="登岳阳楼", command=lambda:Button_process1_4(root1))
    B_4.place(x=200,y=170)
    B_5 = tk.Button(root1, text="辋川闲居赠裴秀才迪", command=lambda:Button_process1_5(root1))
    B_5.place(x=200, y=240)
    B_6 = tk.Button(root1, text="竹里馆", command=lambda:Button_process1_6(root1))
    B_6.place(x=360,y=100)
    B_7 = tk.Button(root1, text="登乐游原", command=lambda:Button_process1_7(root1))
    B_7.place(x=360, y=170)
    B_8 = tk.Button(root1, text="山居秋暝", command=lambda:Button_process1_8(root1))
    B_8.place(x=360, y=240)
    
def Button_process2(root):
    root1 = tk.Toplevel(root)
    root1.geometry("500x400+50+50")
    L_titile = tk.Label(root1,text='请选择藏头诗的主题')
    L_titile.config(font='Arial -30 bold',fg='red')
    L_titile.place(x=250,y=60,anchor="center")
    
    B_0 = tk.Button(root1, text="北大五四", command=lambda:Button_process2_0(root1))
    B_0.place(x=220,y=120)
    B_1 = tk.Button(root1, text="我喜欢你", command=lambda:Button_process2_1(root1))
    B_1.place(x=220, y=190)
    B_2 = tk.Button(root1, text="春夏秋冬", command=lambda:Button_process2_2(root1))
    B_2.place(x=220,y=260)
    
    

if __name__ == "__main__":
    print("开始")
    ui_process()