# -*- coding: utf-8 -*-
from django import template

register = template.Library()
@register.filter(name='format_price')
def format_price(some_string):
    some_string = "%d" % some_string
    if len(some_string) > 3:
        new_string = ""
        length = len(some_string)
        k = 3 - length%3
        some_string = (" "*k + some_string)
        for i in xrange(0,(length + k)/3):
            new_string += (" "+some_string[i*3:(i+1)*3])
        return new_string[k+1:]
    return some_string
    # str = '%d' % value
    # if (len(str)%3 == 0): k = (len(str)/3-1)*3
    # else: k = len(str)%3
    # if (k or (len(str)/3)-1):
    #     num = str[:k]
    #     for i in range(1,len(str)/3+1):
    #         num = num + ' ' + str[(k)*i:(k+1)*(i+1)]
    #         k = k+1
    # else:
    #     num = str
    # return num


# @register.filter
# def price_format(some_string):
#     some_string = "%s" % some_string
#     if len(some_string) > 3:
#         new_string = ""
#         length = len(some_string)
#         k = 3 - length%3
#         some_string = (" "*k + some_string)
#         for i in xrange(0,(length + k)/3):
#             new_string += (" "+some_string[i*3:(i+1)*3])
#         return new_string[k+1:]
#     return some_string