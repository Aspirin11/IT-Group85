from django import template
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary[key]
    except KeyError:
        return None


@register.filter
def chinese_month_to_english(value):
    """将中文月份转换为英文月份"""
    if value is None:
        return ""

    # 中文月份到英文月份的映射
    month_mapping = {
        '一月': 'Jan', '二月': 'Feb', '三月': 'Mar', '四月': 'Apr',
        '五月': 'May', '六月': 'Jun', '七月': 'Jul', '八月': 'Aug',
        '九月': 'Sep', '十月': 'Oct', '十一月': 'Nov', '十二月': 'Dec'
    }

    # 替换中文月份为英文月份
    result = str(value)
    for cn_month, en_month in month_mapping.items():
        result = result.replace(cn_month, en_month)

    return result
