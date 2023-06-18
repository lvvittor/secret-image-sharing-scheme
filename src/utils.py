
def flatten_array(arr):
    flattened = []
    for sub_array in arr:
        if isinstance(sub_array, list):
            flattened.extend(flatten_array(sub_array))
        else:
            flattened.append(sub_array)
    return flattened