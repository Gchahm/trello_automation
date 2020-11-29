import os
import json
import dotenv

BASE_DIR = os.path.curdir
FILES_DIR = os.path.join(BASE_DIR, 'files')

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


def save_json_to_file(obj, file_name, is_dict=False):
    content = json.dumps([x for x in obj] if is_dict else [x.__dict__ for x in obj])
    file_path = os.path.join(FILES_DIR, file_name)
    f = open(file_path, 'w')
    f.write(content)
    f.close()


def load_json_from_file(file_name):
    file_path = os.path.join(FILES_DIR, file_name)
    f = open(file_path, 'r')
    result = f.read()
    f.close()
    return json.loads(result)


def get_env_variable(var_name, default=None):
    return os.environ.get(var_name, default)
