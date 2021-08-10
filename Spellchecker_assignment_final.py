# problems on highlighting 
# non word - no problem (able to take in any weird capitalized in a word, and only highlights when it`s not in the corpus)
# real word - stay away from the word : try me

# dictionary search: just a slight problem when dehighlighting (sometimes work well sometimes dont)
#                  : to recreate the bug just type words that is existing in another words like: "the", "therma","thermall" (the and ther and therma exist in each other, which may end highlight the similar words)
#                  : demo purpose: stay away from similar word seach like: amnesia, covid ... words that has no root word before 

# update changes made for this version:
# 1) tokenize function - filter numeric and stop words (instead of putting in non word check function)
# 4) added minimal edit distance on the drop box for word correction (probability will be the first sort)
# 5) added indication status for program is running: in case GUI did pop up - status will indicate ready
# 6) included "re" library for search on symbols "./ ( ) etc"
# 7) real word check function - changed the else part on p_b,p_t instead of every rung or if, now changed to only 1 else (probability will be none instead of 100 in the earlier version)

# - - - - - - - LIBRARIES (PACKAGE) - - - - - -  - - - -
import pickle
import re
import nltk, string
from nltk.tokenize import word_tokenize, regexp_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
import numpy as np
import math
# - - - - - - - - - GUI LIBRARIES - - - - - - - - - - -
import sys
from PyQt5.QtWidgets import (
    QAction, QMenu, QFrame, QApplication, QWidget, QLineEdit, QPlainTextEdit,
    QVBoxLayout, QTextEdit, QLabel, QPushButton, QColorDialog, QScrollBar,
    QPlainTextEdit, QScrollArea, QSpacerItem, QSizePolicy, QCompleter, QListWidget,
    QListWidgetItem, QAbstractItemView)
from PyQt5.QtCore import QRegExp, QRect, QCoreApplication, Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QColor, QTextCharFormat, QFont, QTextCursor, QBrush


class spellChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spell Check System")
        self.input_Text = ''
        self.corpus = []
        self.dict = []
        self.dehigh = ['1']
        self.attempt = False

        # - - - - - - - - - - - CREATE LAYOUT GUI - - - - - - - - - -
        # setting up frame layer
        self.setGeometry(100, 100, 950, 500)
        self.Frame = QFrame()
        self.Frame.resize(300, 300)
        self.Frame.setStyleSheet("background-color: #8e93ad")

        # - - - - - - - - - QVBOXLAYOUT (FRAME) - - - - - - - -
        # setup the vertical box layout manager on the frame
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.Frame)
        self.setLayout(mainLayout)

        self.controlsLayout = QVBoxLayout()  # Controls container layout.
        mainLayout.addLayout(self.controlsLayout)
        # - - - - - - - - - QLABEL (LABELS) - - - - - - - - - -
        # Input box label
        self.label1 = QLabel(self.Frame, text="Please enter texts here")
        self.label1.setWordWrap(True)

        # dictionary box label
        self.dict_Label = QLabel(self.Frame, text="Dictionary")
        self.dict_Label.setWordWrap(True)

        # search box label
        self.search_Label = QLabel(self.Frame, text="Search")
        self.search_Label.setWordWrap(True)

        # color legend label 
        self.legend = QLabel(self.Frame, text="Legend: ")
        self.non_word_legend = QLabel(self.Frame, text="Non word error")
        self.real_word_legend = QLabel(self.Frame, text="Real word error")

        # word count label
        self.word_count = QLabel(self.Frame, text="Word count: ")

        # - - - - - - - - - QTEXTEDIT (BOXES) - - - - - - - - -
        # input text box
        self.input_Text_Box = MyTextEdit(self.Frame)
        self.input_Text_Box.setPlainText('Text Editor (500 words)')

        # corpus instantiate for dictionary + unique filter

        self.corpus = self.input_Text_Box.setupCorpus()  # uni dict - words
        # [self.dict.append(word) for word in self.corpus if word not in self.dict]
        self.completer = QCompleter(self.corpus)  # putting unique words to the completer box

        # Dictionary box - list widget
        self.list_widget = QListWidget(self.Frame)
        self.list_widget.setGeometry(595, 125, 320, 160)
        self.list_widget.setStyleSheet("background-color: #cecace")

        for items in self.corpus:
            items = QListWidgetItem(items)
            self.list_widget.addItem(items)

        self.list_widget.sortItems()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        # Search bar box
        self.search_Bar = QLineEdit(self.Frame, text=' search here')
        self.search_Bar.setCompleter(self.completer)
        self.search_Bar.textChanged.connect(self.update_display)

        # Menu bar box
        self.menu_Bar = QLineEdit(self.Frame, text='  Spell-check system')

        # - - - - - - - - - BUTTONS - - - - - - - - - - - - -
        # check button
        self.spell_check = QPushButton(self.Frame, text="CHECK")
        self.spell_check.setToolTip("Change value of label")
        self.spell_check.clicked.connect(self.get_Text)

        # close button
        self.close_prog = QPushButton(self.Frame, text="QUIT")
        self.close_prog.setToolTip("Exit window")
        self.close_prog.clicked.connect(self.exit_window)

        # - - - - - - - -  QSTYLESHEET (FONTSTYLES, BACKGROUND COLOR, POSITION, RESIZE) - - - - - - - - - - -
        self.style(self.label1, "None", 1000, 25, 30, 65, "15px")               # LABEL (PLEASE ENTER WORDS)
        self.style(self.dict_Label, "None", 1000, 30, 630, 90, "15px")          # DICTIONARY CAPTION
        self.style(self.search_Label, "None", 1000, 30, 630, 290, "15px")       # SEARCH CAPTION
        self.style(self.input_Text_Box, "#cecace", 540, 300, 20, 100, "12px")   # INPUT BOX
        self.style(self.search_Bar, "#cecace", 165, 30, 690, 290, "15px")       # SEARCH BOX
        self.style(self.menu_Bar, "#cecace", 880, 35, 20, 20, "15px")           # MENU BAR CAPTION
        self.style(self.spell_check, "white", 80, 30, 20, 420, "14px")          # CHECK BUTTON
        self.style(self.close_prog, "white", 80, 30, 120, 420, "14px")          # QUIT BUTTON
        self.style(self.legend,"None",70, 30, 410, 405, "15px")                 # LEGEND LABEL
        self.style(self.non_word_legend,"#ff8080",85, 20, 470, 410, "12px")     # NON WORD ERROR LABEL WITH RED
        self.style(self.real_word_legend,"#95b8e3",85, 20, 470, 430, "12px")    # REAL WORD ERROR LABEL WITH BLUE
        self.style(self.word_count,"None",120, 30, 280, 405, "15px")                 # LEGEND LABEL
        print("Status: Ready")

    # - - - - - - - -  FUNCTIONS - - - - - - - - - - - -
    def style(self, widget, background, resize_x, resize_y, pos_x, pos_y, font_Size):
        widget.setStyleSheet("background-color:" + background + "; font: None; font-size: " + font_Size)
        widget.resize(resize_x, resize_y)
        widget.move(pos_x, pos_y)

    def get_Text(self):
        self.input_Text = self.input_Text_Box.toPlainText()
        self.main(self.input_Text)

    def exit_window(self):
        print("Quit program")
        QCoreApplication.instance().quit()

    # dictionary update - auto scroll
    def update_display(self, text):
        print(text)
        try:
            item = self.list_widget.findItems(text, Qt.MatchFlag.MatchRegExp)[0]
            item.setBackground(QColor('#ffffb5'))
            self.list_widget.scrollToItem(item, QAbstractItemView.PositionAtCenter)
            self.attempt = True
            self.dehigh.append(text)
            print(self.dehigh)

        except:
            if self.attempt == True:
                print(self.dehigh, 'yay')
                item = self.list_widget.findItems(self.dehigh[1], Qt.MatchFlag.MatchRegExp)[0]
                item.setBackground(QColor('#cecace'))
                self.dehigh.pop(1)
                self.attempt = False
            else:
                pass
            print('invalid search word')

    # - - - - - - EXECUTABLE - - - - - - - - -
    def main(self, input_Text):
        self.input_Text_Box.dehighlight()
        self.input_Text_Box.non_word_list = []
        inText = self.input_Text_Box.tokenize(self.input_Text)
        self.word_count.setText("Word count: " + str(len(inText)))
        self.input_Text_Box.word_check(inText)


class MyTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(MyTextEdit, self).__init__(parent)
        self.is_first_input = True
        self.uni_dict = {}
        self.bi_dict = []
        self.bi_dict_right = {}
        self.tri_dict = {}
        self.non_word_list = []
        self.non_word_candidate = []
        self.wLen_dict = {}
        self.real_word_list = {}
        self.real_word_candidate = []

    # - - - - - - - - - - - - SPELLCHECKING FUNCTIONS RELATED - - - - - - - - -
    def tokenize(self, input_text):
        input_tokens = word_tokenize(input_text)
        stop_tokens = list(string.punctuation)
        filtered_tokens = []
        for token in input_tokens:
            #token = token.lower()
            #print("lowered: ",token)
            if token not in stop_tokens and not token.isnumeric() and not token[0:2].isupper():
                #print("filter numeric and stop token: ",token)
                # if re.search('\.\?\)\(\;,', token):
                if re.search('\.', token):
                    ws = nltk.regexp_tokenize(token, '\w+')
                    for i in ws:
                        filtered_tokens.append(i)
                else:
                    #print('filtered: ',token)
                    filtered_tokens.append(token)

        #print(filtered_tokens)
        return filtered_tokens

    def setupCorpus(self):
        print("Initializing ...")
        # load uni dict pickle format
        uni_dict = open("D:/awi/Documents/UNI/AI Master Sem 2/NLP/python/uni_dict_pick_100k", "rb")
        unique_words = pickle.load(uni_dict)
        self.uni_dict = unique_words


        self.unique_words = list(self.uni_dict.keys())
        #print("Unique", len(self.unique_words))
        for word in self.unique_words:
            if len(word) not in self.wLen_dict:
                self.wLen_dict[len(word)] = set()
            self.wLen_dict[len(word)].add(word)
        # print(self.wLen_dict)

        # load bigram dict
        bi_dict = open("D:/awi/Documents/UNI/AI Master Sem 2/NLP/python/bi_dict_pick_100k", "rb")
        bigram_words = pickle.load(bi_dict)
        self.bi_dict = bigram_words

        # load the bigram dict right
        bi_dict_right = open("D:/awi/Documents/UNI/AI Master Sem 2/NLP/python/bi_dict_Right_pick_100k", "rb")
        bigram_words_right = pickle.load(bi_dict_right)
        self.bi_dict_right = bigram_words_right

        # load the trigram dict
        tri_dict = open("D:/awi/Documents/UNI/AI Master Sem 2/NLP/python/tri_dict_pick_100k", "rb")
        trigram_words = pickle.load(tri_dict)
        self.tri_dict = trigram_words

        # print(type(self.uni_dict))
        return self.uni_dict

    # word check on input text
    def word_check(self, input_tokens):  
        # access/iterate token from list of tokenize input text 
        # (original token) - input text token that has not been lower case 
        # (lowered case token) - lower casing input text   
                
        for token in input_tokens:                  
            origin_token = token                    
            token = token.lower()                   

            # if token does not exist in the dictionary of the token length and token length is more than 1
            # append original token into non-word list
            # highlight the non-word error
            
            if token not in self.wLen_dict[len(token)] and len(token) > 1:   
                self.non_word_list.append(origin_token)
                self.highlight(error_type=1)

        # print the list of non-word error
        print("Non-word Error:", self.non_word_list) 

        # proceed passing on real word check callback/function
        # highlight the real-word error
        self.real_word_check(input_tokens, self.uni_dict)
        self.highlight(error_type=2)

    def highlight(self, error_type):
        # set format for background color
        cursor = self.textCursor()
        if error_type == 1:
            fmt = QTextCharFormat()
            fmt.setBackground(QColor('#ff8080'))
            self.moveCursor(QTextCursor.Start)
            pointer = 0
            for text in self.non_word_list:
                #expression = QRegExp(text+'[ ,.]')
                expression = QRegExp(text,Qt.CaseInsensitive)
                index = expression.indexIn(self.toPlainText(), pointer)
                if index == -1:
                    continue
                pointer = index
                cursor.setPosition(index)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(text))
                cursor.mergeCharFormat(fmt)
        elif error_type == 2:
            fmt = QTextCharFormat()
            fmt.setBackground(QColor('#95b8e3'))
            self.moveCursor(QTextCursor.Start)
            pointer = 0
            for text in self.real_word_list.keys():
                expression = QRegExp(text+'[ ,.]')
                index = expression.indexIn(self.toPlainText(), pointer)
                pointer = index
                cursor.setPosition(index)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(text))
                cursor.mergeCharFormat(fmt)

    def dehighlight(self):
        # Restore the default color
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()

    def Calculate_Minimum_edit_distance(self, source, target):
        del_cost = 1
        ins_cost = 1
        sub_cost = 2
        n = len(source)
        m = len(target)
        MED_Matrix = np.zeros((n + 1, m + 1), dtype='int8')
        for i in range(1, n + 1):
            MED_Matrix[i][0] = MED_Matrix[i - 1][0] + del_cost
        for i in range(1, m + 1):
            MED_Matrix[0][i] = MED_Matrix[0][i - 1] + del_cost
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if source[i - 1] == target[j - 1]:
                    MED_Matrix[i][j] = min(
                        [MED_Matrix[i - 1][j] + del_cost, MED_Matrix[i - 1][j - 1] + 0,
                         MED_Matrix[i][j - 1] + ins_cost])
                else:
                    MED_Matrix[i][j] = min([MED_Matrix[i - 1][j] + del_cost, MED_Matrix[i - 1][j - 1] + sub_cost,
                                            MED_Matrix[i][j - 1] + ins_cost])
        # print(MED_Matrix)
        # print("Minimum edit Distance of " + source + " to " + target)
        return MED_Matrix[n][m]

    # non_word correction
    def get_candidate(self, selected_text, word_type):
        token = selected_text
        length_token = len(token)
        possible_words = []
        keys = []
        candidate_word = []
        if word_type == 1:
            self.non_word_candidate = []
        if word_type == 2:
            self.real_word_candidate = []
        if length_token > 2:
            keys.extend((length_token - 2, length_token - 1, length_token, length_token + 1, length_token + 2))
        elif length_token == 2:
            keys.extend((length_token - 1, length_token, length_token + 1, length_token + 2))
        elif length_token == 1:
            keys.extend((length_token, length_token + 1, length_token + 2))
        for key in keys:
            w = self.wLen_dict[key]
            # print(w)
            # S = ', '.join(w)
            possible_words.extend(self.wLen_dict[key])
        # print("Word", token, "is not in dictionary!")
        # print("Possible words are:", possible_words, "\n")
        for words in possible_words:
            # self.candidate_word.append(words)
            if self.Calculate_Minimum_edit_distance(token, words) <= 2:
                if word_type == 1:
                    ed = self.Calculate_Minimum_edit_distance(token, words)
                    # print("Correct word is", words, "occurence", self.uni_dict[words])
                    self.non_word_candidate.append((words, self.uni_dict[words] / sum(self.uni_dict.values()),ed ))
                    self.non_word_candidate.sort(key=self.getLength, reverse=True)
                    self.non_word_candidate.sort(key=lambda list:list[2], reverse=False)
                if word_type == 2:
                    ed = self.Calculate_Minimum_edit_distance(token, words)
                    real_word_candidate_tokens =[self.real_word_list[selected_text][1], words,
                                                 self.real_word_list[selected_text][2]]
                    score = self.real_word_check(real_word_candidate_tokens, self.uni_dict, sort_number=2)
                    self.real_word_candidate.append((words, score, ed))
                    self.real_word_candidate.sort(key=self.getLength, reverse=True)
                    self.real_word_candidate.sort(key=lambda list:list[2], reverse=False)

                # print(self.non_word_candidate)
        if self.non_word_candidate == []:
            self.non_word_candidate.append(("No Candidate",0))
        if self.real_word_candidate == []:
            self.real_word_candidate.append(("No Candidate",0))

    def getLength(self, key):
        return key[1]

    def make_bigram_model(self):
        model_bl = {}
        for key, value in zip(self.bi_dict.keys(), self.bi_dict.values()):
            model_bl[key] = value / self.uni_dict[key[0]]

        model_br = {}
        for key, value in zip(self.bi_dict_right.keys(), self.bi_dict_right.values()):
            model_br[key] = value / self.uni_dict[key[0]]
        return model_bl, model_br

    def make_trigram_model(self):
        model_t = {}
        for key, value in zip(self.tri_dict.keys(), self.tri_dict.values()):
            model_t[key] = value / ((self.bi_dict[key[:2]] + self.bi_dict_right[key[-1:-3:-1]]) / 2)
        return model_t

    def real_word_check(self, input_text, uni_corpus, sort_number=1):
        in_uni = [w for w in input_text if not w.isdigit()]
        in_bl = list(ngrams(in_uni, 2))
        in_br = [(w1, w2) for (w1, w2) in zip(in_uni[1:], in_uni[:-1])]
        in_tri = list(ngrams(in_uni, 3))

        left_bi, right_bi = self.make_bigram_model()
        tri_corpus = self.make_trigram_model()

        score_list = []  # this is the score list for real-word errors
        non_words = self.non_word_list
        real_words = {}
        k = []

        
        """"stupid backoff algorithm code by  for this function is based on code from this repository: https://github.com/ismaildawoodjee/Python-Spellchecker-GUI/blob/main/SpellChecker.py"""
        for t in in_tri:
            if t[1] not in uni_corpus:
                continue
            else:
                d = 0.4  # backoff discount
                ll = 0.25  # weighting on left bigram
                lt = 0.5  # weighting on trigram
                lr = 0.25  # weighting on right bigram
                thresh = 6e-5 * 1000  # threshold score to be considered a real-word error

                # if t is in trigram corpus
                if t in tri_corpus:
                    p_t = tri_corpus[t]
                # This is for bigram
                elif (t[:2] in left_bi) and (t[-1:-3:-1] in right_bi):
                    p_t = (d / 2) * (left_bi[t[:2]] + right_bi[t[-1:-3:-1]])
                # Left bigram
                elif t[:2] in left_bi:
                    p_t = d * left_bi[t[:2]]
                # Right bigram
                elif t[-1:-3:-1] in right_bi:
                    p_t = d * right_bi[t[-1:-3:-1]]
                # Unigram
                else:
                    p_t = d * d * uni_corpus[t[1]]
                if t[:2] in left_bi:
                    p_bl = left_bi[t[:2]]
                
                else:
                    p_bl = d * uni_corpus[t[1]]

                if t[-1:-3:-1] in right_bi:
                    p_br = right_bi[t[-1:-3:-1]]
                else:
                    p_br = d * uni_corpus[t[1]]

                score = ll * p_bl + lt * p_t + lr * p_br
                score = round(score, 3 - int(math.floor(math.log10(abs(score)))) - 1)
                score_list.append(score)
                if sort_number == 2:
                    return score
                elif score < thresh:
                    real_words[t[1]] = [score, t[0], t[2]]
        self.real_word_list = real_words
        print("Real-word Error:", self.real_word_list)
        #( print(score_list)

    # Mouse press event for mouse interaction on input text
    def mousePressEvent(self, event):
        # if it is a first mouse click / event
        # select all text object
        # clear the text in the input text
        # set the flag first input to false
        # continue/invalid after first click
        
        if self.is_first_input:
            self.selectAll()
            self.clear()
            self.is_first_input = False
        else:
            pass

        # set the mouse press event to the input text
        QPlainTextEdit.mousePressEvent(self, event)
        

    def contextMenuEvent(self, event):
        # initiate and set standard context of pop up menu as popup_menu 
        # initiate and set text cursor as cursor  
        # return word under the cursor 
        # print the word under the cursor

        popup_menu = self.createStandardContextMenu()
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)

        # if text cursor return a boolean of true for selection
        # set the selected text as selected_text
        # initiate spell menu option called Spellcheck Suggestions
        # prints the selected text 

        if cursor.hasSelection():
            selected_text = self.textCursor().selectedText()
            spell_menu = QMenu('Spellcheck Suggestions')
            print("Selected Text:", selected_text)

            # if selected text is an error / selected text exist in list of non-word error 
            # get potential candidate correction word for non-word error
            # intitate/set the legend for pop up menu
            # add legend for pop up menu 

            if selected_text in self.non_word_list:
                self.get_candidate(selected_text, 1)
                legend = SpellAction("Candidate\tEdit distance        Probability Score")
                spell_menu.addAction(legend)

                # access and iterate candidate correction word from list of non-word error candidate correction word]
                # if there is no candidate - slot in option of "No candidate"
                # else proceed and calculate minimum edit distance between selected text and candidate word 
                # add format for the probability to 5 decimal places into the spell menu
                # action of selection will invoke correct word call back for replacement of error word with correct word
                for word in self.non_word_candidate[0:10]:
                    if word[0] == "No Candidate":
                        action = SpellAction("No Candidate")
                        spell_menu.addAction(action)
                    else:
                        min_edit_distance = self.Calculate_Minimum_edit_distance(selected_text, word[0])
                        action = SpellAction(word [0]+"\t["+ str(min_edit_distance)+"]\t"+"                         {:.5f}".format(word[1])
                        , spell_menu)
                        action.correct.connect(self.correctWord)
                        spell_menu.addAction(action)

                # additional pop up menu graphics with separator between candidate word
                # add pop up menu spellcheck suggestion
                # provide global pop up feature within input text frame
                popup_menu.insertSeparator(popup_menu.actions()[0])
                popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)
                popup_menu.exec_(event.globalPos())

            # if selected text is an error / selected text exist in list of real-word error 
            # get potential candidate correction word for real-word error
            # intitate/set the legend for pop up menu
            # add legend for pop up menu
            elif selected_text in self.real_word_list.keys():
                self.get_candidate(selected_text, 2)
                legend = SpellAction("Candidate\tEdit distance        Probability Score")
                spell_menu.addAction(legend)

                # access and iterate candidate correction word from list of real-word error candidate correction word]
                # if there is no candidate - slot in option of "No candidate"
                # add format for the probability to 5 decimal places into the spell menu
                # action of selection will invoke correct word call back for replacement of error word with correct word
                for word in self.real_word_candidate[0:10]:
                    if word[0] == "No Candidate":
                        action = SpellAction("No Candidate")
                        spell_menu.addAction(action)
                    else:
                        min_edit_distance = self.Calculate_Minimum_edit_distance(selected_text, word[0])
                        action = SpellAction(word [0]+"\t["+ str(min_edit_distance)+"]\t"+"                         {:.5f}".format(word[1])
                        , spell_menu)
                        action.correct.connect(self.correctWord)
                        spell_menu.addAction(action)

                # additional pop up menu graphics with separator between candidate word
                # add pop up menu spellcheck suggestion
                # provide global pop up feature within input text frame
                popup_menu.insertSeparator(popup_menu.actions()[0])
                popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)
                popup_menu.exec_(event.globalPos())
            else:
                pass

    # Replaces the selected text with word.
    def correctWord(self, word):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(word.split()[0])
        self.dehighlight()
        cursor.endEditBlock()


# A special QAction that returns the text in a signal.
class SpellAction(QAction):
    correct = pyqtSignal(str)
    def __init__(self, *args):
        QAction.__init__(self, *args)
        self.triggered.connect(lambda x: self.correct.emit(str(self.text())))


app = QApplication(sys.argv)
prog = spellChecker()
prog.show()
sys.exit(app.exec_())
