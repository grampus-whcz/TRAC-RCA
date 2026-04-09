# from rca.baseline.rag_tool_multicandidate_agent.controller import control_loop
from rca.baseline.rag_tool_multicandidate_agent.controller_rag import control_loop
# from rca.baseline.rag_tool_multicandidate_agent.controller_graph import control_loop

class RCA_Agent:
    def __init__(self, agent_prompt, basic_prompt) -> None:

        self.ap = agent_prompt
        self.bp = basic_prompt

    def run(self, dataset, instruction, logger, max_step=25, max_turn=5, rag_k=5):
            
        logger.info(f"Objective: {instruction}")
        prediction, trajectory = control_loop(dataset, instruction, "", self.ap, self.bp, logger=logger, max_step=max_step, max_turn=max_turn, rag_k=rag_k)
        logger.info(f"Result: {prediction}")

        return prediction, trajectory