
import yaml
from graphviz import Digraph

# syllabusデータの読み込み
with open('syllabus.yaml', 'r') as file:
    syllabus = yaml.safe_load(file)

# Graphvizを使ってグラフを作成
graph = Digraph(comment='Syllabus Graph')

# 週のボックスノードと講義サブボックスの作成
for i, week_data in enumerate(syllabus):
    if 'chapter' in week_data:
        week_num = week_data['chapter']
        week_topics = ', '.join(week_data['topics'])
        week_node_name = f"Chapter {week_num}\n{week_topics}"
        graph.node(week_node_name, shape='box', style='filled', fillcolor='lightblue')
        
        with graph.subgraph(name=f'cluster_chapter_{week_num}') as subgraph:
            subgraph.attr(style='dashed')
            lecture_list = '\n'.join(week_data['topics'])
            subgraph.node(f'lectures_chapter_{week_num}', shape='box', label=lecture_list)
            graph.edge(week_node_name, f'lectures_chapter_{week_num}', style='dashed', tailport='s', headport='sw')

# 隔週ごとの矢印の接続
for i in range(len(syllabus) - 1):
    current_week = syllabus[i]
    next_week = syllabus[i + 1]
    
    if 'chapter' in current_week and 'chapter' in next_week:
        current_week_num = current_week['chapter']
        next_week_num = next_week['chapter']
        current_week_node_name = f"Chapter {current_week_num}\n{', '.join(current_week['topics'])}"
        next_week_node_name = f"Chapter {next_week_num}\n{', '.join(next_week['topics'])}"
        graph.edge(current_week_node_name, next_week_node_name)

# グラフの保存と表示
graph.render('syllabus_graph', view=True)
