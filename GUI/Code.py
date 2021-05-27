import re
import numpy as  np
import pandas as pd
def differentiate(reply):
    reply_list=reply.split()
    for i in ['can','could','might','should','say','ask','must','tell']:
        if i in reply_list:
                return True
    return False

def review_generator(number,context):
    df=pd.read_csv('zomato.csv',encoding="ISO-8859-1", low_memory=False)
    d=0
    #print(df['reviews_list'][:10])
    p=re.compile(r'\b(most|worst|worse|best|top|least)\b')
    q=p.search(context)
    word=None
    if(q):
        q=q.span()
        word=context[q[0]:q[1]]
        #print(word)
        flag=context.split().index(word)
        while "not"==context.split()[flag-1]:
            flag-=1
            d+=1
    d%=2
    l=list(df['name'])
    l=[x.lower() for x in l]
    flag=0
    for i in context.split():
        if i in l:
            flag=1
            break
    if(flag==0):
        return "In a specific hotel only we can provide the reviews."
    reviews=df['reviews_list'][l.index(i)].lstrip("[").rstrip("]")
    #print(reviews,'\n',type(reviews))
    res = []
    temp = []
    for token in reviews.split(", "):
        st= token.replace("(", "").replace(")", "")
        temp.append(st.strip("\"").strip("'"))
        if ")" in token:
            res.append(tuple(temp))
            temp = []
    reviews=res
    #print(reviews[:5])
    if(reviews==None):
        return "Sorry,for this restaurant the data is not available."
    flag2=1
    if("rating" in context.split()):
        #print("kill")
        num=context.split()[context.split().index("rating")+1]
        if(num.isnumeric()):
            num=int(num)
        else:
            numb=re.compile(r"\b(one|two|three|four|five)\b")
            dic={'one':1,'two':2,'three':3,'four':4,'five':5}
            p=numb.match(num)
            if(p==None):
                flag2=1
            else:
                num=dic[num]
                flag2=0
        if(int(num)>5):
            return "They are rated out of 5"
    reviews_2=[]
    if(flag2==0 and d==0):
        reviews_2=[]
        y=number
        for i in reviews:
            p='Rated'+' '+str(float(num))
            if(i[0]==p):
                reviews_2.append(i[1])
                y-=1
            if(y<=0):
                break
    if(((word=="top" or word=="best")and d==0) or ((word=="least" or word=="worst")and d==1)):
        y=number
        for i in reviews:
            p='Rated'+' '+str(float(5))
            #print(i)
            if(i[0]==p):
                reviews_2.append(i[1])
                y-=1
            if(y<=0):
                break
    if(((word=="top" or word=="best")and d==1) or ((word=="least" or word=="worst")and d==0)):
        y=number
        for i in reviews:
            p='Rated'+' '+str(float(1))
            if(i[0]==p):
                reviews_2.append(i[1])
                y-=1
            if(y<=0):
                break
    s=''
    j=0
    for i in reviews_2:
        l=i.split("\n")
        p=[]
        for k in l:
            k=k[k.index("\\n"):].replace("\\n","\n").strip("\n")
            p.append(k)
        #print(l)
        p=" ".join(p)
        s=s+str(j)+". "+p
        j+=1
    return s
        
    

def generate(reply):
    l=reply.split()
    for i in l:
        num=re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\b")
        dic={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}
        p=num.search(i)
        if(i.isnumeric() or p):
            if(p!=None):
                s=dic[i]
            else:
                s=int(i)
            if(int(i)>10):
                return "Too much to be readable"
    if("reviews" in l):
        response=review_generator(s,reply)
        if(response==''):
            return ("Information is not available.")
        return response
    return ("Can you explain properly like what you want!")


def extract_answer(reply):
    if(differentiate(reply)):
        l=reply.split()
        if "ask" in l:
            pronouns=re.compile(r"\b(h+(im|er|e))\b|\bshe\b|\bthe person\b")
            ch=pronouns.search(reply).span()
            l=reply[0:ch[0]-1]+" you"+reply[ch[1]:]
            l=l.split()
            if "." in l:
                l.remove(".")
            elif "." in l[-1]:
                l[-1]=l[-1][0:len(l[-1])-1]
            ind=l.index('ask')
            if l[ind+1]=="whether":
                ques=l[ind+1:]
                ques[0]="if"
                ques.append("?")
                return (" ".join(ques),1)
            elif l[ind+1]=="about" or l[ind+1]=="that":
                ques=l[ind+2:]
                ques.append("?")
                return (" ".join(ques),1)
    ques_patt=re.compile(r"\b((wh+(o|a+t|ere|y|en))|how)\b")
    matche=ques_patt.search(reply)
    if(matche!=None):
                if "." in reply:
                    reply=reply[0:len(reply)-1]
                p=matche.span()[0]
                q=reply[p:].split()[1]
                pronouns=re.compile(r"\b(h+(im|er|e))\b|\bshe\b|\bthe person\b")
                ch=pronouns.search(reply[p:]).span()
                verb=reply[p:][ch[0]:].split()[1]
                #print(verb)
                ques=reply[matche.span()[0]:matche.span()[1]]+" do you "+reply[p:][(ch[1]+len(verb)+(ch[1]-ch[0])):]
                ques+='?'
                return (" ".join(ques),2)
    fi=r"\b(find|display|show)\b"
    pr=r"\b(top|most|least|worst)\b"
    p=re.search(fi,reply)
    q=re.search(pr,reply)
    if(p!=None):
        if(q!=None):
            l=generate(reply)
            return (l,4)
        else:
            return (reply[p.span()[0]:],4)
    else:
        return(reply,3)
#print(extract_answer("you should ask where he wants to have coffee.".lower()))
#print(extract_answer("You can ask whether he want to have coffe.".lower()))
#print(extract_answer("You should display top 10 reviews in Jalsa".lower()))
#print(extract_answer("when he does like to have coffe".lower()))
#print(extract_answer("You should display top 10 reviews rating 4 in Jalsa".lower()))