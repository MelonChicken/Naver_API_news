from src.naver_API import Response
import json
import os
from konlpy.tag import Okt


def get_criteria(target_titles) -> dict:
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "..", "res", "static", "json", "criteria.json")
    with open(file_path, 'r', encoding='utf-8') as file:
        criteria = json.load(file)

    formed_criteria = {key: {} for key in criteria.keys()}

    for title in target_titles:
        words = criteria[title]
        formed_criteria[title] = {word[0]: [word[1], word[2]] for word in words}

    return formed_criteria


def get_similarity_simple(response: Response, criteria: dict = None, target_titles: list = ["title", "description"]):
    posts = response.cooked_data

    if criteria is None:
        formed_criteria = get_criteria(target_titles=target_titles)
    okt = Okt()
    criteria_corpus = {title : formed_criteria[title].keys() for title in target_titles}
    for post in posts:
        word_pt = {}
        for title in target_titles:
            tmp_nouns = okt.nouns(post[title])
            #  print(f"current nouns{tmp_nouns}")
            word_pt[title] = []
            for word in tmp_nouns:
                if word in criteria_corpus[title]:
                    word_pt[title].append(formed_criteria[title][word][1])
        response.similar_pt[post["id"]] = [round(sum(word_pt[title]), 2) for title in target_titles]

    return response


def classifier_naive_beyes(response: Response, criteria: dict = None, target_titles: list = ["title", "description"]):
    posts = response.cooked_data

    if criteria is None:
        formed_criteria = get_criteria(target_titles=target_titles)
