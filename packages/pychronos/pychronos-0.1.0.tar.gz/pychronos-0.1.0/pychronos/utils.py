#
# def pretty_print(data, keys=None, sep=' '):
#     """ """
#     if not keys:
#         keys = list(data[0].keys() if data else [])
#     out = [keys]  # 1st row = header
#
#     for item in data:
#         out.append([str(item[col] or '') for col in keys])
#
#     col_size = [max(map(len, (sep.join(col)).split(sep))) for col in zip(*out)]
#
#     format_str = ' | '.join(["{{:<{}}}".format(i) for i in col_size])
#
#     line = format_str.replace(' | ', '-+-').format(*['-' * i for i in col_size])
#     item = out.pop(0);
#     lineDone = False
#     while out:
#         if all(not i for i in item):
#             item = out.pop(0)
#             if line and (sep != '\uFFFA' or not lineDone): print(line); lineDone = True
#         row = [i.split(sep, 1) for i in item]
#         print(format_str.format(*[i[0] for i in row]))
#         item = [i[1] if len(i) > 1 else '' for i in row]


def pretty_dict(data, keys=None):
    """ """
    if not keys:
        keys = list(data[0].keys() if data else [])
    out = [keys]  # 1st row = header
    for item in data:
        out.append([str(item.get(col) if item.get(col) is not None else '') for col in keys])
    col_size = [max(map(len, col)) for col in zip(*out)]
    format_str = '  '.join(["{{:<{}}}".format(i) for i in col_size])
    out.insert(1, ['-' * i for i in col_size])
    for item in out:
        print(format_str.format(*item))
