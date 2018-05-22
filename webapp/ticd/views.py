# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .algorithms import algs, modules
from django.shortcuts import render
from dotmap import DotMap
from typing import List
import json
import time
import traceback


@login_required
def get_algorithms(request):
    return JsonResponse(algs, safe=False)


def extract_info(fun):
    return [(name, str(clazz), False if clazz.__name__ == 'bool' else '') for name, clazz in
            fun.__annotations__.items() if name not in ['logging', 'return']]


def starts_with(text: str, items: List[str]):
    for item in items:
        if text.startswith(item):
            return True
    return False


def get_algorithm(algorithm):
    alg = modules[algorithm]
    functions = [getattr(alg, x) for x in dir(alg) if
                 starts_with(x, ['encode', 'decode', 'search', 'verify', 'compare', 'calculate'])]
    return {fun.__name__: extract_info(fun) for fun in functions}


@login_required
def post_algorithm(request, algorithm):
    alg = modules[algorithm]
    try:
        body = DotMap(json.loads(request.body))
        start_time = time.time()
        result = getattr(alg, body.function)(*body.args)
        duration = time.time() - start_time
        return {'result': result, 'time': duration}
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return HttpResponse(status=400)


@login_required
def get_index(request):
    return render(request, 'index.html', context={})


@login_required
@csrf_exempt
def algorithm_execute(request, algorithm=None):
    if request.method == 'GET':
        return JsonResponse(get_algorithm(algorithm))
    if request.method == 'POST':
        res = post_algorithm(request, algorithm)
        if type(res) is dict:
            return JsonResponse(res)
        else:
            return res
