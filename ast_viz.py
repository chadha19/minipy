"""AST visualization using Graphviz."""

from typing import Optional
from ast_nodes import ASTNode, Program, Assign, Print, If, While, BinOp, Number, Var


def ast_to_dot(node: ASTNode, output_file: str) -> None:
    """Convert AST to Graphviz DOT format."""
    lines = ["digraph AST {", "  node [shape=box];"]
    node_counter = [0]
    node_ids = {}
    
    def get_node_id(node: ASTNode) -> str:
        """Get unique ID for a node."""
        if id(node) not in node_ids:
            node_ids[id(node)] = f"node{node_counter[0]}"
            node_counter[0] += 1
        return node_ids[id(node)]
    
    def add_node(node: ASTNode, parent_id: Optional[str] = None) -> None:
        """Recursively add nodes and edges."""
        node_id = get_node_id(node)
        
        if isinstance(node, Program):
            label = "Program"
            lines.append(f'  {node_id} [label="{label}\\n{len(node.statements)} statements"];')
            for stmt in node.statements:
                add_node(stmt, node_id)
        
        elif isinstance(node, Assign):
            label = f"Assign\\n{node.name}"
            lines.append(f'  {node_id} [label="{label}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            add_node(node.expr, node_id)
        
        elif isinstance(node, Print):
            label = "Print"
            lines.append(f'  {node_id} [label="{label}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            add_node(node.expr, node_id)
        
        elif isinstance(node, If):
            label = "If"
            lines.append(f'  {node_id} [label="{label}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            add_node(node.cond, node_id)
            cond_id = get_node_id(node.cond)
            lines.append(f'  {node_id} -> {cond_id} [label="cond"];')
            for stmt in node.then_body:
                add_node(stmt, node_id)
            if node.else_body:
                for stmt in node.else_body:
                    add_node(stmt, node_id)
        
        elif isinstance(node, While):
            label = "While"
            lines.append(f'  {node_id} [label="{label}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            add_node(node.cond, node_id)
            cond_id = get_node_id(node.cond)
            lines.append(f'  {node_id} -> {cond_id} [label="cond"];')
            for stmt in node.body:
                add_node(stmt, node_id)
        
        elif isinstance(node, BinOp):
            label = f"BinOp\\n{node.op}"
            lines.append(f'  {node_id} [label="{label}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            add_node(node.left, node_id)
            add_node(node.right, node_id)
            left_id = get_node_id(node.left)
            right_id = get_node_id(node.right)
            lines.append(f'  {node_id} -> {left_id} [label="left"];')
            lines.append(f'  {node_id} -> {right_id} [label="right"];')
        
        elif isinstance(node, Number):
            label = f"Number\\n{node.value}"
            lines.append(f'  {node_id} [label="{label}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
        
        elif isinstance(node, Var):
            label = f"Var\\n{node.name}"
            lines.append(f'  {node_id} [label="{label}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
    
    add_node(node)
    lines.append("}")
    
    with open(output_file, 'w') as f:
        f.write("\n".join(lines))

