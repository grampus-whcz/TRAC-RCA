import re
import time
from datetime import datetime
from rca.api_router import get_chat_completion
import os
from camel.agents.tool_agents import BaseToolAgent

def extract_json_from_llm_response(text: str) -> str:
    text = text.strip()
    # 匹配 ```json{...}``` 或 ```{...}``` 等格式，提取大括号部分
    match = re.search(r"```(?:json)?\s*({.*})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    # 如果没有代码块包裹，直接返回（可能是纯 JSON）
    if text.startswith("{") and text.endswith("}"):
        return text
    # 否则抛出错误或让后续 json.loads 失败
    return text

def get_tool_agent_class(dataset: str):
    if dataset == "Telecom":
        from camel.agents.tool_agents.Telecom_local_script_tool_agent_5tools_fast import LocalScriptToolAgent
        SCRIPT_DIR = "/root/shared-nvme/work/timeSeries/OmniTransfer_new/Telecom_utils"
        BASE_DIR = "/root/shared-nvme/work/timeSeries/OmniTransfer_new"
        
        clustering_query = f"""# How to Generate General Root Cause Analysis (RCA) Process for Microservices with Multimodal Data
For microservice fault RCA using logs, metrics, and traces, follow this streamlined 4-step framework, leveraging the system’s dependency chain to pinpoint root causes:

Apply these RCA Decision Rules:
- **Sustained Anomaly Priority**: Prefer entities with ≥3 anomalies on the same metric within 5 minutes.
- **Earliest Among Sustained**: If multiple sustained anomalies exist, pick the one starting earliest.
- **Log as Trigger Only**: Treat log anomalies as high-confidence only if they precede sustained metric anomalies by ≤2 minutes.
- **Upstream over Downstream**: Favor components that are called by others (per trace data) and fail first.
- **Ignore Isolated Events**: Single-point anomalies without corroboration are likely symptoms.

You MUST respond ONLY with a JSON object containing the following keys:
{{
  "Cluster 1": "...",
  "Cluster 2": "...",
  ...
}}
"""
        return LocalScriptToolAgent, SCRIPT_DIR, BASE_DIR, clustering_query
    elif dataset == "Bank":
        from camel.agents.tool_agents.local_script_tool_agent_5tools_fast import LocalScriptToolAgent
        SCRIPT_DIR = "/root/shared-nvme/work/timeSeries/OmniTransfer_new/Bank_utils"
        BASE_DIR = "/root/shared-nvme/work/timeSeries/OmniTransfer_new"
        
        clustering_query = f"""# How to Generate General Root Cause Analysis (RCA) Process for Microservices with Multimodal Data
For microservice fault RCA using logs, metrics, and traces, follow this streamlined 4-step framework, leveraging the system’s dependency chain to pinpoint root causes:

# Call Chain Description (Technical Narrative)

The observed trace reveals the following end-to-end service invocation pattern:

1. An external request enters the system through the **IG** (Integration Gateway).  
2. The IG forwards the request to a **Tomcat** application server for business logic processing.  
3. During execution, Tomcat invokes a downstream **MG** (Microservice Gateway) to access core microservices.  
4. The MG, in turn, interacts with services running inside **Docker** containers—either by calling containerized workloads or delegating tasks to them.  
5. Additionally, there is a reverse interaction where **Docker-hosted components initiate calls back to the MG**, suggesting a bidirectional integration pattern (e.g., event-driven callbacks or sidecar coordination).

## Complete Core Dependency Chain (Including Invisible/Embedded Components)
**Client → apache (Load Balancing) → IG → Tomcat (⇆ Redis) → MG (⇆ Redis) ⇄ Dockerized Services (→ Mysql)**

### Component-by-Component Explanation and Breakdown
1. **Client → apache**
apache (apache01/apache02) serves as the **invisible entry point** at the foremost tier of the entire call chain. Although it is a mandatory pass-through for all external client requests, it is not captured in distributed trace data. This is because the trace collection probes are not deployed on the apache load balancers, which only undertake basic request forwarding and traffic distribution without handling business logic, thus failing to generate traceable spans.

2. **apache → IG**
The IG layer (IG01/IG02, interface gateway services) acts as the **first traceable root node** in the distributed tracing system. It receives requests forwarded by the apache load balancers and executes core gateway functions such as request authentication, protocol conversion, and service routing before relaying the requests to the downstream Tomcat business layer. All requests entering the backend microservice cluster are first recorded as trace spans at the IG tier.

3. **IG → Tomcat**
The Tomcat tier (Tomcat01, Tomcat02, Tomcat03, or Tomcat04) is the **core business logic layer** of the banking system, responsible for processing key business workflows like transaction verification and user information management. The notation `(⇆ Redis)` indicates that Tomcat services have bidirectional embedded dependencies on Redis (Redis01/Redis02). Specifically, Tomcat instances query Redis for cached data (e.g., user sessions, transaction configurations) during business processing to improve response efficiency. However, this Redis access is treated as an **internal resource call** rather than an inter-service RPC invocation, so it does not generate independent trace spans and is only reflected in the latency metrics of Tomcat’s trace spans.

4. **Tomcat → MG**
The MG tier (MG01/MG02, microservice governance middleware) provides service governance capabilities such as service registration and discovery, circuit breaking, and distributed transaction coordination for the system. Similar to the Tomcat tier, the `(⇆ Redis)` annotation here denotes that MG components invoke Redis to retrieve configuration information or distributed lock resources during request routing and permission verification. This Redis dependency is also an internal resource access and is not captured as a separate trace span in the distributed tracing system.

5. **MG ⇄ Dockerized Services**
The bidirectional arrow (`⇄`) represents the **mutual interaction** between the MG middleware and containerized business services (e.g., dockerB1): the MG tier forwards standardized business requests to containerized services, and the containerized services return processing results to the MG tier. The suffix `(→ Mysql)` indicates that containerized services ultimately call the Mysql database (Mysql01/Mysql02) for persistent data storage (e.g., transaction ledger recording, account data writing). If trace probes are not deployed on the Mysql client of containerized services, this database access will not generate independent trace spans and will only be counted as part of the latency of containerized service spans.

- IG might be IG01 or IG02
- MG might be MG01 or MG02
- apache might be apache01 or apache02
- Tomcat might be Tomcat01, Tomcat02, Tomcat03, or Tomcat04
- docker might be dockerA1, dockerA2, dockerB1, or dockerB2
- Mysql might be Mysql01 or Mysql02

Notably, the mutual dependency between **MG** and **Docker** implies that the MG not only orchestrates calls to containerized services but may also expose endpoints consumed by those same containers—common in modern cloud-native designs involving control planes, agent-based monitoring, or asynchronous task processing.

Apply these RCA Decision Rules:
- **Sustained Anomaly Priority**: Prefer entities with ≥3 anomalies on the same metric within 5 minutes.
- **Earliest Among Sustained**: If multiple sustained anomalies exist, pick the one starting earliest.
- **Log as Trigger Only**: Treat log anomalies as high-confidence only if they precede sustained metric anomalies by ≤2 minutes.
- **Upstream over Downstream**: Favor components that are called by others (per trace data) and fail first.
- **Ignore Isolated Events**: Single-point anomalies without corroboration are likely symptoms.

You MUST respond ONLY with a JSON object containing the following keys:
{{
  "Cluster 1": "...",
  "Cluster 2": "...",
  ...
}}
"""
        return LocalScriptToolAgent, SCRIPT_DIR, BASE_DIR, clustering_query
    elif dataset in ("Market/cloudbed-1", "Market/cloudbed-2"):
        from camel.agents.tool_agents.Market_local_script_tool_agent_5tools_fast_new import LocalScriptToolAgent
        SCRIPT_DIR = "/root/shared-nvme/work/timeSeries/OmniTransfer_new/Market_utils"
        BASE_DIR = "/root/shared-nvme/work/timeSeries/OmniTransfer_new"
        
        clustering_query = f"""# How to Generate General Root Cause Analysis (RCA) Process for Microservices with Multimodal Data
For microservice fault RCA using logs, metrics, and traces, follow this streamlined 4-step framework, leveraging the system’s dependency chain to pinpoint root causes:

Apply these RCA Decision Rules:
- **Sustained Anomaly Priority**: Prefer entities with ≥3 anomalies on the same metric within 5 minutes.
- **Earliest Among Sustained**: If multiple sustained anomalies exist, pick the one starting earliest.
- **Log as Trigger Only**: Treat log anomalies as high-confidence only if they precede sustained metric anomalies by ≤2 minutes.
- **Upstream over Downstream**: Favor components that are called by others (per trace data) and fail first.
- **Ignore Isolated Events**: Single-point anomalies without corroboration are likely symptoms.

You MUST respond ONLY with a JSON object containing the following keys:
{{
  "Cluster 1": "...",
  "Cluster 2": "...",
  ...
}}
"""
        return LocalScriptToolAgent, SCRIPT_DIR, BASE_DIR, clustering_query
    else:
        from camel.agents.tool_agents import BaseToolAgent
        return BaseToolAgent
    
def execute_act(dataset: str, instruction: str, history, logger) -> str:
    
    ToolAgentClass, SCRIPT_DIR, BASE_DIR, clustering_query = get_tool_agent_class(dataset)    

    # --- ADD THIS TEMPLATE ---
    conclusion_template = """{LLM_answer_for_tool_result}
The original execution output of the tool is also provided below for reference:
{tool_execution_output}
"""

    logger.info("Start execution via tool agent")
    t1 = datetime.now()

    # Initialize tool agent (assume scripts are in current working dir or known path)    
    tool_agent = ToolAgentClass(name="RCAAnalyzer", script_dir=SCRIPT_DIR, base_dir=BASE_DIR, logger=logger)    

    try:
        import json
        cleaned_response = extract_json_from_llm_response(instruction)
        params = json.loads(cleaned_response)
        
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
            if dataset == "Bank" and os.path.exists(path) and "Bank_cluster_window_anomaly_report" in path:
                report_paths.append(path)
            elif dataset == "Telecom" and os.path.exists(path) and "Telecom_cluster_window_anomaly_report" in path:
                report_paths.append(path)
            elif dataset in ("Market/cloudbed-1", "Market/cloudbed-2") and os.path.exists(path) and "Market_cluster_window_anomaly_report" in path:
                report_paths.append(path)
            elif "metric" in path or "log" in path or "trace" in path:
                logger.info(f"Sub-Report file found: {path}")
            else:
                logger.warning(f"Report file not found: {path}")

        # Read report contents
        report_contents = {}
        print(f"final report_paths: {report_paths}")
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
      
        head = "Based on the upper RCA tool execution results and detailed temporal clustering anomaly reports, please provide a concise plain-English summary (RCA analysis result) of the key findings and anomalies about related entities , their features , and the exact root cause occurrence datetime (yyyy-mm-dd HH:MM:SS CST) for every cluster:\n\n."
        # Summarize with LLM using full report contents
        summary_prompt = [
            {'role': 'system', 'content': 'You are a helpful assistant skilled in root cause analysis (RCA).'},
            {'role': 'user', 'content': head + detailed_context + clustering_query}
        ]
        logger.info(f"execute LLM Final Request:\n{summary_prompt}")
        LLM_answer_for_tool_result = get_chat_completion(logger, messages=summary_prompt)
        logger.info(f"execute LLM Final Answer:\n{LLM_answer_for_tool_result}")

        # Fix the format call: use correct placeholder names
        final_result = conclusion_template.format(
            LLM_answer_for_tool_result=LLM_answer_for_tool_result,
            tool_execution_output=tool_execution_result
        )

        return LLM_answer_for_tool_result, True, history + [{'role': 'assistant', 'content': final_result}]

    except Exception as e:
        error_msg = f"Tool execution failed: {str(e)}"
        logger.error(error_msg)
        return str(e), error_msg, False, history + [{'role': 'assistant', 'content': error_msg}]
    
    
    
if __name__ == '__main__':
    
    test_str="""{'cloudbed': 'cloudbed-1', 'pipeline_type': 'all', 'date_offline': '2022_03_21', 'date_offline_start_ts': 1647813600, 'date_offline_end_ts': 1647817200, 'date_online': '2022_03_20', 'date_online_start_ts': 1647738000, 'date_online_end_ts': 1647741600, 'start_ts': 1647738000, 'end_ts': 1647741600, 'method': 'TranAD', 'data_dir': 'data2', 'output_folder_name': '1215', 'output_suffix': '0930_1000'}"""
    text = extract_json_from_llm_response(test_str)
    
    print(text)
    import json  
    
    params = json.loads(text)
