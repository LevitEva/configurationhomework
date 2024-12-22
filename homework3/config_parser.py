import re
import sys
import yaml

# Регулярные выражения для обработки синтаксиса
SINGLE_COMMENT = r";.*"
MULTILINE_COMMENT = r"\|\#.*?\#\|"
STRUCT_PATTERN = r"struct\s*{\s*((?:\s*\w+\s+\w+,?)+)\s*}"
GLOBAL_PATTERN = r"global\s+(\w+)\s+(.+)"
CONSTANT_REF = r"\[(\w+)\]"
IDENTIFIER = r"[a-zA-Z][a-zA-Z0-9]*"
NUMBER = r"\d+"

def remove_comments(data):
    """Удаляет однострочные и многострочные комментарии"""
    data = re.sub(SINGLE_COMMENT, "", data)
    data = re.sub(MULTILINE_COMMENT, "", data, flags=re.DOTALL)
    return data

def parse_struct(text, globals=None):
    """Парсит структуру и возвращает словарь"""
    matches = re.findall(STRUCT_PATTERN, text)
    if not matches:
        raise ValueError("Invalid struct definition")

    result = {}
    for match in matches:
        items = match.split(",")
        for item in items:
            key, value = item.strip().split()
            if globals:
                value = resolve_constants(value, globals)
            result[key] = parse_value(value)
    return result

def parse_value(value):
    """Парсит значение: число, ссылку на константу, или структуру"""
    if re.match(NUMBER, value):
        return int(value)
    elif re.match(IDENTIFIER, value):
        return value
    elif re.match(STRUCT_PATTERN, value):
        return parse_struct(value)
    raise ValueError(f"Некорректное значение: {value}")

def parse_globals(text):
    """Парсит глобальные константы"""
    globals = {}
    for match in re.findall(GLOBAL_PATTERN, text):
        name, value = match
        globals[name] = parse_value(value)
    return globals

def resolve_constants(data, globals):
    """Заменяет ссылки на константы их значениями"""
    def replace_constant(match):
        const_name = match.group(1)
        if const_name in globals:
            return str(globals[const_name])
        raise ValueError(f"Неизвестная константа: {const_name}")

    return re.sub(CONSTANT_REF, replace_constant, data)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 config_parser.py <input_txt_file> <output_yaml_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        with open(input_file, "r") as f:
            data = f.read()

        # Удаление комментариев
        data = remove_comments(data)

        # Парсинг глобальных констант
        globals = parse_globals(data)

        # Замена константных ссылок
        data = resolve_constants(data, globals)

        # Парсинг структуры
        struct = parse_struct(data, globals)

        # Ghi dữ liệu YAML ra file
        with open(output_file, "w") as f:
            yaml.dump(struct, f, allow_unicode=True, default_flow_style=False)

        print(f"Output written to {output_file}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)  # In lỗi ra stderr
        sys.exit(1)

if __name__ == "__main__":
    main()
