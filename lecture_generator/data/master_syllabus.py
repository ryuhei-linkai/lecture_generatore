from graphviz import Digraph
import yaml

# syllabus.yamlを読み込む
with open("syllabus.yaml", "r", encoding="utf-8") as f:
    syllabus = yaml.safe_load(f)
    print(syllabus)

def generate_overview():
    dot = Digraph(comment='Course Overview')
    dot.attr(rankdir='LR', size='8,5')

    for week in syllabus:
        with dot.subgraph(name=f'cluster_week{week["week"]}') as c:
            c.attr(label=f'Week {week["week"]}')
            for topic in week["topics"]:
                c.node(topic)
            for lecture in week["lectures"]:
                c.node(lecture["title"])

    dot.render('images/course_overview', view=True)