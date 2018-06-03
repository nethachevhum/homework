import gensim
import json
import os
import networkx as nx
import matplotlib.pyplot as plt


# программа обучалась на модели rusvectores: ruscorpora_upos_skipgram_300_5_2018.vec.gz ; этот файл должен быть в папке с программой, если нужно заново вычислять косинусную близость
#семантическое поле -- звуки животных

def get_data(words): #массив с косинусными расстояниями записывается в файл, и оттуда считывается. Если файла нет -- расстояния считаются заново
    if os.path.isfile("graph.txt"):
        with open("graph.txt","r", encoding="utf-8") as f:
            q = json.loads(f.read())
            return q
    m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
    model = gensim.models.KeyedVectors.load_word2vec_format(m,binary=False)
    model.init_sims(replace=True)
    graph = []
    for index, word in enumerate(words):
        if not index+1 == len(words):
            for word2 in words[index+1:]:
                graph.append((word,word2,model.similarity(word,word2)))
    with open("graph.txt","w+",encoding="utf-8") as f:
        f.write(json.dumps(graph, ensure_ascii=False))
    return graph

def make_graph(words):
    data = get_data(words)
    grph = nx.Graph()
    grph.add_nodes_from(words)
    grph.add_weighted_edges_from([(el[0],el[1],round(el[2],2)) for el in data if el[2] > 0.5])
    vis = nx.spring_layout(grph)
    nx.draw_networkx_nodes(grph, vis, node_color='red', node_size=50)
    nx.draw_networkx_edges(grph,vis,edge_color="blue")
    nx.draw_networkx_labels(grph,vis,font_size=15,font_family='Arial')
    nx.draw_networkx_edge_labels(grph,vis,font_size=7,font_family='Arial')
    plt.axis('off')
    plt.show()
    dg = nx.degree_centrality(grph)
    return [node for node in sorted(dg, key=dg.get, reverse=True)], nx.radius(grph), nx.average_clustering(grph) # центральные слова -- радиус -- кластеризация


def main():
    handle = make_graph(["лаять_VERB", "гавкать_VERB", "крякать_VERB", "рычать_VERB", "мяукать_VERB", "мурлыкать_VERB", "пищать_VERB","шипеть_VERB"])
    print("Три самых центральных слова: {} \nРадиус графа: {} \nКластеризация графа:{}".format(", ".join(handle[0][:3]),str(handle[1]),str(round(handle[2],2))))


if __name__ == "__main__":
    main()


    # print(model["день_NOUN"][:10])

# get_data("лаять_VERB","гавкать_VERB","крякать_VERB","рычать_VERB","мяукать_VERB","мурлыкать_VERB","пищать_VERB","шипеть_VERB")
# print("wr")