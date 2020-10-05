
def remove_blank_fields(request):
    valid_data={}
    for key in request.data.keys():
        if request.data[key] != "":
            # print(f"printing{key}")
            valid_data[key] = request.data[key] 
    print(request.data)
    return valid_data
