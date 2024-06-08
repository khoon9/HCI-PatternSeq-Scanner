# 최댓 유사도보다 10이상 떨어지는 유사도를 가질 경우 대상에서 제외

def filter_on_path_dict(my_dict):
    max_value = max(my_dict.values())
    keys_to_delete = [key for key in my_dict if my_dict[key] < max_value - 10]
    for key in keys_to_delete:
        del my_dict[key]
    return my_dict