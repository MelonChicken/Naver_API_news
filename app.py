from src.naver_API import get_response
from src.processing import organize_posts
from src.storage import save_as_excel
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
                         f"\nPlease check the API to get reponse. "
                         f"[Data Type : {response.data_type}]")
        return traceback.format_exc()

    else:
        response = organize_posts(response)
        save_as_excel(response=response)
        #  print(f"result: {response.cooked_data}")


run()
