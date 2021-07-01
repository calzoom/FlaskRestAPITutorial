import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"likes": 78, "views": 100000, "name": "POV video"},
    {"likes": 10000, "views": 80000000, "name": "How to make a REST"},
    {"likes": 35, "views": 200, "name": "Time"},
]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())
# input()

# response = requests.delete(BASE + "video/0")
# print(response)
# input()

# response = requests.get(BASE + "video/6")
# print(response.json())

# response = requests.patch(BASE + "video/2", {"views": 99, "likes":101})
response = requests.patch(BASE + "video/2")
print(response.json())