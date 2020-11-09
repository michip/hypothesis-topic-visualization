from django import template

register = template.Library()

@register.filter
def to_percent(value):
    return int(round(value*100))

COLORS = ["#d9534f", "#f0ad4e", "#5bc0de", "#5cb85c"]

@register.filter
def to_color(value):
    return COLORS[min(len(COLORS)-1, int(round(value*100))//25)]

