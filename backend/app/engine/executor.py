from app.engine.graph import create_simple_graph

class WorkflowExecutor:
    """工作流执行器"""
    
    def __init__(self):
        self.graph = create_simple_graph()
    
    async def execute(self, workflow_id: int, input_data: dict):
        """执行工作流"""
        initial_state = {
            "input": str(input_data),
            "output": "",
            "steps": [],
            "current_step": 0,
            "error": None
        }
        
        result = await self.graph.ainvoke(initial_state)
        return result