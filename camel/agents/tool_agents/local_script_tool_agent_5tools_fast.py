import subprocess
import os
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from camel.agents.tool_agents import BaseToolAgent


class LocalScriptToolAgent(BaseToolAgent):
    r"""A tool agent that executes predefined local Python scripts with given arguments."""

    def __init__(
        self,
        name: str,
        script_dir: str,
        base_dir: str,
        logger: Any,
        log_dir: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.name = name
        self.script_dir = script_dir
        self.base_dir = base_dir
        self.log_dir = log_dir or os.path.join(script_dir, "logs")
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up logger for this agent instance
        self.logger = logger

        self.description = (
            "This agent can execute the following RCA analysis pipelines:\n"
            "- Bank_metric_container\n"
            "- Bank_metric_app\n"
            "- Bank_trace\n"
            "- Bank_log\n"
            "- Bank_cluster_window\n"
            "Bank_metric_container, Bank_metric_app, Bank_trace, and Bank_log require parameters: date_offline, date_online, start_ts, end_ts, method, output_folder_name, output_suffix. "
            "Bank_cluster_window requires parameters: date_online, output_folder_name, output_suffix."
        )

    def step(
        self,
        pipeline_type: str,
        date_offline: str,
        date_online: str,
        start_ts: int,
        end_ts: int,
        method: str = "TranAD",
        output_folder_name: str = "1204",
        output_suffix: str = "default",
        min_samples: str = "3",
        **kwargs: Any,
    ) -> str:
        """
        Executes a specific RCA pipeline script, or all four if pipeline_type == 'all'.
        If the expected anomaly report already exists, skips execution and returns the existing report.
        """
        output_folder_name = "1204"
        valid_pipelines = {
            "Bank_metric_container": "run_pipline_Bank_metric_container.py",
            "Bank_metric_app": "run_pipline_Bank_metric_app.py",
            "Bank_trace": "run_pipline_Bank_trace.py",
            "Bank_log": "run_pipline_Bank_log.py",
            # "Bank_cluster_window": "Bank_cluster_window_analyze_anomalies_2.7.py", # ClusTopoRCA version
            "Bank_cluster_window": "2.Bank_cluster_window_analyze_anomalies_old.py", # just cluster version
        }

        self.logger.info(
            f"Received request: pipeline_type={pipeline_type}, "
            f"date_offline={date_offline}, date_online={date_online}, "
            f"start_ts={start_ts}, end_ts={end_ts}, method={method}, "
            f"output_folder_name={output_folder_name}, output_suffix={output_suffix}, min_samples={min_samples}"
        )

        if pipeline_type == "all":
            pipeline_list = list(valid_pipelines.keys())
        elif pipeline_type in valid_pipelines:
            pipeline_list = [pipeline_type]
        else:
            error_msg = f"Invalid pipeline_type '{pipeline_type}'. Valid options: {list(valid_pipelines.keys()) + ['all']}"
            self.logger.error(error_msg)
            return f"Error: {error_msg}"

        results = []
        base_output_dir = os.path.join(self.base_dir, output_folder_name)
        os.makedirs(base_output_dir, exist_ok=True)  # 确保输出目录存在

        for p_type in pipeline_list:
            script_name = valid_pipelines[p_type]
            script_path = os.path.join(self.script_dir, script_name)

            if not os.path.exists(script_path):
                err = f"Script not found for {p_type} at {script_path}"
                self.logger.error(err)
                results.append(f"Error: {err}")
                continue

            # 构建预期的报告路径（关键：用于判断是否跳过执行）
            report_path = os.path.join(base_output_dir, f"{p_type}_anomaly_report_{date_online}_{output_suffix}.txt")

            if p_type in ['Bank_metric_container', 'Bank_metric_app', 'Bank_trace', 'Bank_log', 'Bank_cluster_window']:
                report_path = os.path.join(base_output_dir, f"{p_type}_anomaly_report_{date_online}_{output_suffix}.txt")
            else:
                report_path = os.path.join(base_output_dir, f"Bank_cluster_window_anomaly_report_{date_online}_{output_suffix}_llm_rca_summary.json")

            # ✅ 新增逻辑：如果报告已存在，跳过执行
            if os.path.exists(report_path):
                self.logger.info(f"[{p_type}] Report already exists at {report_path}. Skipping execution.")
                try:
                    with open(report_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    preview = content[:1000] + "..." if len(content) > 1000 else content
                    msg = (
                        f"[{p_type}] Skipped execution (report already exists).\n"
                        f"Report saved to: {report_path}\n"
                        f"Report content preview:\n{preview}\n"
                    )
                    self.logger.info(f"[{p_type}] Report loaded successfully (length: {len(content)} chars).")
                    results.append(msg)
                except Exception as e:
                    msg = f"[{p_type}] Skipped execution but failed to read existing report: {e}"
                    self.logger.warning(msg)
                    results.append(msg)
                continue

            # 构建命令行参数
            if p_type == "Bank_cluster_window":
                cmd = [
                    "/root/shared-nvme/.conda/envs/faiss-env/bin/python", script_path,
                    "--date_online", date_online,
                    "--output_folder_name", output_folder_name,
                    "--output_suffix", output_suffix,
                    "--min_samples", min_samples,
                ]
            elif p_type == "Bank_knowledge_graph_RCA":
                cmd = [
                    "/root/shared-nvme/.conda/envs/faiss-env/bin/python", script_path,
                    "--date_online", date_online,
                    "--output_folder_name", output_folder_name,
                    "--output_suffix", output_suffix,
                ]
            else:
                cmd = [
                    "/root/shared-nvme/.conda/envs/OmniTransfer_py3.7/bin/python", script_path,
                    "--date_offline", date_offline,
                    "--date_online", date_online,
                    "--start_ts", str(start_ts),
                    "--end_ts", str(end_ts),
                    "--method", method,
                    "--output_folder_name", output_folder_name,
                    "--output_suffix", output_suffix,
                ]

            self.logger.info(f"[{p_type}] Executing command: {' '.join(cmd)}")

            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.script_dir,
                    capture_output=True,
                    text=True,
                    timeout=1800  # 30 minutes
                )

                if result.returncode == 0:
                    self.logger.info(f"[{p_type}] Execution succeeded.")
                    msg = f"[{p_type}] Execution successful.\nReport saved to: {report_path}\n"
                    if os.path.exists(report_path):
                        try:
                            with open(report_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            # preview = content[:1000] + "..." if len(content) > 1000 else content
                            preview = content
                            msg += f"Report content preview:\n{preview}\n"
                            self.logger.info(f"[{p_type}] Report loaded successfully (length: {len(content)} chars).")
                        except Exception as e:
                            msg += f"(Failed to read report: {e})\n"
                            self.logger.warning(f"[{p_type}] Failed to read report: {e}")
                    results.append(msg)
                else:
                    err_detail = (
                        f"[{p_type}] Execution failed.\n"
                        f"Stderr:\n{result.stderr}\n"
                        f"Stdout:\n{result.stdout}"
                    )
                    self.logger.error(err_detail)
                    results.append(err_detail)

            except subprocess.TimeoutExpired:
                timeout_msg = f"[{p_type}] Script execution timed out (30 minutes)."
                self.logger.error(timeout_msg)
                results.append(timeout_msg)
            except Exception as e:
                exc_msg = f"[{p_type}] Unexpected error during execution: {str(e)}"
                self.logger.exception(exc_msg)  # logs full traceback
                results.append(exc_msg)

        final_output = "\n" + "=" * 60 + "\n" + "\n".join(results) + "\n" + "=" * 60 + "\n"
        self.logger.info("All pipelines completed. Returning final output.")
        return final_output

    def chat(self, *args, **kwargs) -> str:
        return self.step(*args, **kwargs)

    def reset(self) -> None:
        pass