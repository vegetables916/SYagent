from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

class WorkflowState(TypedDict):
    """工作流状态"""
    input: str
    output: str
    steps: List[str]
    current_step: int
    error: Optional[str]

def create_simple_graph():
    """创建简单的工作流图"""
    
    def node1(state: WorkflowState):
        """节点1：处理输入"""
        return {"steps": ["step1"], "current_step": 1}
    
    def node2(state: WorkflowState):
        """节点2：LLM 调用"""
        return {"steps": ["step2"], "current_step": 2}
    
    def node3(state: WorkflowState):
        """节点3：输出结果"""
        return {"output": "完成", "steps": ["step3"], "current_step": 3}
    
    # 构建图
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("node1", node1)
    workflow.add_node("node2", node2)
    workflow.add_node("node3", node3)
    
    workflow.set_entry_point("node1")
    workflow.add_edge("node1", "node2")
    workflow.add_edge("node2", "node3")
    workflow.add_edge("node3", END)
    
    return workflow.compile()