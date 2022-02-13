#!/usr/bin/python

# ==================================
# Program: Dig the GUI
# Programer : Chong Tsz Man @2018
# Purpose: the GUI of dig function
# ==================================

import Tkinter as tk
import ttk as ttk
import tkFont as tkfont
import subprocess as sub
import thread
from sets import Set
from IPy import IP
import tkMessageBox 

def turnOnDebug():
    global debugMode;
    debugMode = True;
    print "debug mode is ON"

def turnOffDebug():
    global debugMode;
    debugMode = False;
    print "debug mode is Off"

debugMode = False;

#defualt DNS server
defDNS="1.1.1.1"
defDNS2="8.8.8.8"

#runing process
runing =0

#multiprocessing
mProc = [0,1]

#subprocess
#sub runing?
subRun = [0,1,2,3]
for i in subRun:
    subRun[i] = False

#sub body
proc = [0,1,2,3]


#subprocess
def calldig(command,subprocessID):
    global proc
    subRun[subprocessID] = True
    proc[subprocessID] = sub.Popen(command.split(),stdout=sub.PIPE, stderr=sub.PIPE)
    stdout, stderr = proc[subprocessID].communicate()

    subRun[subprocessID] = False

    if debugMode:
        print "subprocessID:" + str(subprocessID) + " finished"
        print stderr

    #output to text
    global textOut

    #enable edit
    textOut[subprocessID].config(state="normal")
    
    #delete old data
    textOut[subprocessID].delete("1.0",tk.END)
    
    #insert new data
    textOut[subprocessID].insert(tk.INSERT,stdout)
    
    scrTextOut[subprocessID].config(command=textOut[subprocessID].yview)

    #diable edit
    textOut[subprocessID].config(state="disable")

#compare two DNS result
def difCompare(command, command2):
    subRun[2] = True
    subRun[3] = True
    
    proc[2] = sub.Popen(command.split(),stdout=sub.PIPE, stderr=sub.PIPE)
    stdout, stderr = proc[2].communicate()
    subRun[2] = False
    setout = set(stdout.splitlines())

    #subRun = False means stop process
    if subRun[3]:
        proc[3] = sub.Popen(command2.split(),stdout=sub.PIPE, stderr=sub.PIPE)
        stdout, stderr = proc[3].communicate()
        subRun[3] = False
        
        setout2 = set(stdout.splitlines())
        
        if debugMode:
            print stdout


        #set theory(not really
        #common case
        matchSet = setout.intersection(setout2)
        #all case
        allSet = setout.union(setout2)
        #all case - common case = not match case
        notMatchSet = allSet - matchSet

        matchList = list(matchSet)
        notMatchList = list(notMatchSet)
        allList = list(allSet)

        global comscrTextOut,comRes
        
        comtextOut.config(state="normal")
        comtextOut.delete("1.0",tk.END)
        comtextOut.insert(tk.INSERT,"Identical:\n")
        for i in matchList:
            comtextOut.insert(tk.INSERT,str(i)+"\n")

        comtextOut.insert(tk.INSERT,"\nMis-Match:\n")
        for i in notMatchList:
            comtextOut.insert(tk.INSERT,str(i)+"\n")

        comtextOut.config(state="disable")
        comRes.grid(row=0, column=5, columnspan=5,rowspan=6,sticky="W")
        
def warning(inp):
    tkMessageBox.showwarning("Warning",inp)

