"""sui.dl
Deep learning algorithm implementations
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__api_info_dict = {'nn.PNN': 'Product-based Neural Networks'}


def api_info(api=None):
    if api is not None:
        if api in __api_info_dict:
            return 'API: {}\nInfo: {}\n'.format(api, __api_info_dict[api])
        else:
            return '{} is not an appreciable API under sui.dl'.format(api)
    else:
        for api, info in __api_info_dict.items():
            return 'API: {}\nInfo: {}\n'.format(api, info)
