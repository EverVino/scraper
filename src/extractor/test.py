a = "https://www.eldiario.net/portal/2023/10/1"
b = "https://www.eldiario.net/portal/2023/10/1/page/2"


def get_date_from_url(s):
    splited = s.split("/")
    if splited[-2] != "page":
        return splited[-3] + "/" + splited[-2] + "/" + splited[-1]
    else:
        return splited[-5] + "/" + splited[-4] + "/" + splited[-3]


print(get_date_from_url(a))
print(get_date_from_url(b))
