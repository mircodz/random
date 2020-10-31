#! /usr/bin/env python3

# If it ain't broke, don't fix it.
# This code has been botched together in an hour, it's ugly, but it works.

def min_distance(dist, queue):
    minimum = float("Inf")
    min_index = -1

    for i in range(len(dist)):
        if dist[i] < minimum and i in queue:
            minimum = dist[i]
            min_index = i
    return min_index

def get_path(parent, j):
    if parent[j] == -1 :
        return [j]
    return [j, *get_path(parent, parent[j])]

def print_paths(dist, parent):
    grid = []
    for i in range(0, len(dist)):
        path = get_path(parent, i)
        grid.append(('-'.join([chr(i + repr_offset) for i in path]), len(path) - 1, dist[i]))

    m0 = max(*map(lambda x: len(str(x[0])), grid), 5)
    m1 = max(*map(lambda x: len(str(x[1])), grid), 5)
    m2 = max(*map(lambda x: len(str(x[2])), grid), 8)

    hline = '+{}+{}+{}+' \
        .format('-' * (m0 + 2),
                '-' * (m1 + 2),
                '-' * (m2 + 2))

    print (hline)
    print('| {{:<{}}} | {{:<{}}} | {{:<{}}} |'
            .format(m0, m1, m2)
            .format('path', 'hops', 'distance'))
    print (hline)
    for i in grid:
        print('| {{:>{}}} | {{:>{}}} | {{:>{}}} |'
            .format(m0, m1, m2)
            .format(*i))
    print (hline)

def dijkstra(graph, src):
    size = len(graph)

    parent = [-1] * size
    visited = [False] * size

    dist = [float("Inf")] * size
    dist[src] = 0

    queue = [i for i in range(size)]

    print('* Step-by-Step Dijkstra\n')
    while queue:
        u = min_distance(dist,queue)
        queue.remove(u)
        for i in range(size):
            if graph[u][i] and i in queue:
                if dist[u] + graph[u][i] < dist[i]:
                    dist[i] = dist[u] + graph[u][i]
                    parent[i] = u
                    visited[u] = True

        m3 = max(len(str(chr(i + repr_offset))), 4)
        m0 = max(*map(lambda x: len(str(x)), dist), 4)
        m1 = max(*map(lambda x: len(str(x)), parent), 6)
        m2 = max(*map(lambda x: len(str(x)), visited), 7)

        hline = '+{}+{}+{}+{}+' \
            .format('-' * (m3 + 2),
                    '-' * (m1),
                    '-' * (m1 + 2),
                    '-' * (m2 + 2))

        print(hline)
        print('| {{:<{}}} | {{:<{}}} | {{:<{}}} | {{:<{}}} |'
                .format(m3, m0, m1, m2)
                .format('node', 'cost', 'parent', 'visited'))
        print(hline)
        c = 0
        for i, j, k in zip(dist, parent, visited):
            print('| {{:>{}}} | {{:>{}}} | {{:>{}}} | {{:>{}}} |'
                    .format(m3, m0, m1, m2)
                    .format(chr(c + repr_offset), i, chr(j + repr_offset) if j != -1 else '/', 'T' if k else 'F'))
            c += 1
        print(hline)
        print()

    print('\n* Routing Table\n')
    print_paths(dist,parent)
    print('\n\nThis file has _not_ been generated by dzjstra, I swear.')

nodes = []

repr_offset = 0

while s := input():
    try:
        i = s.strip().split(' ')[0]
        j = s.strip().split(' ')[1]
        k = s.strip().split(' ')[2]

        try:
            int(i)
            if repr_offset != 0 and repr_offset != 48:
                print('FLAG{try_not_to_break_anything_thanks}')
                exit(1)
            repr_offset = 48
        except:
            if repr_offset != 0 and repr_offset != 65:
                print('FLAG{try_not_to_break_anything_thanks}')
                exit(1)
            repr_offset = 65

        nodes.append((ord(i) - repr_offset, ord(j) - repr_offset, int(k)))
    except:
        print('invalid output, retry')
    if repr_offset == 65 and len(nodes) == 26:
        print('node limit reached')
        break

n = max(max(src, dst) for src, dst, _ in nodes)
graph = [[0] * (n + 1) for i in range(n + 1)]

for src, dst, w in nodes:
    graph[src][dst] = w
    graph[dst][src] = w

# 30 second after having written this I've already forgotten how it works
print('* Adjacency Matrix\n')
w = max(max([len(str(r)) for r in size]) for size in graph)
hline = '+{}+'.format('+'.join(['-' * (w + 2)] * (n + 2)))
print(hline)
print('|{}|'
    .format('|'.join([' {{:>{}}} '.format(w)] * (n + 2)))
    .format('', *(map(lambda x: chr(x + repr_offset), range(n + 1)))))
for i, size in enumerate(graph):
    print(hline)
    print('|{}|'
        .format('|'.join([' {{:>{}}} '.format(w)] * (n + 2)))
        .format(chr(i + repr_offset), *size))
print(hline + '\n\n')

src = ord(input()) - repr_offset

print('* Link State Packet\n')

m0 = max(len(str(n)), 3)
m1 = max(len(str(n)), 3)
m2 = max(*map(lambda x: len(str(x)), graph[src]), 8)

hline = '+{}+{}+{}+' \
    .format('-' * (m0 + 2),
            '-' * (m1 + 2),
            '-' * (m2 + 2))

print(hline)
print('| {{:<{}}} | {{:<{}}} | {{:<{}}} |'
        .format(m0, m1, m2)
        .format('src', 'dst', 'distance'))
print(hline)
for i, row in enumerate(graph):
    if row[src] != 0:
        print('| {{:>{}}} | {{:>{}}} | {{:>{}}} |'
                .format(m0, m1, m2)
                .format(chr(src + repr_offset), chr(i + repr_offset), row[src]))
print(hline)
print('\n')

try:
    dijkstra(graph, src)
except Exception as _:
    print('FLAG{try_not_to_break_anything_thanks}')