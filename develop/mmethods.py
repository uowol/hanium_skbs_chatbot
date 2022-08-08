from bson.json_util import dumps
import json

def get_table_contents(tag):
    contents = ""
    for i in range(10):
        title = "여행을 떠나요 즐거운 마음으로 우리함께 떠나요"
        writer = "김찬우"
        date = "2022/07/09"
        views = "12"
        rates = "99"
        content_id = i
        content = f"""<tr>
                <td style="width: 50%">
                    <a class="text-reset" href="/noticeboard/{tag}/{i}">
                        {title}
                    </a>
                </td>
                <!-- 작성자, 작성일, 조회수 -->
                <td style="width: 10%" class="text-center">
                    {writer}
                </td>
                <td style="width: 20%" class="text-center">
                    {date}
                </td>
                <td style="width: 10%" class="text-center">
                    {views}
                </td>
                <td style="width: 10%" class="text-center">
                    {rates}
                </td>
            </tr>"""
        contents = contents + content
    return contents
    
def _result(status, body):
    return {
        'status': status,
        'body': body
    }
    
def parse_json(data):
    return dumps(data)

def load_json(json_string):
    return json.loads(json_string)