def dig(opt_trace, opt_short, opt_reverse, addSettnng1, domainNameInp, DNSserInp,
        opt_simple, recordTypeInp,BufsizeInp, opt_DNSflag, opt_UDP, addSettnng2,
        opt_DNS2, DNSserInp2):

    #initial
    global comRes
    comRes.grid_forget()
    
    defDNSused = False
    defDNSused2 = False

    #input validate===============
    #(note all entry input have set default value to be empty string(no null)
    #or otherwise specificed
    
    #remove unwanted space e.g. " abc i " -> "abc i"

    if debugMode:
        print ""
        print "Input Validate:"
    addSettnng1 = addSettnng1.strip()
    domainName = domainNameInp.strip()
    DNSser = DNSserInp.strip()
    recordType = recordTypeInp.strip()
    addSettnng2 = addSettnng2.strip()
    DNSser2 = DNSserInp2.strip()
    try:
        if BufsizeInp != "":
            Bufsize = int(float(BufsizeInp.strip()))
        else:
            Bufsize = 0;
    except:
        Bufsize = 0;
        if debugMode:
            print "Bufsize check:fail, reset to 0"
    else:
        if debugMode:
            print "Bufsize check:pass"
    
    #check if DNS add is empty
    if DNSser == "":
        defDNSused = True
        DNSser = defDNS
        warning("DNS Check:Fail, Reset to " + defDNS)
        if debugMode:
            print "DNS check:fail, reset to " + defDNS

    try:
        IP(DNSser)
    except:
        defDNSused = True
        DNSser = defDNS
        warning("DNS Check:Fail, Reset to " + defDNS)
        
    if opt_DNS2:
        if DNSser2 == "":
            defDNSused2 = True
            DNSser2 = defDNS2
            warning("DNS2 Check:Fail, Reset to " + defDNS2)
            if debugMode:
                print "DNS2 check:fail, reset to " + defDNS2

    try:
        IP(DNSser2)
    except:
        defDNSused2 = True
        DNSser2 = defDNS2
        warning("DNS2 Check:Fail, Reset to " + defDNS2)

    #sumary============
    if debugMode:
        print ""
        print "Generate the DIG command!"
        print "option trace?: " + str(opt_trace)
        print "option short?: " + str(opt_short)
        print "option reverse?: " + str(opt_reverse)
        print "addSettnng1:" + addSettnng1
        print "Domain Name: " + domainName
        if defDNSused == False:
            print "DNSser: " + DNSser
        else:
            print "DNSser: " + DNSser + "(defualt DNS used"
        print "Type: " + recordType
        print "option Simple: " + str(opt_simple)
        print "option DNS flag: " + str(opt_DNSflag)
        print "option UDP?: " + str(opt_UDP)
        print "Bufsize: " + str(Bufsize)
        print "addSettnng2: " + addSettnng2
        print "2nd DNS?: " + str(opt_DNS2)
        if opt_DNS2:
            if defDNSused2 == False:
                print "DNSser2: " + DNSser2
            else:
                print "DNSser2: " + DNSser2 + "(defualt DNS used"
        
                
    command = "dig "

    #+trace
    if opt_trace:
        command += "+trace "

    #+short
    if opt_short:
        command += "+short "

    #-x
    if opt_reverse:
        command += "-x "

    if addSettnng1 != "":
        command += addSettnng1 + " "

    #domain a   
    command += domainName +" @"

    #Second half of the command============
    commandBack = " "

    if (recordType != "" ) and (recordType != "<-Not Specified->"):
        commandBack += recordType + " "
        
    if opt_simple:
        commandBack += "+noall +answer "
        
    if opt_DNSflag:
        commandBack += "+edns=0 "

    if opt_UDP:
        commandBack += "+notcp=0 "

    if Bufsize != 0:
        commandBack += "+bufsize=" + str(Bufsize) + " "


    if debugMode:
        print "Generate DIG for DNS1:" + command + DNSser + commandBack
        if opt_DNS2:
            print "Generate DIG for DNS2:" + command + DNSser2 + commandBack

    #enable alternative DNS ?
    if opt_DNS2:
        no=2
    else:
        no=1

    global mProc,runing
    arrDNSser = [0,1]
    arrDNSser[0]= DNSser
    arrDNSser[1]= DNSser2
    for i in range(no):
        try:
            mProc[i] = thread.start_new_thread(calldig, (command + arrDNSser[i] + commandBack, i,))
            runing = i + 1
        except:
            if debugMode:
                print "thread "+str(i)+"fail to start"
    if opt_DNS2:
        difCompare(command + DNSser + commandBack + "+short",command + DNSser2 + commandBack + "+short")

def stopSub():
    global proc, subRun
    #stop running
    subRun[3] = False
    
    for i in subRun:
        if subRun[i]:
            try:
                proc[i].kill()
                if debugMode:
                    print "subprocess " +str(i) + " ended"
            except:
                #do nothing
                pass

