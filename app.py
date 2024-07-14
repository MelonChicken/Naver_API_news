from src.naver_API import get_response
from src.processing import organize_posts
from src.storage import save_as_excel, update_target_groups, get_target_possibility
from src.nlp_model import get_similarity_simple
import sys
import traceback
import toml
import os

#  response = get_response()
#  print(f"|response|\n{response}")
#  print(f"raw_data : {response.raw}")
#  print(f"status_code : {response.status_code}")
#  print(f"body : {response.body}")


def update_target_info():
    response = get_response()
    if response.data_type not in ["xml", "json"]:
        sys.stdout.write(f"The data type of response is not supported."
                         f"\nPlease check the API to get response. "
                         f"[Data Type : {response.data_type}]")
        return traceback.format_exc()

    else:
        response = organize_posts(response)
        response_with_pt = get_similarity_simple(response=response)
        update_target_groups(data=response.cooked_data, headers=["index", "id", "title", "description", 'org_link', "link", "posted_date"])
        get_target_possibility(target_headers=["title", "description"])


def collect_info_naverapi():
    response = get_response()
    if response.data_type not in ["xml", "json"]:
        sys.stdout.write(f"The data type of response is not supported."
                         f"\nPlease check the API to get response. "
                         f"[Data Type : {response.data_type}]")
        return traceback.format_exc()

    else:
        response = organize_posts(response)
        response_with_pt = get_similarity_simple(response=response)
        new_media_interests = []
        for post in response_with_pt.cooked_data:
            tmp_cnt = 0
            point = 0
            tmp_cnt = sum(response_with_pt.similar_pt[post['id']])
            if 0.45 < tmp_cnt:
                point = tmp_cnt

            post['similarity'] = round(tmp_cnt, 2)
            if 0 < point:
                new_media_interests.append(post)
        #  save_as_excel(response=response_with_pt, headers=["index", "id", "title", "description", 'org_link', "link", "posted_date", "similarity"])

        return new_media_interests, response_with_pt



def check_naver():

    toml_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "res", "config.toml")
    with open(toml_dir, "r") as f:
        config_toml = toml.load(f)

    newest_news = config_toml["DISCORD"]["NEWEST_NEWS"]
    new_media_interests, response = collect_info_naverapi()
    #  print(new_media_interests)
    #  print(new_media_interests)
    #  print(newest_news)
    new_posts = [post for post in new_media_interests if newest_news < post["id"]]
    #  print(new_posts)
    current_newest_news = max([post["id"] for post in new_posts])
    if newest_news == current_newest_news:
        new_flag = False
    else:
        config_toml["DISCORD"]["NEWEST_NEWS"] = current_newest_news
        new_flag = True
    with open(toml_dir, "w") as f:
        toml.dump(config_toml, f)

    return new_flag, new_posts, response

#  check_naver()