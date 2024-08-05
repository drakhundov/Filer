import os

from filesystem import direct


def query(directs, queries):
    def contains_queries(file, queries):
        for query in queries:
            if not query.strip().lower().encode('utf-8') in file.read().lower():
                return False
        return True

    occurencies = set()
    cnt = 0
    for dir_ in directs:
        for content in direct.fulltree(dir_):
            with open(content, 'rb') as f:
                if contains_queries(f, queries):
                    occurencies.add(content)
                    cnt += 1

    return {
        'files': occurencies,
        'cnt': cnt
    }
