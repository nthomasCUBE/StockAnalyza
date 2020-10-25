#
#   StockAnalyza v0.1
#
#   2020/10/22: working on the relative genes tagged per total genes in Bin

from tkinter import *
from tkinter.filedialog import askopenfilename
import numpy as np
import math
import random

def empty_function():
    pass

def open_file():
    master.stock_file = askopenfilename()

    clear_screen()
    
    choices={}
    fh=open(master.stock_file, encoding="latin-1")
    xarr=[]
    for line in fh.readlines()[1:]:
        line=line.strip()
        vals=line.split(",")
        if(len(vals)==7):
            try:
                xarr.append(float(vals[1]))
            except:
                pass
            #xarr.append(30*math.log(float(vals[1])))

    x_mean30=[]
    x_mean50=[]
    x_mean200=[]
    diff=[]
    for x in range(2,len(xarr)):
        try:
            diff.append((xarr[x-1]/xarr[x-2]))
        except Exception:
            pass
        
        if(x>30):
            c_sel=xarr[x-30:x]
            x_mean30.append(sum(c_sel)/len(c_sel))
        else:
            c_sel=xarr[1:30]
            x_mean30.append(sum(c_sel)/len(c_sel))

        if(x>50):
            c_sel=xarr[x-50:x]
            x_mean50.append(sum(c_sel)/len(c_sel))
        else:
            c_sel=xarr[1:50]
            x_mean50.append(sum(c_sel)/len(c_sel))

        if(x>200):
            c_sel=xarr[x-200:x]
            x_mean200.append(sum(c_sel)/len(c_sel))
        else:
            c_sel=xarr[1:200]
            x_mean200.append(sum(c_sel)/len(c_sel))

    sim_s=[]
    w_cnt=0
    b_cnt=0

    sim_start=int((len(xarr)*3)/4)

    
    for x in range(1,1000):
        x_start=xarr[sim_start]
        for y in range(0,int(len(xarr)/4)):
            x_start=x_start*diff[random.randint(0,len(diff)-1)]
        sim_s.append(x_start)
        if(x_start>xarr[len(xarr)-1]):
            b_cnt=b_cnt+1
        else:
            w_cnt=w_cnt+1
            
    my_avg=float(sum(sim_s))/float(len(sim_s))
    my_median=sorted(sim_s)
    my_median=my_median[int(len(my_median)/2)]
    
    print("max_sim=%f" % max(sim_s))
    print("min_sim=%f" % min(sim_s))
    print("avg_sim=%f" % my_avg)
    print("last=%f" % xarr[len(xarr)-1])
    print("better_in_cases=%f" % b_cnt)
    print("worse_in_cases=%f" % w_cnt)
    print("m30=%s" % x_mean30[len(x_mean30)-1])
    print("m50=%s" % x_mean50[len(x_mean50)-1])
    print("m200=%s" % x_mean200[len(x_mean200)-1])

    c_f=float(w_cnt)/float(b_cnt+w_cnt)
    w.create_text(100,250,text="p_val=%f" % c_f )
    c_f2=float(b_cnt)/float(b_cnt+w_cnt)
    w.create_text(100,270,text="p_val=%f" % c_f2 )
    w.create_text(100,290,text="SIMULATION (avg)=%f" % my_avg )
    w.create_text(100,310,text="SIMULATION (median)=%f" % my_median )
    w.create_text(100,330,text="ACTUAL=%f" % xarr[len(xarr)-1] )
    w.create_text(100,350,text="m30=%f" %  x_mean30[len(x_mean30)-1] )
    w.create_text(100,370,text="m50=%f" %  x_mean50[len(x_mean50)-1] )
    w.create_text(100,390,text="m200=%f" % x_mean200[len(x_mean200)-1] )

    fac_n=200/max(xarr)

    c_width=1
    for x in range(0,len(xarr)):
        w.create_rectangle(100+c_width*x,600-xarr[x]*fac_n,100+c_width*(x+1),600-xarr[x]*fac_n,fill="white")

    for x in range(0,len(x_mean30)):
        w.create_line(100+c_width*x,600-x_mean30[x]*fac_n,100+c_width*(x+1),600-x_mean30[x]*fac_n,fill="blue")

    for x in range(0,len(x_mean50)):
        w.create_line(100+c_width*x,600-x_mean50[x]*fac_n,100+c_width*(x+1),600-x_mean50[x]*fac_n,fill="orange")

    for x in range(0,len(x_mean200)):
        w.create_line(100+c_width*x,600-x_mean200[x]*fac_n,100+c_width*(x+1),600-x_mean200[x]*fac_n,fill="red")

    w.create_text(100,200,text="200 days",fill="red")
    w.create_text(150,200,text="50 days",fill="orange")
    w.create_text(200,200,text="30 days",fill="blue")

    #for x in range(0,len(diff)):
    #    w.create_rectangle(100+1*x,500-5*diff[x],100+1*(x+1),500+0,fill="white")


def clear_screen():
    w.delete('all')
    
canvas_width =  1000
canvas_height = 600

master = Tk()
master.title("StockAnalyza - analysis of stock data");
master.configure(background='pink')

newwin = Toplevel(master, height=10, width=25)
master.display = Text(newwin, height=5, width=50, bg="lightyellow")
master.display2 = Text(newwin, height=10, width=50, bg="lightyellow")
button = Button(newwin, text="Get Sequence",command=empty_function)
newwin.destroy()

w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height, bg='lightyellow')

var1 = IntVar()
var2 = IntVar()
var1.set(1)
var2.set(1)

menubar = Menu(master)
filemenu = Menu(master, tearoff=0)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(master, tearoff=0)
editmenu.add_command(label="Clear screen", command=clear_screen)
menubar.add_cascade(label="Edit", menu=editmenu)


master.config(menu=menubar)

w.grid(row=8,column=0,columnspan=2)

master.mainloop()

