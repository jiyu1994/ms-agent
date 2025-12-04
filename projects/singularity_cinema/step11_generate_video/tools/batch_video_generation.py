#!/usr/bin/env python3
"""
批量AI视频生成脚本
基于成功的test_video_generation.py，重新生成所有缺失的AI视频片段
"""

import json
import requests
import time
import os
import sys

# API配置
API_KEY = "apikey-dd675b2a3fcb4f1aa88b91503d87f730"
BASE_URL = "https://api.atlascloud.ai"

# 输出目录
OUTPUT_DIR = "/Users/yu/atlascloud/ms-agent/output_video"
VIDEOS_DIR = os.path.join(OUTPUT_DIR, "videos")

# 确保videos目录存在
os.makedirs(VIDEOS_DIR, exist_ok=True)

def load_segments():
    """加载segments.txt中的视频提示"""
    segments_file = os.path.join(OUTPUT_DIR, "segments.txt")
    if not os.path.exists(segments_file):
        print(f"错误：找不到 {segments_file}")
        return []
    
    with open(segments_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        segments = json.loads(content)
        return segments
    except json.JSONDecodeError as e:
        print(f"错误：解析segments.txt失败 - {e}")
        return []

def generate_single_video(prompt, segment_index, duration=4):
    """生成单个AI视频"""
    
    print(f"\n=== 开始生成视频片段 {segment_index} ===")
    print(f"提示词：{prompt[:100]}...")
    
    # Step 1: 启动视频生成
    generate_url = f"{BASE_URL}/api/v1/model/generateVideo"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "openai/sora-2/text-to-video-pro",
        "duration": duration,
        "prompt": prompt,
        "size": "720*1280"
    }
    
    print("发送生成请求...")
    try:
        generate_response = requests.post(generate_url, headers=headers, json=data, timeout=30)
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
        return None
    
    print(f"响应状态：{generate_response.status_code}")
    
    if generate_response.status_code == 429:
        print("遇到限流错误，等待60秒后重试...")
        time.sleep(60)
        return "rate_limited"
    
    if generate_response.status_code != 200:
        print(f"生成请求失败：{generate_response.status_code}")
        print(f"响应内容：{generate_response.text}")
        return None
    
    try:
        generate_result = generate_response.json()
        prediction_id = generate_result["data"]["id"]
        print(f"获得预测ID：{prediction_id}")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"解析响应失败：{e}")
        print(f"响应内容：{generate_response.text}")
        return None
    
    # Step 2: 轮询结果
    poll_url = f"{BASE_URL}/api/v1/model/prediction/{prediction_id}"
    max_polls = 180  # 最多轮询3分钟
    poll_count = 0
    
    while poll_count < max_polls:
        print(f"轮询状态... ({poll_count + 1}/{max_polls})")
        
        try:
            response = requests.get(poll_url, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"轮询请求失败：{e}")
            time.sleep(5)
            poll_count += 1
            continue
        
        if response.status_code != 200:
            print(f"轮询失败：{response.status_code}")
            print(f"响应：{response.text}")
            time.sleep(5)
            poll_count += 1
            continue
        
        try:
            result = response.json()
            status = result["data"]["status"]
            print(f"当前状态：{status}")
        except (KeyError, json.JSONDecodeError) as e:
            print(f"解析轮询响应失败：{e}")
            time.sleep(5)
            poll_count += 1
            continue
        
        if status in ["completed", "succeeded"]:
            try:
                video_url = result["data"]["outputs"][0]
                print(f"✅ 视频生成成功：{video_url}")
                return download_video(video_url, segment_index)
            except (KeyError, IndexError) as e:
                print(f"获取视频URL失败：{e}")
                return None
        
        elif status == "failed":
            error_msg = result["data"].get("error", "生成失败")
            print(f"❌ 视频生成失败：{error_msg}")
            return None
        
        else:
            # 仍在处理中，等待
            time.sleep(2)
            poll_count += 1
    
    print("轮询超时")
    return None

