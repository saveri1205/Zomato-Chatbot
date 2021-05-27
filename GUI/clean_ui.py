import tkinter
from tkinter import *
#from chat import get_response, bot_name
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
from tkinter import simpledialog; 
from Code import extract_answer
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


lemmatizer = WordNetLemmatizer()
model = load_model('chatbot.h5')

with open('zomato-data.json') as jsonfile:
    intents = json.load(jsonfile)
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    if(len(ints)>0):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['response'])
                break
    else:
        result="Sorry, we don't have the answer to the question.\n"
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res




class ChatApplication:   
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Restaurant Based Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,text="This is a restaurant based chatbot for Bangalore!", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.send)
    
    def send(self,event):
        msg = self.msg_entry.get()
        self.msg_entry.delete(0, END)
        print("first: ",msg)
        chat_history.append(msg)
        print(chat_history)
        if msg != '':
            msg1 = f"You: {msg}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg1)

            if(msg=='no'):
                res ="Please enter an alternate response"
                alt_response = simpledialog.askstring("Prompt","Please enter a valid response")
                #self.text_widget.insert(END, "Bot: Your alternate response to the question \' "+chat_history[-2]+"\' is:  " + alt_response + '\n\n')
                self.text_widget.insert(END, "Thank you, I have recorded your input! Please contine with your next question!\n\n") 
                fp=open("Logged_resonses.json","r")
                response=extract_answer(alt_response.lower())
                if(response[1]!=3):
                    self.text_widget.insert(END, "Bot: "+response[0]+"\n\n")
                    self.text_widget.insert(END, "Bot: Was this response satisfactory? \n\n") 
                #print(response)
                data = json.load(fp)
                new_entry=dict()
                new_entry["tag"]=chat_history[-2]
                new_entry["patterns"]=[chat_history[-2]]
                new_entry["responses"]=[response[0]]
                new_entry["context"]="user_response"
                data["intents"].append(new_entry)
                fp.close()
                fp=open("Logged_resonses.json","w")
                json.dump(data,fp,indent=4)
                fp.close()
                self.text_widget.configure(state=DISABLED)
                self.text_widget.see(END)
            elif(msg=="yes"):
                res = "Okay, please enter your next question!"
                self.text_widget.insert(END, "Bot: "+res+"\n\n")
                self.text_widget.configure(state=DISABLED) 
                self.text_widget.see(END)

            else:
                res = chatbot_response(msg)
                self.text_widget.insert(END, "Bot: "+res+"\n\n")
                self.text_widget.insert(END, "Bot: Was this response satisfactory? \n\n") 
                self.text_widget.configure(state=DISABLED) 
                self.text_widget.see(END)

if __name__ == "__main__":
    with open("Logged_resonses.json","w") as fp:
        d=dict()
        d["intents"]=[]
        json.dump(d,fp,indent=4)
        fp.close()
    app = ChatApplication()
    chat_history=[]
    app.run()