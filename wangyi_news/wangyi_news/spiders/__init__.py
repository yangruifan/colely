# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import json
from itertools import chain
import re
from bs4 import Tag, NavigableString, Comment


def clean(content: Tag) -> None:
    """
    去掉对人类无意义的行内文本标签，没有任何可见内容的标签以及除了src之外的所有节点属性
    包括style标签以及任何未知的属性
    :param content: 将清洗的html文本
    :return: 纯粹文本
    """

    def is_empty(tag: Tag):
        if not isinstance(tag, Tag) or tag.name == 'img':
            return False

        has_img = tag.find('img')
        is_blank = (not has_img) and (re.fullmatch('^\\s*$', tag.get_text()))

        return True if is_blank else False

    # 删除所有注释
    for nav_str in content.find_all(text=lambda x: isinstance(x, Comment)):
        nav_str.extract()

    # 将所有span和a标签的内容移出，插入标签之前，并且删除这些标签
    inline_nodes = ["span", "a"]
    black_nodes = chain.from_iterable([content.find_all(i) for i in inline_nodes])

    for node in black_nodes:
        for child in node.children:
            node.insert_before(child)
        node.extract()

    # 删除所有无用属性
    for node in chain([content, ], content.descendants):
        keys = [] if isinstance(node, NavigableString) or node.attrs is None else node.attrs
        keys_del = [i for i in keys if i not in {"src"}]
        for key in keys_del:
            del node[key]

    # 删除不可见/难以处理的
    invisible_list = ['script', 'frame', 'iframe', 'video', 'style']
    invisible_nodes = chain.from_iterable([content.find_all(i) for i in invisible_list])
    for i in invisible_nodes:
        i.decompose()

    # 删除所有空节点
    blank_nodes = [node for node in content.descendants if is_empty(node)]
    for node in blank_nodes:
        node.decompose()

    # 删除所有空文字节点
    for nav_str in content.find_all(text=lambda x: isinstance(x, NavigableString)):
        if re.fullmatch('^\\s*$', str(nav_str)):
            nav_str.extract()

    for i in reversed(content.find_all('img')):
        if 'src' not in i.attrs.keys():
            i.decompose()

def clean_date(content: str) -> str:
    """
    去掉所有何和日期有关的词
    :param content:清洗的内容
    :return:清洗之后的内容
    """
    return re.sub('[\d+{2}]\d*[年|月|日]', '', content)