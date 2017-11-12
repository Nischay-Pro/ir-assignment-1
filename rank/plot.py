import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json
import pymysql.cursors

def main():
    with open('./../config.json', 'r') as f:
        ARR = json.load(f)
    HOST = (ARR)['db-host']
    USER = (ARR)['db-username']
    PASSWORD = (ARR)['db-password']
    DBNAME = (ARR)['db-name']
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DBNAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT uid,inlinks,backlinks From ir_articles"
        cursor.execute(sql, )
        result = cursor.fetchall()
    uidslist = []
    for querydata in result:
        uidslist.append(querydata['uid'])
    inlinks = []
    outlinks = []
    pagerank = []
    for item in uidslist:
        with connection.cursor() as cursor:
            sql = "SELECT inlinks,backlinks,pagerank From ir_articles WHERE uid=" + str(item)
            cursor.execute(sql, )
            result = cursor.fetchall()
            inlinksstring = str(result[0]['inlinks'])
            for data in inlinksstring.split(" "):
                if(len(data)>0):
                    inlinkstemp = []
                    inlinkstemp.append(str(item))
                    inlinkstemp.append(data)
                    inlinks.append(inlinkstemp)
    with connection.cursor() as cursor:
        sql = "SELECT pagerank From ir_articles"
        cursor.execute(sql, )
        result2 = cursor.fetchall()
    for item in result2:
        pagerank.append(item['pagerank'])
    pagerank2 = {}
    for i in range(1,len(pagerank)+1,1):
        pagerank2[str(i)] = float(pagerank[i-1])
    G = nx.DiGraph()
    G.add_edges_from(inlinks)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = [v * 10000 for v in pagerank2.values()])
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='r', arrows=True)
    nx.set_node_attributes(G, pagerank2,'weight')
    nx.set_node_attributes(G, pagerank2,'betweenness')
    plt.show()

if __name__ == "__main__":
    main()