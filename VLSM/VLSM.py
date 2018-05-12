# coding=utf-8
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import os

VLSM = ({'slash': '/25', 'mask': 128, 'hosts': 126, 'block': 128},
        {'slash': '/26', 'mask': 192, 'hosts': 62, 'block': 64},
        {'slash': '/27', 'mask': 224, 'hosts': 30, 'block': 32},
        {'slash': '/28', 'mask': 240, 'hosts': 14, 'block': 16},
        {'slash': '/29', 'mask': 248, 'hosts': 6, 'block': 8},
        {'slash': '/30', 'mask': 252, 'hosts': 2, 'block': 4})


def compute():
    source = raw_input("输入要划分的IP：")
    source_s = ''
    for c in source.rpartition(".")[:-1]:
        source_s += c

    a_sum = int(raw_input("输入划分段数："))
    if a_sum > 64:
        raw_input("大于最大子网数 退出")
        return

    alist = {}
    for i in range(a_sum):
        alist.update({i: int(raw_input("第" + str(i + 1) + "段主机数:"))})

    sum = 0
    for i in alist.values():
        for example in VLSM[::-1]:
            if (i) <= example['hosts']:
                sum += example['block']
                break
    if sum > 256:
        raw_input("大于最大主机数 退出")
        return

    alist_order = alist.items()
    alist_order.sort(key=lambda x: x[1], reverse=True)

    subnet_type = []
    for i in alist_order:
        for example in VLSM[::-1]:
            if i[1] <= example['hosts']:
                subnet_type.append(VLSM.index(example))
                break

    subnet_list = [{}] * len(subnet_type)
    number = 0
    for index in range(len(subnet_type)):
        i = subnet_type[index]
        start = number
        end = start + VLSM[i]['block'] - 1
        subnet_list[alist_order[index][0]] = {'start': start, 'end': end, 'mask': i}
        number = end + 1

    outimg_a(source_s, alist, subnet_list)
    outimg_b(source_s, subnet_list)


def compute_web(source, alist):
    os.chdir(os.path.split(os.path.realpath(__file__))[0])

    # source=raw_input("输入要划分的IP：")
    source_s = ''
    for c in source.rpartition(".")[:-1]:
        source_s += c

    # a_sum=int(raw_input("输入划分段数："))
    # if a_sum>64:
    #     raw_input("大于最大子网数 退出")
    #     return

    # alist={}
    # for i in range(a_sum):
    #     alist.update({i:int(raw_input("第"+str(i+1)+"段主机数:"))})

    sum = 0
    for i in alist.values():
        for example in VLSM[::-1]:
            if (i) <= example['hosts']:
                sum += example['block']
                break
    if sum > 256:
        raw_input("大于最大主机数 退出")
        return False

    alist_order = alist.items()
    alist_order.sort(key=lambda x: x[1], reverse=True)

    subnet_type = []
    for i in alist_order:
        for example in VLSM[::-1]:
            if i[1] <= example['hosts']:
                subnet_type.append(VLSM.index(example))
                break

    subnet_list = [{}] * len(subnet_type)
    number = 0
    for index in range(len(subnet_type)):
        i = subnet_type[index]
        start = number
        end = start + VLSM[i]['block'] - 1
        subnet_list[alist_order[index][0]] = {'start': start, 'end': end, 'mask': i}
        number = end + 1

    outimg_a(source_s, alist, subnet_list)
    outimg_b(source_s, subnet_list)
    return True


def outimg_a(source, alist, subnet):
    h = len(alist) * 30 + 40 + 3
    im = Image.new('RGB', (600, h), 0xffffff)
    draw = ImageDraw.Draw(im)
    width, height = im.size
    # 画行横线，每行30像素，第一行多10像素。
    for i in range(1, len(alist) + 2):
        y = i * 30 + 10;
        draw.line(((10, y), (width - 10, y)), fill=(225, 225, 225))

    # 边线
    draw.line(((10, 1), (10, height - 2)), fill=(225, 225, 225))
    draw.line(((width - 10, 1), (width - 10, height - 2)), fill=(225, 225, 225))

    # 标题

    # 标题背景
    draw.rectangle(((10, 1), (width - 10, 40)), fill=(223, 223, 223));
    # 标题文字，使用雅黑粗
    font = ImageFont.truetype("msyhbd.ttc", 14)
    fontcolor = (14, 77, 157)

    draw.text((20, 10), "No", fill=fontcolor, font=font)
    draw.line(((50, 1), (50, height - 3)), fill=(0, 0, 0))
    draw.text((56, 10), "need hosts", fill=fontcolor, font=font)
    draw.line(((137, 1), (137, height - 3)), fill=(0, 0, 0))
    draw.text((150, 10), "subnet pool", fill=fontcolor, font=font)
    draw.line(((460, 1), (460, height - 3)), fill=(0, 0, 0))
    draw.text((465, 10), "mask", fill=fontcolor, font=font)

    font = ImageFont.truetype("msyh.ttc", 12)
    fontcolor = (50, 100, 100)

    for i in range(len(subnet)):
        h = (i + 1) * 30 + 15
        draw.text((20, h), str(i + 1), fill=fontcolor, font=font)
        draw.text((56, h), str(alist[i]), fill=fontcolor, font=font)
        draw.text((150, h), source + str(subnet[i]['start']) + VLSM[subnet[i]['mask']]['slash'], fill=fontcolor,
                  font=font)
        draw.text((270, h), "----", fill=fontcolor, font=font)
        draw.text((305, h), source + str(subnet[i]['end']) + VLSM[subnet[i]['mask']]['slash'], fill=fontcolor,
                  font=font)
        draw.text((465, h), "255.255.255." + str(VLSM[subnet[i]['mask']]['mask']), fill=fontcolor, font=font)

    im.save('a.jpg')


def outimg_b(source, subnet):
    im = Image.new('RGB', (300, 1320), 0xffffff)
    draw = ImageDraw.Draw(im)

    font_l = ImageFont.truetype("msyh.ttc", 12)
    font_h = ImageFont.truetype("msyhbd.ttc", 12)
    fontcolor = (50, 100, 100)

    for i in range(0, 256 + 1, 4):
        h = (i / 4) * 20 + 12
        if i % 16 == 0:
            draw.text((10, h), str(i).rjust(3), fill=fontcolor, font=font_h)
            draw.line(((37, h + 8), (50, h + 8)), fill=(0, 0, 0), width=4)
        else:
            draw.text((10, h), str(i).rjust(3), fill=fontcolor, font=font_l)
            draw.line(((37, h + 8), (50, h + 8)), fill=(0, 0, 0), width=2)
    draw.line(((43, 20), (43, 1300)), fill=(0, 0, 0), width=2)

    for i in subnet:
        sline_h = i['start'] / 4 * 20 + 12 + 8
        eline_h = (i['end'] + 1) / 4 * 20 + 12 + 8
        text_h = (sline_h + eline_h) / 2 - 8

        draw.line(((60, sline_h), (290, sline_h)), fill=(0, 0, 0), width=2)
        draw.line(((60, eline_h), (290, eline_h)), fill=(0, 0, 0), width=2)
        draw.text((95, text_h),
                  "No." + str(subnet.index(i) + 1) + " - " + source + str(i['start']) + VLSM[i['mask']]['slash'],
                  fill=fontcolor, font=font_l)

    im.save('b.jpg')


if __name__ == '__main__':
    compute()
