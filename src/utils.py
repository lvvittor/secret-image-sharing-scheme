
def flatten_array(arr):
    flattened = []
    for sub_array in arr:
        if isinstance(sub_array, list):
            flattened.extend(flatten_array(sub_array))
        else:
            flattened.append(sub_array)
    return flattened

def convert_to_matrix(array, width, height):
    matrix = []

    for i in range(height):
        row = []
        for j in range(width):
            row.append(array[i * width + j])
        matrix.append(row)

    return matrix