import datetime
from datetime import timedelta
import re

class Date:
    def __init__(self, meeting_date, text):
        md = meeting_date.split()
        date_num = []
        for n in md:
            date_num.append(int(re.sub('[^0-9]','',n)))
        self.meeting_day = datetime.date(date_num[0], date_num[1], date_num[2]) # (2020, 10, 7)
        self.text = text
    
    def preprocessing(self):
        self.text = re.sub("\n", " ", self.text)
        self.text = re.sub("\t", " ", self.text)
        self.text = re.sub("  +", " ", self.text)

        self.text = self.text.strip()
        self.text = self.text.split(".")

        time_text_list = []
        processed_sent = []
        regex = re.compile("\\d+년 *\\d+월 *\\d+일")

        # 정규표현식 - 0000년 00월 00일
        for i in range(len(self.text)):
            # print(self.text[i])
            contents = regex.search(self.text[i])
            # print('  '+self.text[i])
            if contents == None:
                continue
            # print('\\\\\\')
            processed_sent.append(i)
            date = self.text[i][ contents.span()[0]:contents.span()[1]]
            date = re.sub(" ", "", date)
            date = re.sub(r'[^0-9]', " ", date)

            year, month, day = date.split(" ")[0], date.split(" ")[1], date.split(" ")[2]
            time_text_list.append([datetime.date(int(year), int(month), int(day)) , self.text[i]])
            
        # 정규표현식 - 00월 00일
        regex = re.compile("\d+월 *\d+일")

        for i in range(len(self.text)):
            if i in processed_sent:
                continue
                
            contents = regex.search(self.text[i])
            
            if contents == None:
                continue

            date = self.text[i][contents.span()[0]:contents.span()[1]]
            date = re.sub(" ", "", date)
            date = re.sub(r'[^0-9]', " ", date)

            year, month, day = self.meeting_day.year, date.split(" ")[0], date.split(" ")[1]
            time_text_list.append([datetime.date(int(year), int(month), int(day)) , self.text[i]])
        
        korean_date = ["그제", "그저께", "어제", "오늘", "내일", "모레"]
        week_date = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        # date_express = ["이번주", "다음주", "저번주", "지난주"]


        # processed_list = []

        #datetime weekday > 월요일 = 0

        for i in range(len(self.text)):  
            date_tmp = self.meeting_day

            flag = -1
            week = 0

            sent_without_space = re.sub(" ", "", self.text[i])
            
            if "다음주" in sent_without_space or "오는" in sent_without_space:
                week += 1
            elif "저번주" in sent_without_space or "지난주" in sent_without_space:
                week -= 1

            for j in range(len(week_date)):
                if week_date[j] in sent_without_space:
                    flag = j
                    break

            if flag != -1 :
                if j - self.meeting_day.weekday() != 0 :
                    date_tmp += datetime.timedelta(days = (j - self.meeting_day.weekday())) + datetime.timedelta(days = week * 7)
                else:            
                    date_tmp += datetime.timedelta(days = week * 7)

                time_text_list.append([date_tmp, self.text[i]])
                
        for i in range(len(self.text)):
            date_tmp = self.meeting_day
            flag = 0

            if korean_date[0] in self.text[i]  or korean_date[1] in self.text[i]:
                date_tmp -= datetime.timedelta(days = 2)
                flag = 1
            elif korean_date[2] in self.text[i] : 
                date_tmp -= datetime.timedelta(days = 1)
                flag = 1
            elif korean_date[3] in self.text[i] : 
                date_tmp += datetime.timedelta(days = 0)
                flag = 1
            elif korean_date[4] in self.text[i]:
                date_tmp += datetime.timedelta(days = 1)
                flag = 1
            elif korean_date[5] in self.text[i] :
                date_tmp += datetime.timedelta(days = 2)
                flag = 1
            
            if flag == 1:
                time_text_list.append([date_tmp, self.text[i]])
    
        return time_text_list