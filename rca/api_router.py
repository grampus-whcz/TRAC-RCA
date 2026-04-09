import os
import sys
import yaml
import time


def load_config(config_path="rca/api_config.yaml"):
    configs = dict(os.environ)
    with open(config_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    configs.update(yaml_data)
    return configs

configs = load_config()

def OpenAI_chat_completion(messages, temperature):    
    from openai import OpenAI
    client = OpenAI(
        api_key=configs["API_KEY"]
    )
        
    return client.chat.completions.create(
        model = configs["MODEL"],
        messages = messages,
        temperature = temperature,
    ).choices[0].message.content

def Google_chat_completion(messages, temperature):
    import google.generativeai as genai
    genai.configure(
        api_key=configs["API_KEY"]
    )
    genai.GenerationConfig(temperature=temperature)
    system_instruction = messages[0]["content"] if messages[0]["role"] == "system" else None
    messages = [item for item in messages if item["role"] != "system"]
    messages = [{"role": "model" if item["role"] == "assistant" else item["role"], "parts": item["content"]} for item in messages]
    history = messages[:-1]
    message = messages[-1]
    return genai.GenerativeModel(
        model_name=configs["MODEL"],
        system_instruction=system_instruction
        ).start_chat(
            history=history if history != [] else None
            ).send_message(message).text

def Anthropic_chat_completion(messages, temperature):
    import anthropic
    client = anthropic.Anthropic(
        api_key=configs["API_KEY"]
    )
    return client.messages.create(
        model=configs["MODEL"],
        messages=messages,
        temperature=temperature,
        max_tokens=2048  # 补充Anthropic必要参数
    ).content[0].text  # 修正Anthropic返回值提取逻辑

# 新增：GLM-4.7 (Coding端点) 调用函数
def GLM_chat_completion(logger, messages, temperature):
    from zhipuai import ZhipuAI
    
    # 初始化GLM客户端（从配置文件读取密钥和端点）
    client = ZhipuAI(
        api_key=configs["API_KEY"],
        base_url=configs.get("API_BASE", "https://open.bigmodel.cn/api/coding/paas/v4")  # 默认使用Coding端点
    )
    
    try:
        # 建议的Token配置（适配128K上限）
        max_input_tokens = 120000  # 输入上限
        max_output_tokens = configs.get("MAX_TOKENS", 8192)  # 输出上限
        
        full_response = client.chat.completions.create(
            model=configs["MODEL"],
            messages=messages,
            temperature=temperature,
            max_tokens=max_output_tokens,  # 控制输出长度
            top_p=0.95,
            # 可选：设置输入Token上限（部分SDK支持）
            # max_input_tokens=max_input_tokens
        )
        
        # 提取回复内容
        response_content = full_response.choices[0].message.content
        
        # 记录token使用情况（如果有返回）
        if hasattr(full_response, 'usage') and full_response.usage:
            prompt_tokens = full_response.usage.prompt_tokens
            completion_tokens = full_response.usage.completion_tokens
            total_tokens = full_response.usage.total_tokens
            logger.info(f"=={configs['MODEL']}=====================input Tokens: {prompt_tokens}, output Tokens: {completion_tokens}, total: {total_tokens}")
        
        # 预警：接近128K上限时提示
        if (prompt_tokens + completion_tokens) > 120000:
            logger.warning("Token使用量接近128K上限，建议精简输入内容")    
        
        return response_content
    except Exception as e:
        logger.error(f"GLM调用失败: {str(e)}")
        raise e  # 抛出异常让外层重试逻辑处理

# for 3-rd party API which is compatible with OpenAI API (with different 'API_BASE')
def AI_chat_completion(logger, messages, temperature):    
    from openai import OpenAI
    
    client = OpenAI(
        api_key=configs["API_KEY"],
        base_url=configs["API_BASE"]
    )
    
    full_response = client.chat.completions.create(
        model = configs["MODEL"],
        messages = messages,
        temperature = temperature,
    )
    
    response_content = full_response.choices[0].message.content
    
    model = configs["MODEL"]
    prompt_tokens = full_response.usage.prompt_tokens
    completion_tokens = full_response.usage.completion_tokens
    total_tokens = full_response.usage.total_tokens
    logger.info(f"=={model}=====================input Tokens: {prompt_tokens}, output Tokens: {completion_tokens}, total: {total_tokens}")
    
    return response_content

def Ollama_chat_completion(messages, temperature):
    import requests
    import json

    url = "http://127.0.0.1:11434/api/chat"
    payload = {
        "model": configs["MODEL"],
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Ollama request failed with status {response.status_code}: {response.text}")

    result = response.json()
    return result.get("message", {}).get("content", "")

def get_chat_completion(logger, messages, temperature=0.0):

    def send_request():
        if configs["SOURCE"] == "AI":
            return AI_chat_completion(logger, messages, temperature)
        elif configs["SOURCE"] == "OpenAI":
            return OpenAI_chat_completion(messages, temperature)
        elif configs["SOURCE"] == "Google":
            return Google_chat_completion(messages, temperature)
        elif configs["SOURCE"] == "Anthropic":
            return Anthropic_chat_completion(messages, temperature)
        elif configs["SOURCE"] == "Ollama":
            return Ollama_chat_completion(messages, temperature)
        elif configs["SOURCE"] == "GLM":
            return GLM_chat_completion(logger, messages, temperature)
        else:
            raise ValueError("Invalid SOURCE in api_config file.")
    
    for i in range(3):
        try:
            return send_request()
        except Exception as e:
            print(e)
            if '429' in str(e):
                print("Rate limit exceeded. Waiting for 1 second.")
                time.sleep(1)
                continue
            else:
                raise e