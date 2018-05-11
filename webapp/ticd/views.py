# coding=utf-8

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .algorithms import algs, modules
from dotmap import DotMap
from typing import List
import json


def get_algorithms(request):
    return JsonResponse(algs, safe=False)


def extract_info(fun):
    return [(name, clazz.__name__.lower(), False if clazz.__name__ == 'bool' else '') for name, clazz in
            fun.__annotations__.items() if name is not 'return']


def starts_with(text: str, items: List[str]):
    for item in items:
        if text.startswith(item):
            return True
    return False


def get_algorithm(algorithm):
    alg = modules[algorithm]
    functions = [getattr(alg, x) for x in dir(alg) if starts_with(x, ['encode', 'decode', 'search'])]
    return {fun.__name__: extract_info(fun) for fun in functions}


def post_algorithm(request, algorithm):
    alg = modules[algorithm]
    try:
        body = DotMap(json.loads(request.body))
        return {'result': getattr(alg, body.function)(*body.args)}
    except Exception:
        return HttpResponse(status=400)


@csrf_exempt
def algorithm_execute(request, algorithm=None):
    if request.method == 'GET':
        return JsonResponse(get_algorithm(algorithm))
    if request.method == 'POST':
        return JsonResponse(post_algorithm(request, algorithm))
