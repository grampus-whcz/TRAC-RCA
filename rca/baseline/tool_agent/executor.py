import re
import time
from datetime import datetime
from rca.api_router import get_chat_completion
import os


def execute_act(instruction: str, background: str, history, attempt, kernel, logger, objective) -> str:
    from camel.agents.tool_agents.local_script_tool_agent import LocalScriptToolAgent
    
    # --- ADD THIS TEMPLATE ---
    conclusion_template = """{LLM_answer_for_tool_result}
The original execution output of the tool is also provided below for reference:
{tool_execution_output}
"""

    logger.info("Start execution via tool agent")
    t1 = datetime.now()

    # Initialize tool agent (assume scripts are in current working dir or known path)
    SCRIPT_DIR = "/root/shared-nvme/work/timeSeries/OmniTransfer_new"  # <-- 配置你的脚本目录
    tool_agent = LocalScriptToolAgent(name="RCAAnalyzer", script_dir=SCRIPT_DIR)

    # Build prompt to ask LLM to output structured tool call
    tool_system_prompt = f"""You are a DevOps assistant. Your task is to analyze the given problem and decide which RCA pipeline to run.

For Bank dataset, available pipelines:
- Bank_metric_container: for container-level metrics
- Bank_metric_app: for application-level metrics
- Bank_trace: for distributed tracing data
- Bank_log: for log anomaly detection
- all: all the available pipelines including Bank_metric_container, Bank_metric_app, Bank_trace, and Bank_log will be executed orderly

You MUST respond ONLY with a JSON object containing the following keys:
{{
  "pipeline_type": "...",
  "date_offline": "YYYY_MM_DD",
  "date_online": "YYYY_MM_DD",
  "start_ts": ...,
  "end_ts": ...,
  "method": "TranAD",
  "output_folder_name": "...",
  "output_suffix": "..."
}}

Note that:
- the value of pipeline_type can be a single pipeline ('Bank_metric_container', 'Bank_metric_app', 'Bank_trace', and 'Bank_log') or 'all'
- date_offline is 2021_03_05 for Bank dataset
- date_online should be determined by issue description date
- start_ts and end_ts should be determined by issue description time scope, e.g., if the description is "the specified time range of March 8, 2021, from 19:00 to 19:30", then start_ts is 1615201200 (2021/03/08 19:00:00 UTC+8), start_ts is 1615203000 (2021/03/08 19:30:00 UTC+8).
- method is TranAD
- output_folder_name is determined by current date, e.g., if today is 2025-11-17, then the output_folder_name is 1117
- output_suffix is determined by start_ts and end_ts, e.g., start_ts is 1615201200 (2021/03/08 19:00:00 UTC+8), end_ts is 1615203000 (2021/03/08 19:30:00 UTC+8), then output_suffix is 1900_1930.
- Do NOT invent values.

Recall the issue is: {objective}

Please first confirm the issue description time scope, e.g., if the description is "the specified time range of March 8, 2021, from 19:00 to 19:30", then time scope is from 1615201200 (2021/03/08 19:00:00 UTC+8) to 1615203000 (2021/03/08 19:30:00 UTC+8).

"""

    messages = [
        {'role': 'system', 'content': tool_system_prompt},
        {'role': 'user', 'content': instruction}
    ]

    try:
        # Get structured tool call from LLM
        response = get_chat_completion(messages=messages)
        logger.info(f"LLM Tool Call Response:\n{response}")

        import json
        params = json.loads(response.strip())
        
        required = ["pipeline_type", "date_offline", "date_online", "start_ts", "end_ts"]
        if not all(k in params for k in required):
            raise ValueError("Missing required parameters in LLM response")

        # Execute tool
        tool_execution_result = tool_agent.step(**params)
        logger.info(f"Tool Execution Result:\n{tool_execution_result}")

        # Parse report file paths from tool output
        report_paths = []
        pattern = r"Report saved to:\s*(.+\.txt)"
        matches = re.findall(pattern, tool_execution_result)
        for path in matches:
            path = path.strip()
            if os.path.exists(path):
                report_paths.append(path)
            else:
                logger.warning(f"Report file not found: {path}")

        # Read report contents
        report_contents = {}
        for path in report_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                report_contents[os.path.basename(path)] = content
            except Exception as e:
                logger.error(f"Failed to read report {path}: {e}")
                report_contents[os.path.basename(path)] = f"[Error reading file: {e}]"

        # Build detailed context for LLM
        detailed_context = "Tool execution completed successfully. Below are the contents of the generated anomaly reports:\n\n"
        for filename, content in report_contents.items():
            detailed_context += f"--- {filename} ---\n{content}\n\n"
        detailed_context += f"--- Original Tool Output ---\n{tool_execution_result}"

        # Summarize with LLM using full report contents
        summary_prompt = [
            {'role': 'system', 'content': 'You are a helpful assistant skilled in root cause analysis (RCA).'},
            {'role': 'user', 'content': f"Based on the following RCA tool execution results and detailed anomaly reports, provide a concise plain-English summary of the key findings, anomalies, or potential root causes:\n\n{detailed_context}"}
        ]
        LLM_answer_for_tool_result = get_chat_completion(messages=summary_prompt)
        logger.info(f"Final Answer:\n{LLM_answer_for_tool_result}")

        # Fix the format call: use correct placeholder names
        final_result = conclusion_template.format(
            LLM_answer_for_tool_result=LLM_answer_for_tool_result,
            tool_execution_output=tool_execution_result
        )

        return response, final_result, True, history + [{'role': 'assistant', 'content': final_result}]

    except Exception as e:
        error_msg = f"Tool execution failed: {str(e)}"
        logger.error(error_msg)
        return str(e), error_msg, False, history + [{'role': 'assistant', 'content': error_msg}]