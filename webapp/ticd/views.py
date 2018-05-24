# coding=utf-8
import json
import time
import traceback
from itertools import chain
from typing import List

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotmap import DotMap

from .algorithms import algs, modules


@login_required
def get_algorithms(request):
    return JsonResponse(algs, safe=False)


def extract_info(fun):
    samples = fun.input_example if hasattr(fun, 'input_example') else {}

    def sample(key):
        return samples[key] if key in samples else None

    return [(name, str(clazz), False if clazz.__name__ == 'bool' else '', sample(name)) for name, clazz in
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
def get_authors(request):
    mods = list(chain(*algs.values()))
    authors = set([x[2] for x in mods])
    groups = {author: [] for author in authors}
    for alg, _, author in mods:
        groups[author].append(alg)
    return JsonResponse(
            sorted(groups.items(), key=lambda x: x[0].split(' ')[-1].upper() if x[0] != 'GROUP' else 'Z'),
            safe=False)


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