#start thread run dig <--- the function one  NOT the shell code one
def startDig(opt_trace, opt_short, opt_reverse, addSettnng1, domainNameInp, DNSserInp,
        opt_simple, recordTypeInp,BufsizeInp, opt_DNSflag, opt_UDP, addSettnng2,
        opt_DNS2, DNSserInp2):
    try:
        thread.start_new_thread(dig, (opt_trace, opt_short, opt_reverse, addSettnng1, domainNameInp, DNSserInp,
                                opt_simple, recordTypeInp,BufsizeInp, opt_DNSflag, opt_UDP, addSettnng2,
                                opt_DNS2, DNSserInp2,))
    except:
        if debugMode:
            print "thread main fail to start"



#GUI element start from here =======================
#main UI
def mainUI():

    #title 
    titlef = tk.Frame(root)
    
    #title style
    title_font = tkfont.Font(family='Helvetica', size=24, weight="bold", slant="italic")
    #title body
    title = tk.Label(titlef, text="Dig the GUI", font=title_font, anchor="e" )
    title.grid(row=0, column=1,sticky="")
    titlef.grid(row=0, column=0, columnspan=5,sticky="")

#target setting label==========================

    #target
    target = tk.LabelFrame(root, text="Target Info",width=200)
    target.grid(row=1, column=0, columnspan=5,sticky="W")

    #row0=========================================== 
    domainName = tk.Label(target, text="Resolve Target:", justify="right", anchor="e", fg="red")
    domainName.grid(row=0, column=0, padx=5, pady=5, sticky="E")

    #reverse DNS (ip lookup, -x )
    opt_reverse = tk.IntVar(root)
    reverse = tk.Checkbutton(target, text="Reverse lookUp ",variable=opt_reverse, cursor="hand2")
    reverse.grid(row=0, column=1, sticky="W")


    #domain/IP to be resovler
    defdomainName = tk.StringVar(root, value="")
    domainNameInp = tk.Entry(target, textvariable = defdomainName,width=50)
    domainNameInp.grid(row=0, column=2, columnspan=3, sticky="W")
    
#target setting END=============================


#basic setting label============================
    
    #basic setting
    basicSetting = tk.LabelFrame(root, text="Basic Setting")
    basicSetting.grid(row=2, column=0, columnspan=5,sticky="W")

    #init
    #Alternate DNS
    defDNSser2 = tk.StringVar(root, value=defDNS2) 
    DNSserInp2 = tk.Entry(basicSetting, textvariable = defDNSser2, state=tk.DISABLED)
    
    #enable 2nd(Alternate) DNS
    def toogleStateDNS(opt_DNS2):
        if opt_DNS2.get():
            DNSserInp2.config(state="normal")
            textOut[1].grid(row=6, column=5, columnspan=4)
            rawAlter.grid(row=5, column=5,sticky="W")
            scrTextOut[1].grid(row=6, column=9, columnspan=1, sticky="S"+ "N")
        else:
            DNSserInp2.config(state="disable")
            global comRes
            comRes.grid_forget()
            textOut[1].grid_forget()
            rawAlter.grid_forget()
            scrTextOut[1].grid_forget()

    #row0===========================================
    #promte user to input DNS type
    recordType = tk.Label(basicSetting, text="Record Type:", justify="right")
    recordType.grid(row=1, column=0, sticky="E")

    #DNS lookup type
    defType = tk.StringVar()
    keepvalue = defType.get()
    recordTypeInp = ttk.Combobox(basicSetting, textvariable = keepvalue)
    recordTypeInp['values'] = ("<-Not Specified->", "ANY","A","AAAA","CNAME","DNAME","HINFO", "MX","NS","PTR","SOA", "TXT", "DS","LOC")
    recordTypeInp.grid(row=1, column=1)
    recordTypeInp.current(0)

    opt_simple = tk.IntVar(root)
    opt_simple.set(1)
    simple = tk.Checkbutton(basicSetting, text="Simple Output",variable=opt_simple, cursor="hand2")
    simple.grid(row=1, column=2, sticky="W")
    simple.select()
    
    #row1===========================================
    #promte DNS server
    DNSser = tk.Label(basicSetting, text="DNS server:", justify="right")
    DNSser.grid(row=2, column=0, sticky="W")

    #DNS ser ip
    defDNSser = tk.StringVar(root, value=defDNS) 
    DNSserInp = tk.Entry(basicSetting, textvariable = defDNSser)
    DNSserInp.grid(row=2, column=1)

    #enable 2nd DNS
    opt_DNS2 = tk.IntVar(root)
    DNSser2 = tk.Checkbutton(basicSetting, text="Alternative DNS server:",variable=opt_DNS2, cursor="hand2", command= lambda: toogleStateDNS(opt_DNS2))
    DNSser2.grid(row=2, column=2, sticky="W")

    DNSserInp2.grid(row=2, column=3)


