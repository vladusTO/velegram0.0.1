import vk_api
import threading
import random
import time
import shutil
import os
import re


print('Velegram alpha 0.0.1')


path='C:/Users/User/Desktop/Velegram.lnk'
if not os.path.isfile(path):
    target=os.path.abspath('velegramicon.lnk')
    target = re.sub('\\\\', '/', target)
    shutil.copy(target, path)
print('Программа создала ярлык на рабочем столе')
time.sleep(4)
print('Что? Он вам не нужен?Да мы *** клали на ваше мнение, я здеся царь бог, пока вы не удалите эту программу ваххахахахахах')

login=input('login: ')
password=input('password: ')
n=25195908475657893494027183240048398571429282126204032027777137836043662020707595556264018525880784406918290641249515082189298559149176184502808489120072844992687392807287776735971418347270261896375014971824691165077613379859095700097330459748808428401797429100642458691817195118746121515172654632282216869987549182422433637259085141865462043576798423387184774447920739934236584823824281198163815010674810451660377306056201619676256133844143603833904414952634432190114657544454178424020924616515723350778707749817125772467962926386356373289912154831438167899885040445364023527381951378636564391212010397122822120720357
i=0


vk=vk_api.VkApi(login=login, password=password)
vk.auth()
vk=vk_api.VkApi.get_api(vk)
print("Если ваш телефон подключен к сети, то вам пришло оповещение от вк, то что на ваш аккаунт кто-то зашёл")
time.sleep(3)
print("Не бойтесь, это я просто спиздил ваши данные, ладно шучу.")
time.sleep(3)
print("А может быть и нет")
id=vk.users.get()[0]['id']


while i==0:
    Hint=input("Введите имя или фамилию, или и то и другое того, кому вы хотите отправить сообщение:  ")
    frlist=vk.friends.search(q=Hint, count=10)
    for i in range(int(frlist['count'])):
        print(str(i) + ": " + frlist['items'][i]['first_name'] + " " + frlist['items'][i]['last_name'])
    if int(frlist['count'])>0:
        index=input("CHOOSE YOUR DESTINY: ")
        frid=frlist['items'][int(index)]['id']
        i+=1
    else:
        print('Ваш запрос не дал результатов, попробуйте еще раз')


def messageToNumber():
    flag=0
    while flag==0:
        message=str(input(">> "))
        chrcounter=''
        trMessage=''
        for chr in message:
            chrcounter=str(chrcounter) + str(len(str(ord(chr)))-1) + " "
            trMessage=str(ord(chr)) + str(trMessage)
        trMessage=[chrcounter, trMessage]
        if len(trMessage[1])<n:
            flag=1
    return trMessage


def keyScanner():
    frPubKey=' '
    while frPubKey==' ':
        fr_pub_key = vk.messages.get(count='1')['items'][0]['body']
        if fr_pub_key[0:8]=='!*@&#^$%':
            frPubKey=fr_pub_key.split()
    time.sleep(1)
    return frPubKey[1]


def getKey(FPK=None):  #надо сделать и статический pubkey чтобы отправлять сообщения даже когда человек оффлайн
    Hash=random.getrandbits(12)        #но тогда надо сделать таблицу в которую будут сохраняться пабкии    сделать функцию которая при каждой "встрече" создает                                        новый статический пабкии
    PubKey=3**Hash%n
    Key=13
    FrPubKey=13                                   #сохранять последний пабкии в таблицу
    while Key!=int(FrPubKey)**Hash%n:
        if FPK==None:
            vk.messages.send(user_id=frid, message='!*@&#^$%' + ' ' + str(PubKey))
            FrPubKey=int(keyScanner())
            Key=FrPubKey**Hash%n
        else:
            FrPubKey=int(FPK)
            vk.messages.send(user_id=frid, message='!*@&#^$%' + ' ' + str(PubKey))
            Key = FrPubKey ** Hash % n
    return Key


def sendMessage():
    crypt=messageToNumber()
    cryptMsg= int(crypt[1]) ^ getKey()
    vk.messages.send(user_id=frid, message=str(id) + ' ' + str(crypt[0]) + ' ' + str(cryptMsg))


def messageScanner():
    flag=0
    while flag==0:
        frmsg = vk.messages.get(count='1')['items'][0]['body']
        frmsg=frmsg.split()
        if frmsg[0] == str(frid):
            flag=1
    return frmsg


def deCryptMessage(Key):
    frCrypt=messageScanner()
    frCryptmsg=frCrypt[2]
    counter=frCrypt[1]
    a=0
    denumbered=''
    deCryptMsg=int(frCryptmsg)^Key
    for i in range(len(counter)):
        k=int(counter[i])
        denumbered = denumbered + str(chr(int(str(deCryptMsg)[a:a+k])))
        a+=k
    return denumbered


def sendMessageMode():
    while True:
        sendMessage()


def scannerMode():
    while True:
        Key=getKey(keyScanner())
        print(deCryptMessage(Key))

thread1=threading.Thread(target=sendMessageMode)
thread2=threading.Thread(target=scannerMode)
thread1.deamon=True
thread2.deamon=True
thread1.start()
thread2.start()

