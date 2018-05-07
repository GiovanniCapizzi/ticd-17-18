# coding=utf-8

from django.shortcuts import render

from .algorithms import algorithms_list


def algorithm_view(request, algorithm):
    return render(request, 'index.html', {
        'algorithm': algorithm,
        'algorithms': algorithms_list,
        'input': [
            # key, title, description, input type
            ('input', 'Input', 'Inserisci la stringa da codificare', 'string'),
            ('dimension', 'Dimensione Finestra', 'Inserisci qui la dimensione della finestra', 'bool')
        ]
    })
