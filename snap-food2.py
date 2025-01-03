#کد مناسب

import pandas as pd
from hazm import word_tokenize,stopwords_list
from nltk.corpus.reader import WordListCorpusReader
import time
import string
class RestaurantScoreAnalyzer:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.data = self.file_reader()
        self.tokened_list = self.word_tokenizer(2)

    def file_reader(self):
        try:
            with open(self.csv_file_path, encoding="utf-8") as f:
                return pd.read_csv(f)
        except UnicodeDecodeError:
            with open(self.csv_file_path, encoding="ISO-8859-1") as f:
                return pd.read_csv(f)

    def word_tokenizer(self, column: int):
        """توکن‌سازی نظرات و حذف توقف‌واژه‌ها و علائم نگارشی"""
        punctuation = string.punctuation + '؟' + '،'
        term_set = {'عالی', 'خوب', 'بالا', 'کم', 'مناسب', 'زیاد'}  # استفاده از مجموعه برای جستجوی سریع‌تر
        stopwords_comment = set(stopwords_list()) - term_set

        # توکن‌سازی و فیلتر کردن در یک مرحله
        Main_li = [
            [
                word for word in word_tokenize(comment)
                if word not in stopwords_comment and word not in punctuation
            ]
            for comment in self.data.iloc[:, column]
        ]

        return Main_li

    def people_rate_sum(self, colmn):
        clean_rate_column = self.data.iloc[:, colmn].fillna(3).astype(int)
        return clean_rate_column.sum() / (self.data.shape[0] * 5)

    def score_by_word(self, tokened_list, term):
        term_words = set(term.words())
        score = 0
        for tokens in tokened_list:
            for j in range(len(tokens)):
                if tokens[j] in term_words or (j > 0 and (tokens[j - 1] + ' ' + tokens[j]) in term_words):
                    score += 1
                    break
        return score

    def calculate_final_comment_score(self, score):
        score_quality = score[0] / max((score[0] + score[1]), 1)
        score_delivery = score[2] / max((score[2] + score[3]), 1)
        score_cost = score[4] / max((score[4] + score[5]), 1)
        return score_quality, score_delivery, score_cost

    def calculate_final_score(self, final_comment_score, people_rate_sum):
        return (4 * people_rate_sum) + (3 * final_comment_score[0]) + (2 * final_comment_score[1]) + final_comment_score[2]

    def analyze_scores(self):
        # بارگذاری فایل‌های واژه‌ها
        quality_terms = WordListCorpusReader("C:\\Users\\Notebook\\Desktop\\data\\comment", ["quality_terms.txt"])
        neg_quality_terms = WordListCorpusReader("C:\\Users\\Notebook\\Desktop\\data\\comment", ["neg_quality_terms.txt"])
        delivery_terms = WordListCorpusReader("C:\\Users\\Notebook\\Desktop\\data\\comment", ["delivery_terms.txt"])
        neg_delivery_terms = WordListCorpusReader("C:\\Users\\Notebook\\Desktop\\data\\comment", ["neg_delivery_terms.txt"])
        cost_terms = WordListCorpusReader("C:\\Users\\Notebook\\Desktop\\data\\comment", ["cost_terms.txt"])
        neg_cost_terms = WordListCorpusReader("C:\\Users\\Notebook\\Desktop\\data\\comment", ["neg_cost_terms.txt"])

        # محاسبه امتیازها
        quality = self.score_by_word(self.tokened_list, quality_terms)
        neg_quality = self.score_by_word(self.tokened_list, neg_quality_terms)
        delivery = self.score_by_word(self.tokened_list, delivery_terms)
        neg_delivery = self.score_by_word(self.tokened_list, neg_delivery_terms)
        cost = self.score_by_word(self.tokened_list, cost_terms)
        neg_cost = self.score_by_word(self.tokened_list, neg_cost_terms)

        # محاسبه امتیاز نهایی
        list_score = [quality, neg_quality, delivery, neg_delivery, cost, neg_cost]
        final_comment_score = self.calculate_final_comment_score(list_score)
        people_rate = self.people_rate_sum(1)
        final_score = self.calculate_final_score(final_comment_score, people_rate)

        print('our score to your restaurant is ', round(final_score, 3), " from 10")

if __name__ == "__main__":
    start_time = time.time()
    analyzer = RestaurantScoreAnalyzer("snappfood.csv")
    analyzer.analyze_scores()
    end_time = time.time()
    print("مدت زمان اجرا:", round(end_time - start_time, 2), "ثانیه")

# our score to your restaurant is  5.903  from 10
# مدت زمان اجرا: 0.31 ثانیه

