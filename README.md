# ZOMATO CHATBOT 
Designing a chatbot for the zomato restaurant application.

Dataset preprocessing:
* Download the Zomato Bangalore dataset from the kaggle website(Link can be founf here: https://www.kaggle.com/himanshupoddar/zomato-bangalore-restaurants)
* Run the Data preprocessing.ipynb file under the Preprocessing folder. 
* This file needs to be run on colab.
* This preprocessing code will convert the csv file to json.

Training:
* After the preprocessing step, we need to train our data set. 
* For the training to happen, run the training.py file under the Training Folder using the commands python training.py on your windows machine.

GUI:
* The clean_ui.py is a main file which runs the chatbot. It takes the previously created model and json files.
* After the training phase, run the above file using the commands python clean_ui.py on your windows machine 
* After this a chatbot window will appear.
* The other file which is refered by clean_ui.py  is Code.py which provides the display of the reviews and extracts the responses from the assertive feedbacks. 
* Code.py uses the csv file to extract the reviews. 

To Display the reviews or for giving feedback:
* In order to give feedback, type “No” when the bot asks “Was this satisfactory?”
* A prompt will be displayed.
* In the prompt, type the response which the chatbot should give. The feedback can be assertive or a statement which the chatbot should give as a response.
* The response given will get stored in the Logged_responses.json file
* In order to display the top reviews for a restaurant, type “No” when the bot asks “Was this satisfactory?”
* In the prompt, type “Display the top 10 reviews of Jalsa restaurant” for the reviews. 
* The reviews for that restaurant gets displayed.
* The extracted reviews and the intent is extracted and will be stored in Logged_responses.json file.
