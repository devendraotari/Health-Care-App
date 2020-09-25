
def remove_blank_fields(request):
    valid_data=request.data
    for key in valid_data.keys():
        if valid_data[key] == " ":
            valid_data.pop(key)
    return valid_data
