from src.naver_API import Response
from konlpy.tag import Okt
import os
import sys
import traceback
import json
import datetime
import pandas as pd


class ExcelHandler:
    def __init__(self, excel_path: str, headers: list):
        self.excel_path: str = excel_path
        self.headers: list = headers
        if os.path.exists(self.excel_path):
            self.is_created = True
        else:
            self.create_file(excel_path=self.excel_path, headers=self.headers)

    def create_file(self, excel_path: str, headers: list):
        if os.path.exists(excel_path):
            sys.stdout.write(f"[INFO]: The excel file is already exists.\nPath: [{excel_path}]")
            return traceback.format_exc()

        else:
            os.mkdir(excel_path)
            self.excel_path = excel_path
            self.headers = headers
            df = pd.DataFrame(columns=headers)
            cnt = 1
            df.to_excel(self.excel_path)
            sys.stdout.write(f"[INFO]: The excel file has been created.\nPath: [{excel_path}]")
            self.is_created = True

    def put_data(self, data: dict, overwrite: bool = False):
        if not self.is_created:
            sys.stdout.write("[INFO]: The excel file has not been created yet. "
                             "Please make sure to create the file first.")
            return traceback.format_exc()

        else:
            if not overwrite:
                df = pd.read_excel(self.excel_path)
                print(df.columns)
                print(self.headers)
                cnt = df.shape[0] + 1
                for post in data:
                    df.loc[cnt] = [post[key] for key in post.keys()]
                    cnt += 1
            else:
                df = pd.DataFrame(columns=self.headers)
                cnt = 0
                for post in data:
                    df.loc[cnt] = [post[key] for key in post.keys()]
                    cnt += 1

            df.to_excel(self.excel_path, index=False)
            sys.stdout.write(f"[INFO]: The data has been put to the file successfully.\n"
                             f"Path: [{self.excel_path}]")


def save_as_excel(response: Response, headers: list):
    column_titles = headers
    data_frame = pd.DataFrame(columns=column_titles)
    cnt = 1
    for post in response.cooked_data:
        tmp_list = [post[key] for key in column_titles if key != "similarity"]
        tmp_list.append(sum(response.similar_pt[post["id"]]))
        data_frame.loc[cnt] = tmp_list
        cnt += 1
    current_date = datetime.datetime.now().strftime("%y%m%d-%H%M")
    data_frame_result = data_frame
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "..", "res", "static", "excel", f"posts[{current_date}].xlsx")
    data_frame_result.to_excel(file_path, index=False)
    return data_frame_result


def update_target_groups(data: dict, headers: list, overwrite: bool = False):
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "res", "static", "excel", "target_groups.xlsx")
    if os.path.exists(file_path):
        target_groups = ExcelHandler(excel_path=file_path, headers=headers)
        target_groups.put_data(data=data, overwrite=overwrite)


def get_target_possibility(target_headers: list, df: pd.DataFrame = None):
    if not df:
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..", "res", "static", "excel", "target_groups.xlsx")
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)

        else:
            sys.stdout.write("[INFO]: The excel file for target group has not been created yet. "
                             "Please make sure to create the file first.")
            return traceback.format_exc()
    okt = Okt()

    result_dict = {header: [] for header in target_headers}
    stats_dict = {}

    for idx, post in df.iterrows():
        #  print(post)
        for header in target_headers:
            if isinstance(post[header], str):
                words = okt.nouns(post[header])
            result_dict[header].extend(words)

    for header in target_headers:
        tmp_words = result_dict[header]
        header_stat = {}
        for word in tmp_words:
            if word not in header_stat.keys():
                header_stat[word] = 1
            else:
                header_stat[word] += 1

        total = sum(header_stat.values())-len(header_stat.values())
        result_dict[header] = [[word, header_stat[word], round((header_stat[word]/total), 3)]
                               for word in header_stat.keys() if header_stat[word] >2]
        result_dict[header].sort(reverse=True, key=lambda x: [x[1], x[0]])
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "res", "static", "json", "criteria.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False)
    sys.stdout.write(f"The data for target group is saved in \n[ {file_path} ]")
    return result_dict
