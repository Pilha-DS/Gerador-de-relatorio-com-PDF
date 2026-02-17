import os
import json

def join_path(path_a: list = None, basepath: bool = False)->str:
    '''
        Create path using path_a
        or
        Create absolute path using path_a
    '''
    if not path_a:
        print(" --- Empty path --- ")
        return False

    c_path = ""

    if basepath:
        basepath_init = os.path.dirname(__file__)
        c_path = os.path.join(basepath_init, "..", "..")

    for p in path_a:
        c_path = os.path.join(c_path, p)

    return c_path

def tlt(phrase: str = "", lang: str = "en", ltl_archive:str = "initial_screen") -> str:
    translations_path = join_path(["default", "translations", f"{ltl_archive}.json"], True)

    if not phrase:
        print(" --- dont have phrase --- ")
        return False

    try:
        with open(translations_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get(lang, {}).get(phrase, "Translation not found")

    except FileNotFoundError:
        return "Translation file not found"
    except Exception as e:
        return f"Error: {e}"
    
def get_languages(ltl_archive):
    translations_path = join_path(["default", "translations", f"{ltl_archive}.json"], True)

    with open(translations_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Retorna algo assim:
    # [("en", "english"), ("br", "Portigues brasileiro")]
    return [(lang, content.get("base", lang)) for lang, content in data.items()]