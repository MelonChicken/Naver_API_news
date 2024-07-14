from src.naver_API import get_response
from src.processing import organize_posts
from src.storage import save_as_excel, update_target_groups, get_target_possibility
from src.nlp_model import get_similarity_simple
import sys
import traceback

#  response = get_response()
#  print(f"|response|\n{response}")
#  print(f"raw_data : {response.raw}")
#  print(f"status_code : {response.status_code}")
#  print(f"body : {response.body}")


def run():
    response = get_response()
    if response.data_type not in ["xml", "json"]:
        sys.stdout.write(f"The data type of response is not supported."
                         f"\nPlease check the API to get response. "
                         f"[Data Type : {response.data_type}]")
        return traceback.format_exc()

    else:
        response = organize_posts(response)
        response_with_pt = get_similarity_simple(response=response)
        #  update_target_groups(data=response.cooked_data, headers=["index", "id", "title", "description", 'org_link', "link", "posted_date"])
        #  get_target_possibility(target_headers=["title", "description"])
        save_as_excel(response=response_with_pt, headers=["index", "id", "title", "description", 'org_link', "link", "posted_date", "similarity"])
        #  print(f"result: {response.cooked_data}")
        #  print(response_with_pt.similar_pt)


run()
