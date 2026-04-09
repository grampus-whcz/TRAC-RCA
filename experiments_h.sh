#！/bin/bash

## c means cluster size 3, no RAG

## ====================================================================

## GLM 4.5
# nohup bash experiments_h.sh >> Bank_no_RAG_c3_log_template_new_context_back_llm_glm-4.5.log 2>&1 &

# nohup bash experiments_h.sh >> Bank_no_RAG_c3_knowledge_graph_advanced_merged_0-135_glm-4.5.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 0  --end_idx 135

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_knowledge_graph_advanced_merged_0-50_glm-4.5.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 0  --end_idx 50

# nohup bash experiments_h.sh >> Market_cloudbed-1_no_RAG_c3_knowledge_graph_advanced_merged_0-70_glm-4.5.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1  --start_idx 0  --end_idx 70

# nohup bash experiments_h.sh >> Market_cloudbed-2_no_RAG_c3_knowledge_graph_advanced_merged_0-77_glm-4.5.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1  --start_idx 0  --end_idx 77

## ====================================================================

## GLM 4.6
# nohup bash experiments_h.sh >> Bank_no_RAG_c3_knowledge_graph_advanced_merged_0-135_glm-4.6.log 2>&1 &
python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 44  --end_idx 135

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_log_template_new_context_back_llm_glm-4.6.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 0  --end_idx 50

# nohup bash experiments_h.sh >> Market_cloudbed-1_no_RAG_c3_log_template_new_context_back_llm_glm-4.6.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1  --start_idx 0  --end_idx 70

# nohup bash experiments_h.sh >> Market_cloudbed-2_no_RAG_c3_log_template_new_context_back_llm_glm-4.6.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1  --start_idx 0  --end_idx 77

## ====================================================================

## GLM 4.7
# nohup bash experiments_h.sh >> Bank_no_RAG_c3_log_template_new_context_back_llm_tune7_new_test_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 0  --end_idx 135
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 4  --end_idx 4
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 16  --end_idx 16
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 33  --end_idx 33
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 38  --end_idx 38
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 48  --end_idx 48

# nohup bash experiments_h.sh >> Bank_no_RAG_c3_knowledge_graph_advanced_merged_0-135_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 0  --end_idx 135

# nohup bash experiments_h.sh >> Bank_no_RAG_c3_knowledge_graph_programmatic_4-16_33_38_48_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 4  --end_idx 4
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 16  --end_idx 16
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 33  --end_idx 33
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 38  --end_idx 38
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 48  --end_idx 48

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_log_template_new_context_back_tune5_4_llm_0-50_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 0  --end_idx 50

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_knowledge_graph_program_0-0_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 0  --end_idx 0
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 45  --end_idx 50

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_knowledge_graph_advanced_merged_0-50_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 38  --end_idx 50
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 45  --end_idx 50

# nohup bash experiments_h.sh >> Market_cloudbed-1_no_RAG_c3_knowledge_graph_programmatic_0_70_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1  --start_idx 1  --end_idx 2

# nohup bash experiments_h.sh >> Market_cloudbed-1_no_RAG_c3_knowledge_graph_advanced_merged_0_70_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1  --start_idx 0  --end_idx 70

# nohup bash experiments_h.sh >> Market_cloudbed-2_no_RAG_c3_knowledge_graph_llm_0_77_glm-4.7.log 2>&1 &

# nohup bash experiments_h.sh >> Market_cloudbed-2_no_RAG_c3_knowledge_graph_advanced_merged_0_77_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1  --start_idx 0  --end_idx 77

## ====================================================================

## gpt-4o
# nohup bash experiments_h.sh >> Bank_no_RAG_c3_log_template_new_context_back_llm_gpt-4o.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 0  --end_idx 135

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_log_template_new_context_back_llm_gpt-4o.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 0  --end_idx 51

# nohup bash experiments_h.sh >> Market_cloudbed-1_no_RAG_c3_log_template_new_context_back_llm_gpt-4o.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1  --start_idx 0  --end_idx 70

# nohup bash experiments_h.sh >> Market_cloudbed-2_no_RAG_c3_log_template_new_context_back_llm_gpt-4o.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1  --start_idx 0  --end_idx 78

## ====================================================================

## qwen3-235b-a22b-instruct-2507
# nohup bash experiments_h.sh >> Bank_no_RAG_c3_log_template_new_context_back_llm_qwen3-235b-a22b-instruct-2507.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 0  --end_idx 135

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_log_template_new_context_back_llm_qwen3-235b-a22b-instruct-2507.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 0  --end_idx 51

# nohup bash experiments_h.sh >> Market_cloudbed-1_no_RAG_c3_log_template_new_context_back_llm_qwen3-235b-a22b-instruct-2507.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1  --start_idx 0  --end_idx 70

# nohup bash experiments_h.sh >> Market_cloudbed-2_no_RAG_c3_log_template_new_context_back_llm_qwen3-235b-a22b-instruct-2507.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1  --start_idx 0  --end_idx 78

## ====================================================================

## deepseek-r1-250528
# nohup bash experiments_h.sh >> Bank_no_RAG_c3_log_template_new_context_back_llm_deepseek-r1-250528.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 0  --end_idx 135

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_log_template_new_context_back_llm_deepseek-r1-250528.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 0  --end_idx 51

# nohup bash experiments_h.sh >> Market_cloudbed-1_no_RAG_c3_log_template_new_context_back_llm_deepseek-r1-250528.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1  --start_idx 0  --end_idx 70

# nohup bash experiments_h.sh >> Market_cloudbed-2_no_RAG_c3_log_template_new_context_back_llm_deepseek-r1-250528.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1  --start_idx 0  --end_idx 78

## ====================================================================

## gemini-2.5-pro-preview-p
# nohup bash experiments_h.sh >> Bank_no_RAG_c3_log_template_new_context_back_llm_gemini-2.5-pro-preview-p.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1  --start_idx 0  --end_idx 135

# nohup bash experiments_h.sh >> Telecom_no_RAG_c3_log_template_new_context_back_llm_gemini-2.5-pro-preview-p.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1  --start_idx 0  --end_idx 51

# nohup bash experiments_h.sh >> Market_cloudbed-1_no_RAG_c3_log_template_new_context_back_llm_gemini-2.5-pro-preview-p.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1  --start_idx 0  --end_idx 70

# nohup bash experiments_h.sh >> Market_cloudbed-2_no_RAG_c3_log_template_new_context_back_llm_gemini-2.5-pro-preview-p.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1  --start_idx 0  --end_idx 78
