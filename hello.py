from flask import Flask, request,render_template
import networkx as nx
import json as json
import random as random
import matplotlib.pyplot as plt




app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to ICD 11 Web App"


@app.route('/ask')
def ask():
   return render_template('ask.html')


@app.route("/result",methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        global G
        info = {}
        source = result["source"]
        target = result["target"]
        path = nx.shortest_path(G, source, target)

        SG = nx.Graph()
        for node in path:
            nbd = [n for n in G.neighbors(node)]
            SG.add_node(node)
            for item in nbd:
                SG.add_node(item)
            for item in nbd:
                SG.add_edge(node,item)

        info.update({"path":path,\
                "source":source,\
                "target":target,\
                "path_length": len(path),\
                "info":nx.info(SG),\
                "nodes":SG.nodes()})


        return render_template("result.html", info = info)

#=================== Supportive Functions  ====================================

@app.route("/path")
def path():
    global G
    info = {}
    source = '1307379503'
    target = '1369242951'

    path = nx.shortest_path(G, source, target)

    info.update({"source":source,\
                "target":target,\
                "path":path,\
                "path_length":len(path)})

    return render_template("path.html", info = info)


@app.route("/subgraph")
def subgraph():
    SG = nx.Graph()
    info = {}
    n1 = '1307379503'
    n2 = '1369242951'
    path = nx.shortest_path(G,source=n1,target=n2)
    for node in path:
        nbd = [n for n in G.neighbors(node)]
        SG.add_node(node)
    for item in nbd:
        SG.add_node(item)
    for item in nbd:
        SG.add_edge(node,item)

    info.update({"path":path,\
                "source":n1,\
                "target":n2,\
                "path_length": len(path),\
                "info":nx.info(SG),\
                "nodes":SG.nodes()})


    return render_template("subgraph.html", info = info)


      
    
if __name__ == '__main__':
   
    global G
    G = nx.Graph()

    with open('DATA.json', 'r') as f:
        DATA = json.load(f)

    with open('ROOTS.json', 'r')as f:
        ROOTS = json.load(f)

    for item in DATA:
        item_id = item['id']
        G.add_node(item_id)
        childs = item['childs']
        if childs!= 'Key Not found':
            for c_id in childs:
                G.add_edge(item_id,c_id)
            
            
    G.add_node("ICD11",\
           title="International Disease CLassification")

    for root in ROOTS:
        G.add_edge("ICD11",root)


    app.run(port = 3000, debug = True)



