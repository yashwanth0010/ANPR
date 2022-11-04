import random

def space(s):
    u=s.replace(' ','')
    x = s
    x=x.replace('-',' ')
    x.upper()
    if(len(u)==10):
        x = u[0:2]+' '+u[2:4]+' '+u[4 :6]+' '+u[6:len(x)]
    return x

def Manipulate(s):
    x=s
    al=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    nu=['1','2','3','4','5','6','7','8','9','0']
    if(len(x)>10):
        if(x[0] in al and x[1] in al and x[2] in al):
            x=x[1:len(x)+1]
        if(x[len(x)-1] in nu and x[len(x)-2] in nu and  x[len(x)-3] in nu and x[len(x)-4] in nu and x[len(x)-5] in nu ):
            x=x[0:len(x)-1]
    return x



def change(s):
    x=s
    if(s[0]=='I' or s[0]=='i'):
        s=s[1:len(s)+1]

    if(s[0:4]=="IND" or s[0:4]=="ind"):
        s=s[4:len(s)+1]

    return s

def Random(s):
    if(len(s)<10):
        k=random.randint(1111,9999)
        w=str(k)
        s=s+w
    return s
