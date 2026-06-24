import json
import re

def getTableName(name: str) -> str:
    """
    Returns the table name for the given name.
    """
    return f'cnx{name}'

def getBotRole(name: str) -> str:
    """
    Returns the role model for the given role.
    """
    result = ''
    if name in ('Cody', 'Chien', 'Asky'):
        result = f'You are a code analyst, your name is {name}.'
    return result

def convertMessage(lstRecord: list) -> list:
    """
    Converts a list of records to a list of messages.
    """
    result = []
    for record in lstRecord:
        message = {
            'role': record['role'],
            'content': record['content'],
        }
        result.append(message)
    return result

def getCurrentDateTime() -> str:
    """
    Returns the current date and time in the format YYYY-MM-DD HH:MM:SS.
    """
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def convertValidJson(jsContent: str) -> str:
    """
    Converts a string to valid JSON format.
    """
    print('#################### Start: ', jsContent)
    cleaned_content = jsContent.strip()

    # Loại bỏ các dấu ````json` và ```` ` nếu có
    if cleaned_content.startswith('```json'):
        cleaned_content = cleaned_content.replace('```json\n', '', 1).replace('\n```', '', 1)
    elif cleaned_content.startswith('```'):
        cleaned_content = cleaned_content.replace('```\n', '', 1).replace('\n```', '', 1)

    try:
        # Thử tải trực tiếp chuỗi JSON
        json.loads(cleaned_content)
        print('#################### End (success direct): ', cleaned_content)
        return cleaned_content
    except json.JSONDecodeError:
        # Nếu thất bại, thử làm sạch sâu hơn
        # Tìm kiếm và xử lý giá trị của khóa "Sample"
        # Regex để tìm "Sample": '...' hoặc "Sample": "..."
        match = re.search(r'("Sample":\s*)(["\'])(.*?)\2', cleaned_content, re.DOTALL)
        if match:
            key_part = match.group(1)
            quote_char = match.group(2)
            original_sample_value = match.group(3)

            # Thoát các ký tự đặc biệt trong giá trị Sample
            # Thay thế dấu nháy đơn bằng dấu nháy kép
            escaped_sample_value = original_sample_value.replace("'", '"')
            # Thoát dấu nháy kép
            escaped_sample_value = escaped_sample_value.replace('"', '\\"')
            # Thoát dấu gạch chéo ngược
            escaped_sample_value = escaped_sample_value.replace('\\', '\\\\')
            # Thoát các ký tự xuống dòng
            escaped_sample_value = escaped_sample_value.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')

            # Thay thế giá trị Sample đã sửa vào chuỗi gốc
            # Đảm bảo rằng giá trị mới được bao quanh bởi dấu nháy kép
            cleaned_content = cleaned_content.replace(match.group(0), f'{key_part}"{escaped_sample_value}"')

        try:
            parsed_json = json.loads(cleaned_content)
            print('#################### End (success deep clean): ', cleaned_content)
            return cleaned_content
        except json.JSONDecodeError as e:
            print(f"#################### JSONDecodeError after deep clean: {e}")
            print('#################### End (fail): ', jsContent)
            return jsContent # Trả về chuỗi gốc nếu không thể chuyển đổi