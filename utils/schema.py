from pydantic import BaseModel
from typing import List

class Node(BaseModel):
    name: str
    type: str
    description: str
    id: int
    
class Edge(BaseModel):
    source_id: int
    target_id: int
    type: str
    description: str
    
class KnowledgeGraph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
