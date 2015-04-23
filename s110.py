__author__ = 'sail'
db_filename = r'resource/link.db'
schema_filename = r'link.sql'
import sqlite3


def read_data():
    import os
    import pickle
    from multiprocessing import Pool

    conn = sqlite3.connect(db_filename)
    print('Creating schema')
    with open(schema_filename, 'rt') as f:
        schema = f.read()
    conn.executescript(schema)
    if not os.path.exists(r"resource/temp"):
        os.makedirs(r"resource/temp")

    pool = Pool(processes=os.cpu_count())
    results = pool.map(__read_excle, [(r'resource/linkdata/' + i, i) for i in os.listdir(r'resource/linkdata/')])
    pool.close()
    pool.join()
    pages = set()
    for i in results:
        pages.update(i)
    conn.executemany(r'INSERT INTO url(host,page,url) VALUES (?,?,?)',
                     (i.split(r'//')[1][:-1].split(r'/', 1) + [i] for i in pages))
    conn.commit()
    result = conn.execute(r'SELECT id,url FROM url')
    page_map = {}
    for i in result:
        page_map[i[1]] = i[0]

    for parent, dirnames, filenames in os.walk(r'resource/temp'):
        for i in filenames:
            with open(parent + r'/' + i, 'rb') as f:
                page_link = pickle.load(f)
            os.remove(parent + r'/' + i)
            conn.executemany(r'INSERT INTO link(source,target) VALUES (?,?)',
                             [(page_map[source], page_map[target]) for source in page_link for target in
                              page_link[source]])
    conn.commit()
    conn.close()


def __read_excle(file):
    import xlrd
    import pickle

    pages = set()
    page_link = {}
    table = xlrd.open_workbook(file[0]).sheets()[0]
    for j in range(table.nrows):
        row = table.row_values(j)
        url = row[1]
        pages.add(url)
        page_link[url] = [i[1:-1] for i in row[2][1:-1].split(', ')]
        for j in page_link[url]:
            pages.add(j)
    with open(r'resource/temp/' + file[1] + '.dat', 'wb') as f:
        pickle.dump(page_link, f)
    return pages


def link_out(host, page):
    conn = sqlite3.connect(db_filename)
    result = conn.execute('SELECT url.url FROM link LEFT '
                          'JOIN url ON url.id=link.target WHERE source IN '
                          '(SELECT id FROM url WHERE host=? AND page=?)', (host, page))
    return [i[0] for i in result]


def link_in(host, page):
    conn = sqlite3.connect(db_filename)
    result = conn.execute('SELECT url.url FROM link LEFT '
                          'JOIN url ON url.id=link.source WHERE target IN '
                          '(SELECT id FROM url WHERE host=? AND page=?)', (host, page))
    return [i[0] for i in result]


def link_out_count(host):
    conn = sqlite3.connect(db_filename)
    result = conn.execute('SELECT url.host,count(*) FROM link LEFT '
                          'JOIN url ON url.id=link.target WHERE source IN '
                          '(SELECT id FROM url WHERE host=?) GROUP BY url.host', (host,))
    return list(result)


def link_in_count(host):
    conn = sqlite3.connect(db_filename)
    result = conn.execute('SELECT url.host,count(*) FROM link LEFT '
                          'JOIN url ON url.id=link.source WHERE target IN '
                          '(SELECT id FROM url WHERE host=?) GROUP BY url.host', (host,))
    return list(result)