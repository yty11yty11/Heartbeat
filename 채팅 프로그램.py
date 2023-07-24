#ConnectionClient.py
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
from os.path import exists
import socket, _thread

#######################################
#          클라이언트 부분            #
#######################################

#Socket 설정
HOST = 'localhost'
PORT = 9009
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#연결 시작하는 함수 설정
def startConnection(dialog, hostentry, portentry):
    global sock
    if not len(hostentry.get()) == 0 and not len(portentry.get()) == 0:
        HOST = hostentry.get()
        PORT = int(portentry.get())
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            _thread.start_new_thread(recieveThread, ())
            destroyDialog(dialog)
            pass
        except Exception as e:
            print(e)
            messagebox.showerror("오류", "연결 실패\n")
            pass
    else:
        messagebox.showerror("오류", "다시 입력 바람")
        pass    
    pass

#메세지 보내는 함수 설정
def sendMessage(box, event):
    try:
        sock.send(box.get().encode())
        box.delete(0, 'end')
        pass
    except Exception as e:
        messagebox.showerror("오류", "\n" + str(e))
        pass
    pass

#파일 전송 함수
def sendFile(filename, event):
    data_transfered = 0
    if not exists(filename):
        return -1
    with open(filename, 'rb') as file:
        sock.send('#file'.encode())
        try:
            data = file.read(1024)
            while data:
                data_transfered += sock.send(data)
                data = file.read(1024)
                pass
            pass
        except Exception as e:
            return -2
        return 0
    pass
    
#메세지 받는 스레드 설정
def recieveThread():
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode()
            if message.strip().find('#id') == 0:
                chatbox.insert(END, "<섭> 닉네임 선택 바람")
            elif message.strip().find('#add') == 0:
                chatbox.insert(END, "<섭> [%s] 입장함" %message.strip()[5:])
            elif message.strip().find('#del') == 0:
                chatbox.insert(END, "<섭> [%s] 퇴장함" %message.strip()[5:])
                pass
            elif message.strip().find('#change') == 0:
                i = peoplebox.get(0, END).index(message.strip()[8:].split(' ')[0])
                peoplebox.delete(i)
                peoplebox.insert(i, message.strip()[8:].split(' ')[1])
                chatbox.insert(END, "<섭> - [%s]에서 닉네임을 [%s]로 변경" %(message.strip()[8:].split(' ')[0], message.strip()[8:].split(' ')[1]))
                pass
            elif message.strip().find('#list') == 0:
                peoplebox.delete(0, END)
                people = message.strip()[6:].split(' ')
                for item in people:
                    peoplebox.insert(END, item)
                    pass
                pass
            elif message.strip().find('#file') == 0:
                pass
            else:
                chatbox.insert(END, message)
                pass
            pass
        except OSError:
            pass
        except Exception as e:
            messagebox.showerror("오류 발생\n" + str(e))
            break
        pass
    sock.close()
    pass

##########################################
#               GUI 부분                 #
##########################################

#채팅방 접속 함수
def enterRoom():
    dialog = Toplevel()
    dialog.title("채팅방 접속")
    dialog.geometry("240x120")

    #dialog - Frame Layout
    hostframe = Frame(dialog)
    portframe = Frame(dialog)
    btnframe = Frame(dialog)
    hostframe.pack(side=TOP, padx=10, pady=10)
    portframe.pack(side=TOP, padx=10)
    btnframe.pack(side=BOTTOM, padx=10, pady=10)

    #dialog - Host Input
    hostlabel = Label(hostframe, text="호스트>> ", font=font)
    hostentry = Entry(hostframe, font=font, bd=3)
    hostlabel.pack(side=LEFT)
    hostentry.pack(side=RIGHT, expand=True, fill=X)
    
    #dialog - Port Input
    portlabel = Label(portframe, text="포트>> ", font=font)
    portentry = Entry(portframe, font=font, bd=3)
    portlabel.pack(side=LEFT)
    portentry.pack(side=RIGHT, expand=True, fill=X)

    #dialog - Ok, Cancel Btn
    okbutton = Button(btnframe, text="  확인  ", font=font, command = partial(startConnection, dialog, hostentry, portentry))
    spacelabel = Label(btnframe, text=" ", font=font)
    cancelbutton = Button(btnframe, text="  취소  ", font=font, command = partial(destroyDialog, dialog))
    okbutton.pack(side=LEFT)
    cancelbutton.pack(side=RIGHT)
    spacelabel.pack(side=RIGHT)

    dialog.mainloop()
    pass

#창 닫는 함수
def destroyDialog(dialog):
    dialog.destroy()
    pass

