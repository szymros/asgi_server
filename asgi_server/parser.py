import urllib.parse
from http import HTTPStatus


class HttpParser:
    @classmethod
    def parse(cls, request: str):
        lines = request.split("\r\n")
        method, path, query_params = cls.parse_url(lines[0])
        http_version = lines[0].split("/")[-1].strip()
        headers_end = lines.index("")
        body = "".join(lines[headers_end:])
        headers = []
        for line in lines[1:headers_end]:
            header = line.split(":")
            headers.append((header[0].strip().encode(), header[1].strip().encode()))
        return {
            "http_version": http_version,
            "method": method,
            "path": path,
            "query_string": query_params,
            "headers": headers,
            "body": body,
        }

    @classmethod
    def parse_url(cls, request: str):
        method_path_and_query = request.split("/")
        method = method_path_and_query[0].strip()
        path_and_query = method_path_and_query[1].split("?")
        path = "/" + path_and_query[0].split(" ")[0]
        query_params = path_and_query[1].split("&") if len(path_and_query) > 1 else []
        query_params = urllib.parse.quote_plus("&".join(query_params)).encode()
        return method, path, query_params

    @classmethod
    def parse_response(cls, data: dict):
        result = ""
        result += (
            f"HTTP/1.1 {data['status']} {HTTPStatus(int(data['status'])).phrase}\r\n"
        )
        for header, header_value in data["headers"]:
            result += f"{header.decode()}: {header_value.decode()}\r\n"

        result += "Connection: close\r\n"
        result += "\r\n"
        result += data["body"].decode()
        return result


# {'type': 'http.response.start', 'status': 200, 'headers': [(b'content-length', b'24'), (b'content-type', b'application/
# json')]}
# {'type': 'http.response.body', 'body': b'{"Hello":"from FastAPI"}'}