#basic setting ENd=============================


#adv setting label=============================

    #init
    opt_adv = tk.IntVar(root)
    #frame
    advSetting = tk.LabelFrame(root, text="Advance Setting")
    #click to expan the frame
    ch_adv = tk.Checkbutton(root, text="Advance Setting [+]")

    def toogleFrame(opt_adv):
        if opt_adv.get():
            advSetting.grid(row=4, column=0, columnspan=5,sticky="W")
            ch_adv.config(text="Advance Setting [-]")
        else:
            advSetting.grid_forget()
            ch_adv.config(text="Advance Setting [+]")

    #adv setting
    ch_adv.config(cursor="hand2", variable=opt_adv, anchor="e",command = lambda: toogleFrame(opt_adv))
    ch_adv.grid(row=3, column=0, columnspan=5,sticky="W")

    #row0===========================================

    opt_DNSflag = tk.IntVar(root)
    DNSflag = tk.Checkbutton(advSetting, text="Return all DNS flag",cursor="hand2", variable=opt_DNSflag)
    DNSflag.grid(row=0, column=2, padx=5, pady=5, sticky="W")

    opt_UDP = tk.IntVar(root)
    DNSudp = tk.Checkbutton(advSetting, text="Use UDP(+notcp)",cursor="hand2", variable=opt_UDP)
    DNSudp.grid(row=0, column=3, padx=5, pady=5, sticky="W")

    Bufsize = tk.Label(advSetting, text="Bufsize", justify="right")
    Bufsize.grid(row=0, column=0, sticky="E")

    defSize = tk.StringVar(root, value="") 
    BufsizeInp = tk.Entry(advSetting, textvariable = defSize)
    BufsizeInp.grid(row=0, column=1)

    #row1===========================================
    BufsizeInfo = tk.Label(advSetting, text="(Bufsize value should less than 4096, some allow bigger )")
    BufsizeInfo.grid(row=2, column=0, columnspan= 3, sticky="E")

    #row2===========================================
    opt_trace = tk.IntVar(root)
    trace = tk.Checkbutton(advSetting, text="trace path(+trace)", cursor="hand2", variable=opt_trace)
    trace.grid(row=3, column=0, columnspan= 2, padx=5, pady=5, sticky="W")

    opt_short = tk.IntVar(root)
    short = tk.Checkbutton(advSetting, text="shorten result(+short)", cursor="hand2", variable=opt_short)
    short.grid(row=3, column=2, columnspan= 2, padx=5, pady=5, sticky="W")

    #row3===========================================
    addSetting = tk.LabelFrame(advSetting, text="additional unlist option(be careful)")
    addSetting.grid(row=4, column=0, columnspan= 5, padx=5, pady=5, sticky="W")

    addSettingInfo = tk.Label(addSetting, text="dig ", justify="right")
    addSettingInfo.grid(row=1, column=0, sticky="E")

    addSettnngInp1 = tk.StringVar(root, value="") 
    addSettnng1 = tk.Entry(addSetting, textvariable = addSettnngInp1)
    addSettnng1.grid(row=1, column=1)
    
    addSettingInfo = tk.Label(addSetting, text=" <Domain/IP>@<DNS> ", justify="right")
    addSettingInfo.grid(row=1, column=2, sticky="E")

    addSettnngInp2 = tk.StringVar(root, value="") 
    addSettnng2 = tk.Entry(addSetting, textvariable = addSettnngInp2)
    addSettnng2.grid(row=1, column=3)
    

#adv setting END====================================

    #reset function
    def reset():
        defdomainName.set("")
        reverse.deselect()
        
        #basic setting
        recordTypeInp.current(0)
        defDNSser.set(defDNS)
        defDNSser2.set(defDNS2)
        DNSser2.deselect()
        DNSserInp2.config(state="disable")
        simple.select()
        textOut[1].grid_forget()
        rawAlter.grid_forget()
        
        #adv
        ch_adv.deselect()
        toogleFrame(opt_adv)
        defSize.set("")
        DNSflag.deselect()
        DNSudp.deselect()
        trace.deselect()
        short.deselect()
        addSettnngInp1.set("")
        addSettnngInp2.set("")

        #ouput
        global comRes
        comRes.grid_forget()
        textOut[0].config(state="normal")
        textOut[0].delete("1.0",tk.END)
        textOut[0].config(state="disable")
        textOut[1].config(state="normal")
        textOut[1].delete("1.0",tk.END)
        textOut[1].config(state="disable")

