from django.views.decorators.csrf import csrf_exempt
from collections import Counter
from django.http import JsonResponse, HttpResponseBadRequest
import re
import json


def analyze(request):
    body = request.body.decode()

    try:
        parsed_json = json.loads(body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('bad json')

    if 'text' not in parsed_json or type(parsed_json['text']) != str:
        return HttpResponseBadRequest('"text" field missing or of wrong type')

    def count_matches(r, s):
        return sum(1 for _ in re.finditer(r, s))

    text = parsed_json['text']
    number_of_char = len(text)
    white_space = number_of_char - count_matches('\\s', text)

    word_count = count_matches('[^\\s]+', text)
    counter_dict = Counter(m[0].lower() for m in re.finditer('[A-Za-z]', text))

    sorted_counter = [{key: value} for key, value in sorted(counter_dict.items())]

    response = {
        "textLength": {"withSpaces": number_of_char, "withoutSpaces": white_space},
        "wordCount": word_count,
        "characterCount": sorted_counter
    }

    return JsonResponse(response)