#채팅방 나가는 함수
def exitRoom():
    reply = messagebox.askquestion("채팅방 나가기", "현재 채팅방을 나가시겠습니까?",)
    if reply:
        try:
            sock.send("/quit".encode())
            sock.close()
            pass
        except:
            pass
        chatbox.delete(0, END)
        peoplebox.delete(0, END)
        pass
    pass

#귓속말 함수
def whisper(event):
    inputbox.delete(0, END)
    try:
        inputbox.insert(0, "/w %s "%peoplebox.get(peoplebox.curselection()[0]))
        pass
    except:
        inputbox.delete(0, END)
        pass
    pass

#보낼 파일 선택창 여는 함수
def openFileToSend():
    filename = filedialog.askopenfilename(title = "전송할 파일 선택")
    return filename

#파일 전송 함수
def sendFile():
    filename = openFileToSend()
    if filename:
        pass
    pass

#선택 채팅 기록 삭제 함수
def deleteChat():
    chat = chatbox.curselection()[0]
    if chat:
        try:
            chatbox.delete(chat)
            pass
        except Exception as e:
            print(e)
            pass
        pass
    else:
        pass
    pass

#모든 채팅 기록 삭제 함수
def deleteChatAll():
    chatbox.delete(0, 'end')
    pass

#tkinter GUI 기본 root 창 설정
root = Tk()
root.title("Connection")
root.geometry("700x500")

#폰트 관리자 선언
font = font.Font(family="맑은 고딕", size=10)

#메뉴 생성
menubar = Menu(root)
conmenu = Menu(menubar, tearoff=0)
conmenu.add_command(label="채팅방 접속하기", font=font, command = enterRoom)
conmenu.add_command(label="채팅방 나가기", font=font, command = exitRoom)
menubar.add_cascade(label="채팅 연결", font=font, menu = conmenu)
chatmenu = Menu(menubar, tearoff=0)
chatmenu.add_command(label="파일 보내기", font=font, command = sendFile)
chatmenu.add_separator()
chatmenu.add_command(label="선택 채팅 기록 삭제", font=font, command = deleteChat)
chatmenu.add_command(label="모든 채팅 기록 삭제", font=font, command = deleteChatAll)
menubar.add_cascade(label="채팅 옵션", font=font, menu = chatmenu)
root.config(menu = menubar)

#프레임 생성
listframe = Frame(root, padx=10, pady=10)
inputframe = Frame(root, padx=10, pady=5, bg="#cccccc")
peopleframe = Frame(root, padx=10, pady=10, bg= "#cccccc")
peopleframe.pack(side=RIGHT, fill=Y)
listframe.pack(side=TOP, expand = True, fill=BOTH)
inputframe.pack(side=BOTTOM, fill=X)

#메세지 입력창 설정
inputlabel = Label(inputframe, text = "메세지 :  ", font=font, bg="#cccccc")
inputlabel.pack(side=LEFT)
inputbox = Entry(inputframe, bd=3, font=font, takefocus=1)
sendbutton = Button(inputframe, text="전송", font=font, command = partial(sendMessage, inputbox, None), padx=15, bg="#cccccc")
sendbutton.pack(side=RIGHT)
spacelabel = Label(inputframe, text =" ", font=font, bg="#cccccc")
spacelabel.pack(side=RIGHT)
inputbox.pack(side=RIGHT, expand = True, fill=X)
root.bind('<Return>', partial(sendMessage, inputbox))

#채팅방 참여인원 표시창 설정
peoplelabel = Label(peopleframe, text="참여자 목록", font=font, bg="#cccccc", pady=4)
peoplelabel.pack(side=BOTTOM)
peoplebarY = Scrollbar(peopleframe)
peoplebarY.pack(side=RIGHT, fill=Y)
peoplebox = Listbox(peopleframe, font=font, yscrollcommand = peoplebarY.set)
peoplebox.bind('<<ListboxSelect>>', whisper)
peoplebox.pack(side=LEFT, expand = True, fill = Y)
peoplebarY.config(command = peoplebox.yview)

#채팅창 설정
scrollbarY = Scrollbar(listframe)
scrollbarY.pack(side=RIGHT, fill=Y)
scrollbarX = Scrollbar(listframe, orient=HORIZONTAL)
scrollbarX.pack(side=BOTTOM, fill=X)
chatbox = Listbox(listframe, font=font, yscrollcommand = scrollbarY.set, xscrollcommand = scrollbarX.set)
chatbox.pack(side=LEFT, expand = True, fill=BOTH)
scrollbarY.config(command = chatbox.yview)
scrollbarX.config(command = chatbox.xview)

root.mainloop()
