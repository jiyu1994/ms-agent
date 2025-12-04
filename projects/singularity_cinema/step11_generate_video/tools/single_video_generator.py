#!/usr/bin/env python3
"""
单个AI视频生成脚本
更保守的方式，逐个生成AI视频，带有详细的错误处理
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

def generate_video_for_segment(segment_index):
    """为指定段落生成AI视频"""
    
    # 视频提示词映射
    prompts = {
        1: "A modern smartphone on a desk with glowing AI icons floating above the screen, cinematic lighting, 4K quality",
        2: "Close-up of typing on a computer keyboard with predictive text suggestions, then zooming to data center, professional lighting",
        3: "Aerial view of a vast digital library with floating books, transitioning to neural network visualization, ethereal atmosphere",
        4: "Abstract visualization of massive library with thousands of glowing switches being adjusted, high-tech ambiance",
        5: "Split-screen: left shows sequential text reading, right shows interconnected web with attention connections lighting up",
        6: "Three professionals at modern workstations: student, office worker, programmer, each with AI assistance overlay, clean modern office",
        7: "Multiple screens displaying text, images, audio waveforms, videos - all connecting to central AI brain visualization",
        8: "Split scene: AI giving confident but wrong answer on left, human fact-checker with magnifying glass on right",
        9: "Comparison of mechanical robot following rigid rules versus student learning adaptively, high contrast lighting",
        10: "Timeline showing evolution from small computers to massive data centers, AI capabilities growing exponentially",
        11: "Balanced workspace with human and AI collaboration - AI as tool, human maintaining control, professional setting",
        12: "Person at modern workspace with AI assistant interface, collaborative work environment, natural lighting"
    }
    
    prompt = prompts.get(segment_index, f"Professional AI technology demonstration, segment {segment_index}")
    
    print(f"\n🎬 生成视频片段 {segment_index}")
    print(f"提示词: {prompt}")
    print("-" * 60)
    
    # 检查文件是否已存在
    output_file = os.path.join(VIDEOS_DIR, f"ai_video_{segment_index}.mp4")
    if os.path.exists(output_file):
        print(f"⚠️ 文件已存在: {output_file}")
        choice = input("是否重新生成? (y/N): ").strip().lower()
        if choice != 'y':
            print("跳过生成")
            return True
    
    # 生成请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "openai/sora-2/text-to-video-pro",
        "duration": 4,
        "prompt": prompt,
        "size": "720*1280"
    }
    
    # 发送生成请求
    try:
        print("📤 发送生成请求...")
        response = requests.post(f"{BASE_URL}/api/v1/model/generateVideo", 
                                headers=headers, json=data, timeout=30)
        
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 429:
            print("❌ 遇到限流，建议等待后重试")
            return False
        
        if response.status_code != 200:
            print(f"❌ 请求失败: {response.text}")
            return False
        
        result = response.json()
        prediction_id = result["data"]["id"]
        print(f"✅ 获得任务ID: {prediction_id}")
        
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False
    
    # 轮询结果
    poll_url = f"{BASE_URL}/api/v1/model/prediction/{prediction_id}"
    print(f"🔄 开始轮询状态...")
    
    for attempt in range(90):  # 最多轮询3分钟
        try:
            time.sleep(2)
            poll_response = requests.get(poll_url, 
                                       headers={"Authorization": f"Bearer {API_KEY}"}, 
                                       timeout=10)
            
            if poll_response.status_code != 200:
                print(f"轮询失败 #{attempt}: {poll_response.status_code}")
                continue
            
            poll_result = poll_response.json()
            status = poll_result["data"]["status"]
            
            print(f"状态 #{attempt + 1}: {status}")
            
            if status in ["completed", "succeeded"]:
                video_url = poll_result["data"]["outputs"][0]
                print(f"🎉 生成成功! 下载URL: {video_url}")
                
                # 下载视频
                return download_video(video_url, output_file)
            
            elif status == "failed":
                error_msg = poll_result["data"].get("error", "Unknown error")
                print(f"❌ 生成失败: {error_msg}")
                return False
            
            # 仍在处理中，继续等待
            
        except Exception as e:
            print(f"轮询异常 #{attempt}: {e}")
            continue
    
    print("❌ 轮询超时")
    return False

def download_video(video_url, output_path):
    """下载视频文件"""
    try:
        print(f"⬇️ 下载视频到: {output_path}")
        
        response = requests.get(video_url, timeout=120)
        response.raise_for_status()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content)
        print(f"✅ 下载完成! 文件大小: {file_size:,} bytes")
        
        return True
    
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python single_video_generator.py <段落编号>")
        print("例如: python single_video_generator.py 2")
        print("段落编号范围: 1-12")
        sys.exit(1)
    
    try:
        segment_index = int(sys.argv[1])
        if segment_index < 1 or segment_index > 12:
            print("❌ 段落编号必须在 1-12 之间")
            sys.exit(1)
    except ValueError:
        print("❌ 段落编号必须是数字")
        sys.exit(1)
    
    print("🎬 AI视频单个生成工具")
    print("=" * 40)
    
    success = generate_video_for_segment(segment_index)
    
    if success:
        print(f"\n🎉 视频片段 {segment_index} 生成成功!")
        
        # 检查总体进度
        total_videos = 0
        for i in range(1, 13):
            if os.path.exists(os.path.join(VIDEOS_DIR, f"ai_video_{i}.mp4")):
                total_videos += 1
        
        print(f"📊 当前进度: {total_videos}/12 个AI视频")
        
        if total_videos >= 10:
            print("✅ 已有足够视频进行最终合成!")
        
    else:
        print(f"\n❌ 视频片段 {segment_index} 生成失败")
        print("💡 建议:")
        print("1. 检查网络连接")
        print("2. 等待一段时间后重试")
        print("3. 检查API配额和限流状态")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断操作")
        sys.exit(0)