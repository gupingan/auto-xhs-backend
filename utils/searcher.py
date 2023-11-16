"""
@File: searcher.py
@Author: 顾平安
@Created: 2023/11/9 17:32
@Description: Created in backend.
"""
import time

NOTE_TYPE_DICT = {
    'video': '视频',
    'normal': '图文'
}


def get_valid_items(data, count):
    items = data["data"]["items"]
    valid_items = [item for item in items if '-' not in item["id"]][:count]
    return valid_items


def get_desired_items(searcher, keyword, page, fixed_count, sort_type, note_type_):
    desired_count = 0
    result_items = []
    has_more = True

    while desired_count < fixed_count and has_more:
        time.sleep(0.314)
        data = searcher.notes(keyword, page, 20, sort_type, note_type_)
        valid_items = get_valid_items(data, fixed_count - desired_count)
        result_items.extend(valid_items)
        desired_count += len(valid_items)
        has_more = data["data"]["has_more"]
        page += 1

    return [{'noteId': item['id'], 'state': False, 'type': NOTE_TYPE_DICT.get(item['note_card']['type'])} for item in
            result_items[:fixed_count]]
