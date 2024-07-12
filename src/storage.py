from src.naver_API import Response
import os
import pandas as pd


def save_as_excel(response: Response):
    column_titles = ["number", "title", "description", 'org_link', "link", "posted_date"]
    data_frame = pd.DataFrame(columns=column_titles)
    cnt = 1
    for post in response.cooked_data:
        data_frame.loc[cnt] = [post[key] for key in column_titles]
        cnt += 1

        if cnt == len(response.cooked_data):
            data_frame_result = data_frame
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..", "res", "static", "excel", "posts.xlsx")
    data_frame_result.to_excel(file_path)
    return data_frame_result
