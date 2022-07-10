# -*- coding: utf-8 -*-
# https://colab.research.google.com/drive/1ve9jFG2w6osSiyNTZbdGqI_Toj-HLA0_

import re
import numpy as np

import pymorphy2
from navec import Navec
from scipy.special import softmax

# git clone https://github.com/barrust/pyspellchecker.git
# cd pyspellchecker
# python setup.py install
from spellchecker import SpellChecker

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(783, 424)
        self.centralwidget = QWidget(MainWindow)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 0, 2, 1, 1)

        self.gridLayout = QGridLayout()
        self.btn = QPushButton(self.centralwidget)

        self.gridLayout.addWidget(self.btn, 8, 1, 1, 1)

        self.n_keys = QSpinBox(self.centralwidget)

        self.gridLayout.addWidget(self.n_keys, 2, 5, 1, 1)

        self.label_3 = QLabel(self.centralwidget)

        self.gridLayout.addWidget(self.label_3, 2, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.label = QLabel(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(14)
        font.setWeight(50)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.category = QLineEdit(self.centralwidget)
        self.category.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.category.sizePolicy().hasHeightForWidth())
        self.category.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.category, 1, 5, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)

        self.problem = QTextEdit(self.centralwidget)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.problem.sizePolicy().hasHeightForWidth())
        self.problem.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.problem, 1, 1, 7, 1)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 2, 1, 1)

        self.tableWidget = QTableWidget(self.centralwidget)
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.tableWidget, 3, 3, 5, 3)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ed_tech", None))
        self.btn.setText(QCoreApplication.translate("MainWindow", u"get predictions!", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u043b\u044e\u0447\u0435\u0432\u044b\u0445 \u0441\u043b\u043e\u0432:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043d\u0438\u0436\u0435 \u0442\u0435\u043a\u0441\u0442 \u0437\u0430\u0434\u0430\u0447\u0438:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043a\u0441\u0442 \u043e\u0442\u043d\u043e\u0441\u0438\u0442\u0441\u044f \u043a \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438:", None))
    # retranslateUi


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn.clicked.connect(self.predict_for_txt)
        self.n_keys.setRange(1, 10)
        self.n_keys.setValue(3)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['слово', 'вероятность принадлежности к классу'])
        font = QFont()
        font.setFamily(u"MS Shell Dlg 2")
        font.setPointSize(12)
        font.setWeight(40)
        self.label_3.setFont(font)
        self.label_2.setFont(font)
        self.label_3.setStyleSheet('color: rgb(30, 30, 247)')
        self.label_2.setStyleSheet('color: rgb(30, 30, 247)')
        self.btn.setFixedHeight(20)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.btn.setStyleSheet('''background: rgb(30, 30, 247);
        border-radius: 7px; color: white; font-weight: 1500; border: 0''')
        #self.lbl = QLabel(self)
        #self.lbl.setPixmap(QPixmap('./imgs/herobox-butterfly.jpg').scaled(170, 100))
        #self.gridLayout_2.addWidget(self.lbl, 10, 5)

    def predict_for_txt(self):
        task = self.problem.toPlainText()
        n = self.n_keys.value()
        preds = get_sentence_predictions(task)
        word_significancy = get_word_significancy(task, np.argmax(preds))

        self.category.setText(classes[np.argmax(preds)])
        self.tableWidget.setRowCount(n)

        keywords = []
        j = 0
        r = 0
        m = len(word_significancy)
        if m < n:
            n = m
        while len(keywords) < n:
            word = word_significancy[j]
            if word not in keywords:
                keywords.append(word)
                self.tableWidget.setItem(r, 0, QTableWidgetItem(word[1]))
                self.tableWidget.setItem(r, 1, QTableWidgetItem(str(round(word[0] * 100, 3)) + '%'))
                r += 1
            j += 1

        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    def cosine_similarity(a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)

    def token_to_embed_id(word):
        if word in stopWordsRu:
            return None
        for category, topic_words in zip(categories, allWords):
            if word in topic_words:
                return navec.vocab[category]
        if word in navec.vocab:
            return navec.vocab[word]
        return navec.vocab['<unk>']

    def text_to_ids(text: str):
        tokens = []
        embed_ids = []
        for word in punctuation.sub(' ', text).split():
            word = russian.correction(word.strip().lower())
            p = morph.parse(word)[0]
            embed_id = token_to_embed_id(p.normal_form)
            if embed_id is not None:
                tokens.append(word)
                embed_ids.append(embed_id)
        return tokens, embed_ids

    def get_sentence_predictions(sentence: str):
        tokens, embed_ids = text_to_ids(sentence)
        embeddings = np.array([navec.pq[embed_id] for embed_id in embed_ids])
        mean_emb = embeddings.sum(axis=0)

        results = [np.dot(class_emb, mean_emb) for class_emb in classes_emb]
        results = softmax(results)
        return results

    def get_word_significancy(sentence: str, class_: int):
        tokens, embed_ids = text_to_ids(sentence)
        embeddings = np.array([navec.pq[embed_id] for embed_id in embed_ids])

        results = [(cosine_similarity(token_emb, classes_emb[class_]), token)
                   for token, token_emb in zip(tokens, embeddings)]
        return sorted(results, reverse=True)

    with open('all_animals.txt', 'r', encoding='utf-8') as f:
        all_animals = set(f.read().split(','))

    with open('all_music.txt', 'r', encoding='utf-8') as f:
        all_music = set(f.read().split(','))

    with open('all_sport.txt', 'r', encoding='utf-8') as f:
        all_sport = set(f.read().split(','))

    with open('all_lit.txt', 'r', encoding='utf-8') as f:
        all_lit = set(f.read().split(','))

    allWords = (all_animals, all_music, all_sport, all_lit)
    categories = ("животные", "музыка", "спорт", "литература")

    path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
    navec = Navec.load(path)

    morph = pymorphy2.MorphAnalyzer()
    russian = SpellChecker(language='ru')
    punctuation = re.compile(r'[!()\-\[\]{};:\\,<>./?@#$%^&*_~—]')

    with open('russian.txt', 'r', encoding='utf-8') as f:
        stopWordsRu = set(f.read().split('\n'))

    classes = ['животные', 'спорт', 'музыка', 'литература']
    classes_emb = [navec[class_name] for class_name in classes]

    app = QApplication(sys.argv)

    form = MyWidget()
    palette = QPalette()
    palette.setBrush(QPalette.Background, QBrush(QPixmap("herobox-background-2.jpg").scaled(983, 464)))
    form.setPalette(palette)
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
