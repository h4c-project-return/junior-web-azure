def id(o): return o


def fill_none(iterable):
    last_item = None
    for item in iterable:
        last_item = item or last_item
        yield last_item


def strip_all(iterable):
    return map(lambda s: s.strip(), iterable)


def repeat(item, count):
    i = 0
    while i < count:
        yield item
        i = i + 1


def zip_padded(x, y, pad):
    x = list(x)
    y = list(y)
    lenX = len(x)
    lenY = len(y)
    if (lenX < lenY): x = x + list(repeat(pad, lenY - lenX))
    if (lenX > lenY): y = y + list(repeat(pad, lenX - lenY))
    return zip(x, y)


def distinct(iterable):
    visited = set()
    for item in iterable:
        if not item in visited:
            visited.add(item)
            yield item


def skip(count, iterable):
    visited = 0
    for item in iterable:
        visited = visited + 1
        if visited > count: yield item


def key_val_dict_list(iterable):
    return map(lambda (k, v): { "key" : k, "value" : v }, iterable)

