import requests

def call(user_id, student_id):
    url = 'http://10.60.7.253:8999/v1/call/makeCall'

    params = {
        'userId': user_id,
        'studentId': student_id
    }

    response = requests.get(url=url, params=params)
    print(response.content)

def main():
    params_list = [('100011', '307031'),('100439', '306959'), ('11', '86174')]
    for d in params_list:
        call(d[0], d[1])
    
if __name__ == '__main__':
    main()