def download_video(video_url, segment_index):
    """下载视频文件"""
    video_filename = f"ai_video_{segment_index}.mp4"
    video_path = os.path.join(VIDEOS_DIR, video_filename)
    
    print(f"下载视频到：{video_path}")
    
    try:
        response = requests.get(video_url, timeout=60)
        response.raise_for_status()
        
        with open(video_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ 视频下载成功：{video_path}")
        return video_path
    
    except requests.exceptions.RequestException as e:
        print(f"下载失败：{e}")
        return None

def create_video_prompts():
    """根据segments内容创建适合的视频提示词"""
    segments = load_segments()
    if not segments:
        return []
    
    video_prompts = []
    
    for segment in segments:
        index = segment.get("index", 0)
        content = segment.get("content", "")
        
        # 为第12段使用已有的video字段
        if index == 12 and "video" in segment:
            prompt = segment["video"]
        else:
            # 为其他段落生成适合的视频提示词
            prompt = generate_video_prompt_from_content(content, index)
        
        video_prompts.append({
            "index": index,
            "prompt": prompt,
            "content": content[:50] + "..."
        })
    
    return video_prompts

def generate_video_prompt_from_content(content, index):
    """根据文本内容生成英文视频提示词"""
    prompts = {
        1: "A modern smartphone on a desk with glowing AI icons floating above the screen, showing text editing, resume writing, and language learning features, cinematic lighting, professional setting",
        
        2: "Close-up of typing on a computer keyboard with predictive text suggestions appearing, then zooming out to show a massive data center with glowing servers representing AI model training",
        
        3: "Aerial view of a vast digital library with floating books and documents, then transitioning to a brain-like neural network with glowing connections, representing AI learning from text",
        
        4: "Abstract visualization of a massive library with thousands of glowing switches and dials being adjusted by invisible hands, representing parameter tuning in AI models",
        
        5: "Split-screen animation: left side shows text being read line by line sequentially, right side shows a web of interconnected text elements with attention lines lighting up simultaneously",
        
        6: "Three professionals at their desks: a student writing a thesis, an office worker composing emails, and a programmer coding, each with AI assistance visualized as helpful digital overlays",
        
        7: "Multiple screens showing different types of media - text documents, images, audio waveforms, and video feeds - all connecting to a central AI brain visualization",
        
        8: "A split scene showing an AI confidently giving incorrect information on one side, and a human fact-checker with magnifying glass verifying information on the other side",
        
        9: "Comparison of a mechanical robot following rigid programming rules versus a student learning and adapting to solve new problems through pattern recognition",
        
        10: "Timeline visualization showing the evolution from small early computers to massive modern data centers, with AI capabilities growing exponentially over time",
        
        11: "A balanced workspace showing humans and AI working together - the AI as a powerful tool or external brain augmentation, with humans maintaining oversight and control",
        
        12: "A person sitting at a modern workspace with a computer showing an AI assistant interface, working collaboratively while maintaining human agency and decision-making"
    }
    
    return prompts.get(index, f"Professional technology demonstration related to artificial intelligence and large language models, segment {index}")

def main():
    """主函数"""
    print("🎬 AI视频批量生成工具")
    print("=====================================")
    
    # 检查现有视频
    existing_videos = []
    for i in range(1, 13):
        video_path = os.path.join(VIDEOS_DIR, f"ai_video_{i}.mp4")
        if os.path.exists(video_path):
            existing_videos.append(i)
    
    if existing_videos:
        print(f"已存在的AI视频：{existing_videos}")
        choice = input("是否重新生成所有视频？(y/N): ").strip().lower()
        if choice != 'y':
            print("仅生成缺失的视频...")
    
    # 获取需要生成的视频提示词
    video_prompts = create_video_prompts()
    
    if not video_prompts:
        print("❌ 无法获取视频提示词")
        return
    
    print(f"准备生成 {len(video_prompts)} 个视频片段")
    
    # 批量生成
    successful_videos = []
    failed_videos = []
    rate_limited_count = 0
    
    for prompt_info in video_prompts:
        index = prompt_info["index"]
        prompt = prompt_info["prompt"]
        
        # 检查是否需要跳过
        video_path = os.path.join(VIDEOS_DIR, f"ai_video_{index}.mp4")
        if os.path.exists(video_path) and choice != 'y':
            print(f"⏭️  跳过片段 {index} (已存在)")
            successful_videos.append(index)
            continue
        
        # 生成视频
        result = generate_single_video(prompt, index)
        
        if result == "rate_limited":
            rate_limited_count += 1
            failed_videos.append(index)
            print(f"⏱️  片段 {index} 因限流失败")
            
            # 如果连续遇到限流，等待更长时间
            if rate_limited_count >= 2:
                print("连续遇到限流，等待5分钟...")
                time.sleep(300)
                rate_limited_count = 0
        
        elif result:
            successful_videos.append(index)
            print(f"✅ 片段 {index} 生成成功")
            # 成功后短暂休息，避免过快请求
            time.sleep(10)
        
        else:
            failed_videos.append(index)
            print(f"❌ 片段 {index} 生成失败")
    
    # 生成报告
    print("\n" + "="*50)
    print("📊 批量生成完成报告")
    print("="*50)
    print(f"✅ 成功生成：{len(successful_videos)} 个")
    print(f"❌ 生成失败：{len(failed_videos)} 个")
    
    if successful_videos:
        print(f"成功的片段：{successful_videos}")
    
    if failed_videos:
        print(f"失败的片段：{failed_videos}")
        print("\n💡 建议：")
        print("1. 等待一段时间后重新运行此脚本")
        print("2. 检查网络连接和API配额")
        print("3. 联系API提供商了解限流政策")
    
    # 检查是否可以进行视频合成
    total_expected = 12
    total_generated = len([f for f in os.listdir(VIDEOS_DIR) if f.startswith("ai_video_") and f.endswith(".mp4")])
    
    print(f"\n📹 当前AI视频状态：{total_generated}/{total_expected}")
    
    if total_generated >= 10:  # 至少有10个视频就可以合成
        print("🎉 有足够的AI视频可以重新合成最终视频！")
        print("下一步：运行视频合成脚本")
    else:
        print("⚠️  AI视频数量不足，建议解决限流问题后重新生成")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 脚本执行出错：{e}")
        sys.exit(1)