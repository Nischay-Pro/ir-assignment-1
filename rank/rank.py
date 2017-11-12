import pprint, math, sys
import json
import pymysql.cursors

t = .85 #teleportation factor

def calculatePagerank(allpages, inlinks, outlinks, count):

    #find all pages with no outlinks
    nooutlinks = []
    for page in allpages:
        #if outlinks[page] == 0:
        if page not in outlinks:
            nooutlinks.append(page)

    #initial pagerank is evenly split
    pagerank = {}
    for key in allpages:
        pagerank[key] = 1.0/count

    prevPerplexity = 0
    currentPerplexity = perplex(pagerank)


    #main loop
    while not hasconverged(prevPerplexity, currentPerplexity):
        #pprint.pprint(currentPerplexity)

        ####pagerank

        newpagerank = {}
        sinkPR = 0

        for page in nooutlinks:
            sinkPR += pagerank[page]

        for key in list(pagerank.keys()):

            newpagerank[key] = (1 - t) / count
            newpagerank[key] += t * sinkPR / count
            for inlink in inlinks[key]:
                if(inlink.isdigit()):
                    newpagerank[key] += t * (pagerank[int(inlink)] / len(outlinks[int(inlink)]))
        ###

        pagerank = newpagerank
        prevPerplexity = currentPerplexity
        currentPerplexity = perplex(pagerank)

    return pagerank

def hasconverged(prevPerplexity, currentPerplexity):
    r1 = round(prevPerplexity, 4)
    r2 = round(currentPerplexity, 4)
    return r1 == r2

def perplex(pagerank):
    return pow(2, shannonEntropy(pagerank))

def shannonEntropy(pagerank):
    s = 0
    for key in pagerank:
        p = pagerank[key]
        s += p * math.log(p, 2)
    return -1 * s

def readFile():
    count = 0 #total num pages in collection
    inlinks = {} #dict of pages to a list of all inlinks
    outlinks = {} #dict of pages to count of outlinks
    allpages = [] #list of all pages seen
    f = open(sys.argv[1], 'r')
    content = f.readlines()

    for line in content:
        line = line.strip() #remove newlines
        links = line.split(" ")

        node = links[0]

        links.remove(node)

        inlinks[node] = links
        allpages.append(node)

        for link in links:
            if link in outlinks:
                outlinks[link] += 1
            else:
                outlinks[link] = 1

        count += 1

    return allpages, inlinks, outlinks, count


def getTopXbyPagerank(x, pageranks):
    s = [(k, pageranks[k]) for k in sorted(pageranks, key=pageranks.get, reverse=True)]
    for k, v in s[:x]:
        print(k, v)
def sumPagerank(pagerank):
    s = 0
    for key in list(pagerank.keys()):
        s += pagerank[key]
    return s

def main():
    with open('./../config.json', 'r') as f:
        ARR = json.load(f)
    HOST = (ARR)['db-host']
    USER = (ARR)['db-username']
    PASSWORD = (ARR)['db-password']
    DBNAME = (ARR)['db-name']
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DBNAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT LAST_INSERT_ID(uid) From ir_articles ORDER BY uid DESC LIMIT 1"
        cursor.execute(sql, )
        result = cursor.fetchone()
        if result != None:
            uid = result['LAST_INSERT_ID(uid)']
        else:
            uid = 1
    with connection.cursor() as cursor:
        sql = "SELECT uid,inlinks,backlinks From ir_articles"
        cursor.execute(sql, )
        result = cursor.fetchall()
    uidslist = []
    for querydata in result:
        uidslist.append(querydata['uid'])
    inlinks = {}
    outlinks = {}
    for item in uidslist:
        with connection.cursor() as cursor:
            sql = "SELECT inlinks,backlinks From ir_articles WHERE uid=" + str(item)
            cursor.execute(sql, )
            result = cursor.fetchall()
            inlinksstring = str(result[0]['inlinks'])
            inlinkstemp = []
            for data in inlinksstring.split(" "):
                inlinkstemp.append(data)
            backlinksstring = str(result[0]['backlinks'])
            backlinkstemp = []
            for data in backlinksstring.split(" "):
                backlinkstemp.append(data)
            inlinks[item] = inlinkstemp
            outlinks[item] = backlinkstemp
    pagerank = calculatePagerank(uidslist, inlinks, outlinks, uid)
    with connection.cursor() as cursor:
        for uid in range(1,len(pagerank)+1,1):
            sql = "UPDATE ir_articles SET `pagerank`=" + str(pagerank[uid]) + "WHERE uid=" + str(uid)
            cursor.execute(sql, )
    connection.commit()
    print("Top 10")
    getTopXbyPagerank(10, pagerank)
    
if __name__ == "__main__":
    main()