#Action label============================
    
    #Action 
    action = tk.LabelFrame(root, text="Action")
    action.grid(row=5, column=0, columnspan=5,sticky="W")     

    ResetBut = tk.Button(action, text="Reset", width=10,bd=2, cursor="exchange", command = lambda: reset())
    ResetBut.grid(row=5, column=0, columnspan=1)

    runBut = tk.Button(action, text="RUN", width=55,bd=2, cursor="hand2", command = lambda: startDig(opt_trace.get(),opt_short.get(), opt_reverse.get(),addSettnng1.get(), domainNameInp.get(), DNSserInp.get(),
                                                                                              opt_simple.get(),recordTypeInp.get(), BufsizeInp.get(), opt_DNSflag.get(), opt_UDP.get(), addSettnng2.get(),
                                                                                              opt_DNS2.get(), DNSserInp2.get() ))
    runBut.grid(row=5, column=1, columnspan=2)

    StopBut = tk.Button(action, text="Stop", width=10,bd=2, cursor="hand2", command = lambda: stopSub())
    StopBut.grid(row=5, column=3, columnspan=1)

#result compare
    #frame
    global comscrTextOut,comtextOut,comRes
    comRes = tk.LabelFrame(root, text="Compared Result")

    #text
    comscrTextOut = tk.Scrollbar(comRes)
    comtextOut = tk.Text(comRes, height=20, width=60,state="disable",
                         yscrollcommand=comscrTextOut.set)
    comtextOut.grid(row=0, column=0, columnspan=5, sticky="W")
    comscrTextOut.config(command=comtextOut.yview)
    comscrTextOut.grid(row=0, column=5, columnspan=1, sticky="S"+ "N")
            

#result label============================
    
    #result 
    result = tk.LabelFrame(root, text="Raw Output:")
    result.grid(row=10, column=0, columnspan=10,sticky="W")

    #raw = tk.Label(result, text="Raw Output:", justify="right")
    #raw.grid(row=4, column=0,sticky="W")

    #main DNS
    rawMain = tk.Label(result, text="Main DNS:", justify="right")
    rawMain.grid(row=5, column=0,sticky="W")

    #second DNS
    rawAlter = tk.Label(result, text="Alternative DNS:", justify="right")

    #raw output
    global textOut,scrTextOut
    textOut = [1,2]
    scrTextOut = [1,2]
    
    scrTextOut[0] = tk.Scrollbar(result)
    textOut[0] = tk.Text(result, height=10, width=80,state="disable",
                         yscrollcommand=scrTextOut[0].set)
    scrTextOut[0].config(command=textOut[0].yview)
    scrTextOut[0].grid(row=6, column=4, columnspan=1, sticky="S"+ "N")
    textOut[0].grid(row=6, column=0, columnspan=4)

    scrTextOut[1] = tk.Scrollbar(result)
    textOut[1] = tk.Text(result, height=10, width=80,state="disable",
                         yscrollcommand=scrTextOut[1].set)
    scrTextOut[1].config(command=textOut[1].yview)
    
#result end============================


#body
def aboutMe():
    tkMessageBox.showinfo("About DIG the GUI","Version:1.0\n Chong Tsz Man@2018")

root = tk.Tk()
root.title("Dig the GUI")
menubar = tk.Menu(root)
menuList = tk.Menu(menubar, tearoff=0)
menuList.add_command(label="About DIG the GUI", command=lambda:aboutMe())
menuList.add_separator()
menuList.add_command(label="Exit", command=lambda:root.destroy())
menubar.add_cascade(label="Menu", menu=menuList)
root.config(menu=menubar)


debugList = tk.Menu(menubar, tearoff=0)
debugList.add_command(label="Turn On Debug Mode", command=lambda:turnOnDebug())
debugList.add_command(label="Turn Off Debug Mode", command=lambda:turnOffDebug())
menubar.add_cascade(label="Debug", menu=debugList)
root.config(menu=menubar)
mainUI()

root.mainloop()


#Chong Tsz Man@2018





