# Copyright (C) 2022 Deadpool
# 
# This file is part of Project.HITSZCourseConverter
# This script converts HITSZ course table to wake up app format
# 
# Project.HITSZCourseConverter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# Project.HITSZCourseConverter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Project.HITSZCourseConverter.  If not, see <http://www.gnu.org/licenses/>.

import sys, re
import pandas as pd
from parse import parse

time_split_tokens = [ "第1-2节", "第3-4节", "第5-6节", "第7-8节", "第9-10节", "第11-12节"]

my_course_path = sys.argv[1]
# wake up course path
wu_course_path = sys.argv[2]

my_course_table = pd.read_excel(my_course_path).to_csv()
tokens = my_course_table.split(",")
time_courses = []
tmp_tokens = []

""" clean data """
for token in tokens:
    is_append = False
    for time_split_token in time_split_tokens:
        if token.count(time_split_token) != 0:
            is_append = True
            if token != time_split_token and token[token.index(time_split_token) + len(time_split_token)] != "\"":
                token1 = "+" + token[:token.index(time_split_token) + len(time_split_token)] + "\""
                token2 = "\"" + token[token.index(time_split_token) + len(time_split_token):]
                tmp_tokens.append(token1)
                tmp_tokens.append(token2)
            else:
                tmp_tokens.append(token)

    if not is_append:
        tmp_tokens.append(token)    

tokens = tmp_tokens

""" parse course table into week_courses """
for time_split_token in time_split_tokens:
    start_idx = tokens.index(time_split_token)
    end_idx = start_idx + 1
    courses = []
    is_nextline = False
    for i in range(0, 7):
        course = []
        course_str: str = ""
        while True:
            if tokens[end_idx] == "":
                end_idx += 1
                break 
            if tokens[end_idx].count("\r\n") > 0:
                is_nextline = True
                break
            tokens[end_idx] = tokens[end_idx].replace("\n", "")
            course_str += ("," + tokens[end_idx])
            if tokens[end_idx].count(time_split_token) != 0:
                course_str = course_str.removeprefix(",")
                is_continue = False
                if course_str.count("+"):
                    is_continue = True 
                    course_str = course_str.replace("+", "")
                res = parse("\"{}[{}][{}][{}]{}\"", course_str)
                def parse_weeks(time_str: str):
                    ret = []
                    tokens = time_str.split("周")[0].split(",")
                    for token in tokens:
                        if token.isdigit():
                            ret.append(int(token))
                        else:
                            ranges = token.split("-")
                            for i in range(int(ranges[0]), int(ranges[1]) + 1):
                                ret.append(i)
                    return ret
                weeks = parse_weeks(res[2])
                _course = {
                    "course": res[0],
                    "teacher": res[1],
                    "week": weeks,
                    "location": res[3],
                    "time": res[4]
                }
                
                course.append(_course)
                if not is_continue:
                    end_idx += 1
                    break
                else:
                    course_str: str = ""
            end_idx += 1
        courses.append(course)
    time_courses.append(courses)

# for time_course in time_courses:
#     print(time_course)
#     print("")

""" convert to wakeup app format """
wakeup_excel = pd.DataFrame()
wakeup_excel = wakeup_excel.append(pd.Series(["课程名称", "星期", "开始节数", "结束节数", "老师", "地点", "周数"]), ignore_index=True)
for time in range(0, len(time_courses)):
    courses = time_courses[time]
    for course_idx, course_list in enumerate(courses):
        for course in course_list:
            name = course["course"]
            day = str(course_idx + 1)
            times = re.findall(r'[1-9]+\.?[0-9]*', course["time"])
            start = str(times[0])
            end = str(times[1])
            teacher = course["teacher"]
            location = course["location"]
            weeks = ""
            for idx, week in enumerate(course["week"]):
                if idx != len(course["week"]) - 1:
                    weeks += (str(week) + "、")
                else:
                    weeks += (str(week))     
            wakeup_excel = wakeup_excel.append(pd.Series([name, day, start, end, teacher, location, weeks]), ignore_index=True)

wakeup_excel.to_csv(wu_course_path, index=None, header=None, encoding='utf-8_sig')