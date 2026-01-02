from graphviz import Digraph
from models import Base
from sqlalchemy.orm import class_mapper

# function to generate .png with db schema
def generate_schema_png(output="./utils/db_schema"):
    dot = Digraph("ERD", format="png")
    dot.attr(rankdir="LR", fontsize="10")

    # ---------------------------
    # CREATE TABLE NODES
    # ---------------------------
    for cls in Base.__subclasses__():
        mapper = class_mapper(cls)
        table = mapper.local_table

        label = f"<<TABLE BORDER='1' CELLBORDER='1' CELLSPACING='0'>"
        label += f"<TR><TD BGCOLOR='lightgray'><B>{table.name}</B></TD></TR>"

        for column in table.columns:
            col_label = column.name

            if column.primary_key:
                col_label += " (PK)"
            elif column.foreign_keys:
                col_label += " (FK)"

            label += f"<TR><TD ALIGN='LEFT'>{col_label}</TD></TR>"

        label += "</TABLE>>"

        dot.node(table.name, label=label, shape="plaintext")

    # ---------------------------
    # ADD FK EDGES
    # ---------------------------
    for cls in Base.__subclasses__():
        table = class_mapper(cls).local_table

        for column in table.columns:
            for fk in column.foreign_keys:
                parent = fk.column.table.name
                child = table.name
                dot.edge(child, parent)

    # ---------------------------
    # RENDER
    # ---------------------------
    path = dot.render(output, cleanup=True)
    print(f"Generated ERD: {path}")

if __name__ == "__main__":
    generate_schema_png()
