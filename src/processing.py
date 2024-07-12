from src.naver_API import Response
import json
import sys
import datetime


def get_post_data_json(post, numbering: int) -> list:
    title = post['title']
    org_link = post['originallink']
    link = post['link']
    description = post['description']
    posted_date = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    posted_date = posted_date.strftime('%Y-%m-%d %H:%M:%S')

    result = {'number': numbering, 'title': title, 'description': description,
                        'org_link': org_link, 'link': org_link, 'posted_date': posted_date}
    return result


def organize_posts(response: Response) -> list:
    if not response.body:
        sys.stdout.write(f"The body of the response is None. [{response.body}]")
        response.cooked_data = None
        return response
    else:
        if response.data_type == "json":
            response.cooked_data = json.loads(response.body)
            cnt = 0
            json_result = []

            if (response.cooked_data is not None) and (response.cooked_data["display"] != 0):
                for post in response.cooked_data["items"]:
                    cnt += 1
                    json_result.append(get_post_data_json(post=post, numbering=cnt))
            response.cooked_data = json_result
            return response
        elif response.data_type == "xml":
            #  space for organizing xml reponse
            pass
        else:
            sys.stdout.write(f"The type of response is not supported type. [response type : {response.data_type}]")
            response.cooked_data = None
            return None

