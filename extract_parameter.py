def extract_params(content_file):
    lines = content_file[1:]
    parameters = []
    for line in lines:
        part = line.split('(')[1].split(')')[0]
        parameters.append(part)
    return parameters

def get_type(params):
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    number_of_int = 0
    for param in params:
        i = 0
        while i < len(param) and param[i] in digits:
            i += 1
        if i == len(param):
            number_of_int +=1
    return number_of_int > (len(params)/2)
