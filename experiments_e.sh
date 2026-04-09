#！/bin/bash

## ====================================================================

## GLM 4.7
# nohup bash experiments_e.sh >> Bank_all_RAG_k3_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 135

# nohup bash experiments_e.sh >> Telecom_all_RAG_k3_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 50

# nohup bash experiments_e.sh >> Market_cloudbed-1_all_RAG_k3_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 69

# nohup bash experiments_e.sh >> Market_cloudbed-2_all_RAG_k3_glm-4.7.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 77

## ====================================================================

## gpt-4o
# nohup bash experiments_e.sh >> Bank_all_RAG_k3_gpt-4o.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 136

# nohup bash experiments_e.sh >> Telecom_all_RAG_k3_gpt-4o.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 51

# nohup bash experiments_e.sh >> Market_cloudbed-1_all_RAG_k3_gpt-4o.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 70

# nohup bash experiments_e.sh >> Market_cloudbed-2_all_RAG_k3_gpt-4o.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 78

## ====================================================================

## qwen3-235b-a22b-instruct-2507
# nohup bash experiments_e.sh >> Bank_all_RAG_k3_qwen3-235b-a22b-instruct-2507.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1 --rag_k 3 --start_idx 58  --end_idx 136

# nohup bash experiments_e.sh >> Telecom_all_RAG_k3_qwen3-235b-a22b-instruct-2507.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 51

# nohup bash experiments_e.sh >> Market_cloudbed-1_all_RAG_k3_qwen3-235b-a22b-instruct-2507.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1 --rag_k 3 --start_idx 21  --end_idx 70

# nohup bash experiments_e.sh >> Market_cloudbed-2_all_RAG_k3_qwen3-235b-a22b-instruct-2507.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 78

## ====================================================================

## deepseek-r1-250528
# nohup bash experiments_e.sh >> Bank_all_RAG_k3_deepseek-r1-250528.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1 --rag_k 3 --start_idx 93  --end_idx 136

# nohup bash experiments_e.sh >> Telecom_all_RAG_k3_deepseek-r1-250528.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 51

# nohup bash experiments_e.sh >> Market_cloudbed-1_all_RAG_k3_deepseek-r1-250528.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 70

# nohup bash experiments_e.sh >> Market_cloudbed-2_all_RAG_k3_deepseek-r1-250528.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 78

## ====================================================================

## gemini-2.5-pro-preview-p
# nohup bash experiments_e.sh >> Bank_all_RAG_k3_gemini-2.5-pro-preview-p.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Bank --controller_max_step 1 --rag_k 3 --start_idx 3  --end_idx 3

# nohup bash experiments_e.sh >> Telecom_all_RAG_k3_gemini-2.5-pro-preview-p.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Telecom --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 51

# nohup bash experiments_e.sh >> Market_cloudbed-1_all_RAG_k3_gemini-2.5-pro-preview-p.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-1 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 70

# nohup bash experiments_e.sh >> Market_cloudbed-2_all_RAG_k3_gemini-2.5-pro-preview-p.log 2>&1 &
# python -m rca.run_agent_standard_multi_candidate --dataset Market/cloudbed-2 --controller_max_step 1 --rag_k 3 --start_idx 0  --end_idx 78
