import logging
from datetime import timedelta, datetime

from tqdm import tqdm
import networkx as nx
from github import Github
import matplotlib.pyplot as plt

from rimo_storage import cache


g = None


@cache.disk_cache(path='_dc_follower', serialize='pickle')
def follower(人):
    return set([i.login for i in g.get_user(人).get_followers()])


@cache.disk_cache(path='_dc_星表', serialize='pickle')
def 星表(人):
    li = []
    for r in tqdm(g.get_user(人).get_repos()):
        try:
            for x in r.get_stargazers_with_dates():
                li.append(x)
        except Exception as e:
            logging.warning(f'仓库{r}读取失败了，因为{repr(e)}')
    return sorted(li, key=lambda x: x.starred_at)


def ember(token, 我, days=365, save_path='1.png'):
    global g
    g = Github(token)
    琴 = {}
    黄泉 = []

    for i in tqdm(星表(我)):
        if i.starred_at < datetime.now() - timedelta(days=days):
            continue
        if i.user.login == 我:
            continue
        琴.setdefault(i.user.login, {'直接': 0, '间接': []})['直接'] += 1
        黄泉 = [j for j in 黄泉 if i.starred_at-timedelta(days=3) < j.starred_at]
        v = set()
        for j in 黄泉:
            if i.user.login in follower(j.user.login) and j.user.login not in v:
                v.add(j.user.login)
                琴[j.user.login]['间接'].append(i.user.login)
        黄泉.append(i)

    G = nx.Graph()
    for k, v in sorted(琴.items(), key=lambda x: len(x[1]['间接']))[-25:]:
        print(k, '直接:', v['直接'], '间接:', len(v['间接']))
        G.add_edge(k, 我)
        for i in v['间接']:
            G.add_edge(i, k)

    d = dict(G.degree)
    plt.figure(1, figsize=(23, 23)) 
    nx.draw_kamada_kawai(G, nodelist=d.keys(), node_size=[v * 75 for v in d.values()], with_labels=True)
    plt.savefig(save_path)
