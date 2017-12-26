import vk_api
import threading
import random
import time


print('Velegram alpha 0.0.1')


login='kryuchkov2001@mail.ru'#input('login: ')
password='05032001dobropozalovat'#input('password: ')
n=10**200

vk=vk_api.VkApi(login=login, password=password)
vk.auth()
vk=vk_api.VkApi.get_api(vk)

id=vk.users.get()[0]['id']


Hint=input("Введите имя или фамилию, или и то и другое того, кому вы хотите отправить сообщение:  ")
frlist=vk.friends.search(q=Hint, count=10)
for i in range(int(frlist['count'])):
    print(str(i) +": " + frlist['items'][i]['first_name'] + " " + frlist['items'][i]['last_name'])
index=input("CHOOSE YOUR DESTINY: ")
frid=frlist['items'][int(index)]['id']


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

