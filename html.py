from lxml import etree, html
html_str = open("test.html", "r").read()
root = etree.HTML(html_str)
tr_pos = 4
tds = root.xpath("//tr/td/table/tbody/tr[position()=%s]/td" % str(tr_pos))
data_start = 4
data_end = 16
for i in range(data_start, data_end):
    value = tds[i].text
    if value is None or len(value.strip()) == 0:
        if tds[i].find('font') is None:
            value = tds[i].findall('div')[1].text
        else:
            value = tds[i].find('font').text
    data_strip = value.strip()
    print(data_strip)

tr_pos = 5
tds = root.xpath("//tr/td/table/tbody/tr[position()=%s]/td" % str(tr_pos))
data_start = 1
data_end = 13
for i in range(data_start, data_end):
    value = tds[i].text
    if value is None or len(value.strip()) == 0:
        if tds[i].find('font') is None:
            value = tds[i].findall('div')[1].text
        else:
            value = tds[i].find('font').text
    data_strip = value.strip()
    print(data_strip)

tr_pos = 6
tds = root.xpath("//tr/td/table/tbody/tr[position()=%s]/td" % str(tr_pos))
data_start = 1
data_end = 13
for i in range(data_start, data_end):
    value = tds[i].text
    if value is None or len(value.strip()) == 0:
        if tds[i].find('font') is None:
            value = tds[i].findall('div')[1].text
        else:
            value = tds[i].find('font').text
    data_strip = value.strip()
    print(data_strip)

tr_pos = 7
tds = root.xpath("//tr/td/table/tbody/tr[position()=%s]/td" % str(tr_pos))
data_start = 2
data_end = 14
for i in range(data_start, data_end):
    value = tds[i].text
    if value is None or len(value.strip()) == 0:
        if tds[i].find('font') is None:
            value = tds[i].findall('div')[1].text
        else:
            value = tds[i].find('font').text
    data_strip = value.strip()
    print(data_strip)

tr_pos = 8
tds = root.xpath("//tr/td/table/tbody/tr[position()=%s]/td" % str(tr_pos))
data_start = 1
data_end = 13
for i in range(data_start, data_end):
    value = tds[i].text
    if value is None or len(value.strip()) == 0:
        if tds[i].find('font') is None:
            value = tds[i].findall('div')[1].text
        else:
            value = tds[i].find('font').text
    data_strip = value.strip()
    print(data_strip)

tr_pos = 9
tds = root.xpath("//tr/td/table/tbody/tr[position()=%s]/td" % str(tr_pos))
data_start = 1
data_end = 13
for i in range(data_start, data_end):
    value = tds[i].text
    if value is None or len(value.strip()) == 0:
        if tds[i].find('font') is None:
            value = tds[i].findall('div')[1].text
        else:
            value = tds[i].find('font').text
    data_strip = value.strip()
    print(data_strip)
