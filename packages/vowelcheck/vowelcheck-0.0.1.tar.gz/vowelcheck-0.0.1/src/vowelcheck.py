def vowel_check(string):
    List = ["a","e","i","o","u"]
    if len(string) == 1:
        if string.isupper() == True:
            New_string = string.lower()
            for i in List:
                if New_string == i:
                    return "The Letter is Vovel"
            else :
                 return "The Letter is not Vovel"
        else:
            for tab in List :
                if string == tab:
                    return "The Letter is Vovel"
            else :
                return "The Letter is not Vovel"
    else:
        return ("String has incresed in length")


