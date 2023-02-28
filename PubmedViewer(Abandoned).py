# ====================================================================================================

import os
import sys
import time
import requests
import re
import html
import six
from google.cloud import translate_v2 as translate
from pprint import pprint as pprint

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
            print('%3d/200\r'%(i+1), end = '')
        tmp_paper.append(tmp_dict)
        
    return tmp_paper

def papers_printer(input_papers_list, input_paper_num_to_see):
    i = input_paper_num_to_see
    tmp = input_papers_list
    print("PMID: " + "https://pubmed.ncbi.nlm.nih.gov/" + str(tmp[i]["PMID"]))
    print("TI: " + str(tmp[i]["TI"]))
    print("AB: " + str(tmp[i]["AB"]))
    print("AU: " + str(tmp[i]["AU"]))
    print("JT: " + str(tmp[i]["JT"]))
    print("SO: " + str(tmp[i]["SO"]))
    print("MH: " + str(tmp[i]["MH"]))

# ====================================================================================================

paper_list = []
tg_tot_set = ("PMID", "JT", "TI", "AB", "AU", "SO", "MH", "OT")
tg_mult_set = ("MH", "AU", "OT")

# ====================================================================================================

url = input("url 입력: ")
if url == "0":
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=%28regulatory+t+lymphocyte%5BMeSH+Terms%5D%29+AND+%28%22Frontiers+in+immunology%22%5BJournal%5D%29&sort=date"
pages_num = int(input("탐색할 페이지 수: "))

# ====================================================================================================

for page_num in range(1, pages_num + 1):
    raw_list = []
    raw_list = raw_list_maker(url, page_num)
    if raw_list == []:
        print("None")
        break
    paper_list.extend(dict_maker(raw_list))
    print("        Progress: %d/%d\r"%(page_num, pages_num), end = "")

# ====================================================================================================

MH_set = set()
MH_dict = dict()

for paper in range(0, len(paper_list)):
    MH_set.update(paper_list[paper]["MH"])
    for MH in paper_list[paper]["MH"]:
        MH_dict[MH] = []
for paper in range(0, len(paper_list)):
    for MH in paper_list[paper]["MH"]:
        MH_dict[MH].append(paper + 1)



# ====================================================================================================

# print(sorted(MH_set))



# ====================================================================================================

while True:
    os.system("cls")
    select = input("논문 리스트(1)\nMH 리스트(2)\nMH 검색(3)\n입력: ")
    if select == "1":
        while(True):
            os.system("cls")
            print("논문 리스트")
            print("="*100)
            paper_num_to_see = int(input("페이지 입력(1~%d): "%len(paper_list))) - 1
            if paper_num_to_see == -1:
                break
            print("="*100)
            papers_printer(paper_list, paper_num_to_see)
            q = input("Enter 0 to go back")
            if q == "0":
                break
    elif select == "2":
        os.system("cls")
        for i in sorted(MH_set):
            print(i)
            print(MH_dict[i])
        input("Enter to go back")
    elif select == "3":
        while True:
            os.system("cls")
            MH_search = input("확인할 MH 입력: ")
            print("")
            if MH_search not in MH_set:
                print("다시 선택하세요.")
                q = input("Press Enter to continue or Enter 0 to go back")
                if q == "0":
                    break
                continue
            print(MH_dict[MH_search])
            q = input("Enter 0 to go back")
            if q == "0":
                break
    else:
        print("\n다시 선택하세요.")
        input("Press Enter to continue")

    
