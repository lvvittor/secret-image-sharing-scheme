
def flatten_array(arr):
    flattened = []
    for sub_array in arr:
        if isinstance(sub_array, list):
            flattened.extend(flatten_array(sub_array))
        else:
            flattened.append(sub_array)
    return flattened

def convert_to_matrix(array):
    if len(array) != 300 * 300:
        raise ValueError("Array size must be 300 * 300")

    matrix = []
    for i in range(0, len(array), 300):
        row = array[i:i+300]
        matrix.append(row)

    return matrix