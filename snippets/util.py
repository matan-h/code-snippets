import json
import os
import howdoi.howdoi as howdoi_base
import importlib


def howdoi(query: str, num_answers: int = 1, search_engine='duckduckgo', all_answer: bool = True):
    importlib.reload(howdoi_base)
    if search_engine != 'google':
        os.environ['HOWDOI_SEARCH_ENGINE'] = search_engine
    query = {
        'query': [query],
        'num_answers': num_answers,
        'all': all_answer,
        'json_output': True,
        'search_engine': search_engine,
        # default arguments:
        'explain': True,
        'pos': 1,
        'link': False,
        'color': False,
        'save': False,
        'remove': False,
    }
    try:
        result = howdoi_base.howdoi(query)
    except (howdoi_base.BlockError, howdoi_base.GoogleValidationError, howdoi_base.BingValidationError,
            howdoi_base.DDGValidationError) as e:
        result = {'error': str(e)}
    else:
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            return {'error': result}  # (Sorry, couldn't find any help with that topic)
    return result
