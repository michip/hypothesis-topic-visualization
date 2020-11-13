from django import template
from colour import Color
red = Color("red")
COLORS = list(red.range_to(Color("green"),101))

register = template.Library()

@register.filter
def to_percent(value):
    return int(round(value*100))

@register.filter
def to_percent_float(value):
    return round(value*100, 3)

@register.filter
def to_color(value):
    return COLORS[int(round(value*100))]

