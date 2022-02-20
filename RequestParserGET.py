import requests
CRLF = '\r\n'
DEFAULT_HTTP_VERSION = 'HTTP/1.1'
protocol = "https://"
class RequestParser(object):
    def __parse_request_line(self, request_line):
        request_parts = request_line.split(' ')
        self.method = request_parts[0]
        self.url = request_parts[1]
        self.protocol = request_parts[2] if len(request_parts) > 2 else DEFAULT_HTTP_VERSION

    def __init__(self, req_text):
        req_lines = req_text.split(CRLF)
        self.__parse_request_line(req_lines[0])
        ind = 1
        colon_ind = req_lines[ind].find(':')
        self.url = protocol+req_lines[ind][colon_ind + 1:].lstrip()+self.url
        ind = 2
        self.headers = dict()
        while ind < len(req_lines) and len(req_lines[ind]) > 0:
            colon_ind = req_lines[ind].find(':')
            header_key = req_lines[ind][:colon_ind]
            header_value = req_lines[ind][colon_ind + 1:].lstrip()
            self.headers[header_key] = header_value
            ind += 1

    def __str__(self):
        headers = CRLF.join(f'{key}: {self.headers[key]}' for key in self.headers)
        return f'{self.method} {self.url} {self.protocol}{CRLF}' \
               f'{headers}{CRLF}'

    def to_request(self):
        req = requests.Request(method=self.method,
                               url=self.url,
                               headers=self.headers, )
        return req

f = open("request.txt", "r")
myreq = f.read().splitlines()
myreq2 = '\r\n'.join(myreq)
if __name__ == '__main__':
    r = RequestParser(myreq2)
    req = r.to_request()
    print("---------")
    print("url:\t\t", req.url)
    print("headers:\t\t", req.headers)
    print("data:\t\t", req.data)
    print("---------")
    response = requests.get(url=req.url, headers = req.headers)
    print("------Status Code-------")
    print(response.status_code)
    print("------------------------")
    print(response.text)
