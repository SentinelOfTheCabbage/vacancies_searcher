# Importing main libraries
import os
from time import sleep
from requests import get
from re import sub
from json import loads as load_string
from json import dump

url_pattern = 'https://my.sbertalents.ru/job-requisition/v3?' \
              'postingCategoory=777&region=1466&keywords=Python' \
              '&page={}&size={}'
size = 0
all_jobs = set()

def get_beautified_html(head):
    r'This function converting HTML to ASCII for terminal output. For example:'
    r'<p \args\>, <span \args\> -> \n'
    r'<li \args\> -> dash list'
    r'<strong \args\> -> select words with "<" and ">" brackets pairs'

    result = head
    result = sub('&mdash;','➖', result)
    result = sub('&ndash;','-', result)
    result = sub('&bull;','🔸', result)
    result = sub('&quot;','"', result)
    result = sub('&nbsp;',' ', result)
    result = sub('&laquo;','"', result)
    result = sub('&raquo;','"', result)
    result = sub('&middot;','>', result)
    result = sub('&hellip;','...', result)

    result = sub('<p[ \&#a-zA-Z:;=\'"\"\-0-9,.]*>','',result)
    result = sub('</p>','\n',result)

    result = sub('<br />','\n',result)

    result = sub('[ ]{1,}',' ', result)
    result = sub('<[/]{0,1}h[0-9]>','', result)

    result = sub('(<span[ \&#a-zA-Z:;=\'\"\-0-9,.]*>){1,}','\n',result)
    result = sub('(</span>){1,}','',result)

    result = sub('<ul[ \&#a-zA-Z:;=\'"\"\-0-9,.]*>','\n',result)
    result = sub('</ul>','\n',result)

    result = sub('<li[ \&#a-zA-Z:;=\'"\"\-0-9,.]*>','-',result)
    result = sub('</li>','\n',result)

    result = sub('<strong[ \&#a-zA-Z:;=\'"\"\-0-9,.]*>','<',result)
    result = sub('</strong>','>',result)

    result = sub('<em[ \&#a-zA-Z:;=\'"\"\-0-9,.]*>','',result)
    result = sub('</em>','',result)

    result = sub('<ol[ \&#a-zA-Z:;=\'"\"\-0-9,.]*>','',result)
    result = sub('</ol>','',result)

    result = sub('<div[ \&#a-zA-Z:;=\'"\"\-0-9,.]*>','',result)
    result = sub('</div>','',result)

    result = sub('<font[ \&#a-zA-Z:;=\'"\"\-0-9,.]*>','',result)
    result = sub('</font>','',result)

#    result = result.replace('<span>', '\n')
    result = sub('-[\n ]{1,}','-',result)
#    result = sub('<[\n ]{1,}','<',result)
    result = sub('[\n]{1,}','\n',result)
    result = sub('[\n ]*<[ \n]*','\n\n<', result)
    result = sub('[\n ]*>[ \n]*','>\n', result)
    return result
 #   return head

def get_current_vacancies():
    current_vacancies = list()
    query = get(url_pattern.format('1','100'))
    status = query.status_code
    if status == 200:
        pages_count = load_string(query.text)['totalPages']
        print(f'Try to load {pages_count} pages')
        for i in range(1, pages_count + 1):
            query = get(url_pattern.format(str(i), str(100)))
            content = load_string(query.text)['content']
            current_vacancies += content

    return current_vacancies

def main():
    with open('lovely_vacancies.json','r') as file:
        lovely_vacancies = load_string(file.read())
    current_vacancies = get_current_vacancies()
    with open('id_list.json', 'r') as file:
        checked_vacancies = load_string(file.read())

    current_vacancies = [job for job in current_vacancies
                         if job['id'] not in checked_vacancies]

    for pos, job in enumerate(current_vacancies):
        os.system('clear')
        print(f'{pos+1}/{len(current_vacancies)}')
        if 'header' in job['content']:
            print(
                job['content']['header'],
                f"\t! {job['content']['title']} !\n",
                get_beautified_html(job['content']['header']),
                f"\n==VACANCY ID = {job['id']}==",
                end='\n-----------------\n',
            )
            print(
                'ENTER to skip',
                'L to like it',
                'Q to quit prog',
                'P to show previous',
                sep='\n'
            )
            user_answer = input('[ Your Answer? ]:')
            if user_answer.lower() == 'q':
                break
            if user_answer.lower() == 'l':
                lovely_vacancies.append(job['id'])
            checked_vacancies.append(job['id'])

    with open('id_list.json', 'w') as file:
        dump(checked_vacancies, file)

    with open('lovely_vacancies.json', 'w') as file:
        dump(lovely_vacancies, file)

main()
