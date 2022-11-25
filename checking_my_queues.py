import os
import time
import requests


# https://iyuu.cn     get token
def send_msg(text='default_title', desp='default_desp', IYUU_TOKEN='xxx'):
    url = f'https://iyuu.cn/{IYUU_TOKEN}.send'
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    Form = {'text': text, 'desp': desp}
    return requests.post(url, data=Form, headers=headers)

def text_to_dict(text):
    dic = {}
    for line in text:
        dic[line[0]] = line
    return dic

def get_my_queue():
    r = os.popen('squeue --me')
    text = r.read()
    r.close()
    text = text.split('\n')
    text =text[1:-1]
    text = [[*filter(lambda s:len(s)>0,line.split(' '))] for line in text]
    # 0:JOBID, 1:PARTITION, 2:NAME, 3:USER, 4:ST, 5:TIME, 6:NODES, 7:NODELIST(REASON)
    return text_to_dict(text)


def main():
    last_state = get_my_queue()
    while True:
        time.sleep(2)
        new_state = get_my_queue()
        if new_state.keys()!=last_state.keys():
            # new_jobs = new_state.keys()-last_state.keys()
            done_jobs = last_state.keys() - new_state.keys()
            for done_job in done_jobs:
                title = f'{last_state[done_job][2]} DONE'
                msg = f'DONE: {last_state[done_job][2]}, {last_state[done_job][5]}, {last_state[done_job][7]}, {last_state[done_job][1]}'
                print(title,msg)
                send_msg(title,msg)
        last_state=new_state


if __name__ == '__main__':
    while(True):
        try:
            main()
        except KeyboardInterrupt:
            break
        except:
            continue