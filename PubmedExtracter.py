# ====================================================================================================

import os
import requests
import re
import html

# ====================================================================================================

my_path = os.path.dirname(os.path.realpath(__file__))

# ====================================================================================================

def raw_list_maker(input_url, input_page):
    tmp_url = re.sub(r'(.*?)\&.*', '\\1', input_url)
    tmp_url = tmp_url + '&page=%d&format=pubmed&sort=date&size=200'%input_page
    response = requests.get(tmp_url)
    if response.status_code != 200:
        return []
    response = html.unescape(response.text)
    tmp_list = re.findall(r'PMID- .*?(?=PMID- |</pre>)', response, re.DOTALL)
    return tmp_list

def txt_slicer(input_tg, input_txt):
    tmp_txt_lst = input_txt
    tmp_txt_lst = re.findall(r'(?<=%-4s- ).*?(?=\r\n[A-Z][A-Z][ A-Z][ A-Z]- |\r\n$)' %input_tg, tmp_txt_lst, re.DOTALL)
    if tmp_txt_lst == []:
        return []
    if input_tg not in tg_mult_set:
        tmp_txt_str = str(tmp_txt_lst[0])
        tmp_txt_str = re.sub(r'\r|\n', '', tmp_txt_str)
        tmp_txt_str = re.sub(r'\s+', ' ', tmp_txt_str)
        return tmp_txt_str
    tmp_txt_lst.sort()
    for i in range(0, len(tmp_txt_lst)):
        tmp_txt_lst[i] = re.sub(r'\*|\r|\n','', tmp_txt_lst[i])
        tmp_txt_lst[i] = re.sub(r'\s+', ' ', tmp_txt_lst[i])
    return tmp_txt_lst

def dict_maker(input_list):
    tmp_paper = []
    for i in range(0, len(input_list)):
        tmp_dict = {}
        for tag in tg_tot_set:
            tmp_dict[tag] = txt_slicer(tag, input_list[i])
            print('Progress: %3d/200 Total: %d/%d\r'%(i+1, page_num, pages_num), end = '')
        tmp_paper.append(tmp_dict)
        
    return tmp_paper

# ====================================================================================================

tg_tot_set = ("PMID", "JT", "TI", "AB", "SO", "MH", "OT")
tg_mult_set = ("MH", "OT")

# ====================================================================================================

url = input("url 입력: ")
if url == "0":
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=%28%28%28%22immunity%22%5BMeSH+Terms%5D%29+OR+%28immunology%5BMeSH+Terms%5D%29%29+OR+%28immune+system%5BMeSH+Terms%5D%29%29+OR+%28immune+system+disease%5BMeSH+Terms%5D%29"
pages_num = int(input("탐색할 페이지 수: "))

# ====================================================================================================

f = open(my_path+"/Papers.txt", 'a+')

# ====================================================================================================
alp = 0

for page_num in range(1, pages_num + 1):
    paper_list = []
    raw_list = []
    raw_list = raw_list_maker(url, page_num)
    if raw_list == []:
        print("None")
        break
    paper_list.extend(dict_maker(raw_list))
    for paper in paper_list:
        f.write("No. %d"%(paper_list.index(paper) + 1 + alp) + "\n")
        try:
            f.write("ID: " + paper["PMID"] + "\n")
        except:
            f.write("ID: " + "None\n")
        try:
            f.write("TI: " + paper["TI"] + "\n")
        except:
            f.write("TI: " + "None\n")
        try:
            f.write("AB: " + paper["AB"] + "\n")
        except:
            f.write("AB: " + "None\n")
        try:
            for MH in paper["MH"]:
                f.write("MH: " + MH + "\n")
        except:
            f.write("MH: " + "None\n")
        try:
            for OT in paper["OT"]:
                f.write("OT: " + OT + "\n")
        except:
            f.write("OT: " + "None\n")
        try:
            f.write("SO: " + paper["SO"] + "\n")
        except:
            f.write("SO: " + "None\n")
        f.write("\n")
    alp = alp + 200

# ====================================================================================================

f.close()
