#!/usr/bin/env python3
"""
混合视频合成脚本
将已生成的AI视频与Manim动画结合，创建更好的最终视频
"""

import os
import subprocess
import json

# 基础路径
BASE_DIR = "/Users/yu/atlascloud/ms-agent/output_video"
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
MANIM_DIR = os.path.join(BASE_DIR, "manim_render")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

def check_available_content():
    """检查可用的视频和音频内容"""
    print("🔍 检查可用内容...")
    
    available_content = {}
    
    for segment in range(1, 13):
        content_info = {
            "ai_video": None,
            "manim_video": None,
            "audio": None,
            "preferred": None
        }
        
        # 检查AI视频
        ai_video_path = os.path.join(VIDEOS_DIR, f"ai_video_{segment}.mp4")
        if os.path.exists(ai_video_path):
            content_info["ai_video"] = ai_video_path
            print(f"✅ 片段 {segment}: 找到AI视频 ({os.path.getsize(ai_video_path):,} bytes)")
        
        # 检查Manim视频
        manim_video_path = os.path.join(MANIM_DIR, f"scene_{segment}", f"Scene{segment}.mov")
        if os.path.exists(manim_video_path):
            content_info["manim_video"] = manim_video_path
        
        # 特殊处理第12段
        if segment == 12:
            video_12_path = os.path.join(VIDEOS_DIR, "video_12.mp4")
            if os.path.exists(video_12_path):
                content_info["ai_video"] = video_12_path
        
        # 检查音频
        audio_path = os.path.join(AUDIO_DIR, f"segment_{segment}.mp3")
        if os.path.exists(audio_path):
            content_info["audio"] = audio_path
        
        # 确定首选内容（AI视频优于Manim动画）
        if content_info["ai_video"]:
            content_info["preferred"] = "ai_video"
        elif content_info["manim_video"]:
            content_info["preferred"] = "manim_video"
        
        available_content[segment] = content_info
    
    return available_content

def create_segment_video(segment_num, content_info, output_path):
    """为单个片段创建视频（视频+音频）"""
    
    video_source = None
    if content_info["preferred"] == "ai_video":
        video_source = content_info["ai_video"]
        print(f"📹 片段 {segment_num}: 使用AI视频")
    elif content_info["preferred"] == "manim_video":
        video_source = content_info["manim_video"]
        print(f"🎬 片段 {segment_num}: 使用Manim动画")
    else:
        print(f"❌ 片段 {segment_num}: 没有可用视频源")
        return False
    
    audio_source = content_info["audio"]
    if not audio_source:
        print(f"❌ 片段 {segment_num}: 没有可用音频")
        return False
    
    # FFmpeg命令：合并视频和音频
    cmd = [
        "ffmpeg",
        "-i", video_source,
        "-i", audio_source,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",  # 以最短的流为准
        "-avoid_negative_ts", "make_zero",
        "-fflags", "+genpts",
        "-y",  # 覆盖输出文件
        output_path
    ]
    
    try:
        print(f"🔄 处理片段 {segment_num}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            file_size = os.path.getsize(output_path)
            print(f"✅ 片段 {segment_num} 处理完成 ({file_size:,} bytes)")
            return True
        else:
            print(f"❌ 片段 {segment_num} 处理失败:")
            print(f"Error: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print(f"⏱️ 片段 {segment_num} 处理超时")
        return False
    except Exception as e:
        print(f"❌ 片段 {segment_num} 处理异常: {e}")
        return False

def create_concat_list(segment_files):
    """创建FFmpeg concat文件"""
    concat_file = os.path.join(BASE_DIR, "hybrid_concat_list.txt")
    
    with open(concat_file, 'w') as f:
        f.write("# 混合视频合成列表\n")
        for segment_file in segment_files:
            if os.path.exists(segment_file):
                f.write(f"file '{os.path.basename(segment_file)}'\n")
    
    return concat_file

def concatenate_final_video(segment_files, final_output):
    """合并所有片段为最终视频"""
    print("🎬 合并最终视频...")
    
    # 创建concat文件
    concat_file = create_concat_list(segment_files)
    
    # FFmpeg合并命令
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        "-y",
        final_output
    ]
    
    try:
        # 切换到输出目录运行，因为concat文件使用相对路径
        result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            file_size = os.path.getsize(final_output)
            print(f"🎉 最终视频创建成功!")
            print(f"📁 文件: {final_output}")
            print(f"📊 大小: {file_size:,} bytes")
            
            # 获取视频信息
            probe_cmd = [
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", "-show_streams", final_output
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
            
            if probe_result.returncode == 0:
                info = json.loads(probe_result.stdout)
                duration = float(info["format"]["duration"])
                print(f"⏱️ 时长: {duration:.1f} 秒")
            
            return True
        else:
            print(f"❌ 最终视频合成失败:")
            print(f"Error: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print("⏱️ 最终视频合成超时")
        return False
    except Exception as e:
        print(f"❌ 最终视频合成异常: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(concat_file):
            os.remove(concat_file)

def main():
    """主函数"""
    print("🎬 混合视频合成工具")
    print("=" * 50)
    print("将AI视频与Manim动画结合，创建最终科普视频")
    print("=" * 50)
    
    # 检查可用内容
    available_content = check_available_content()
    
    # 统计内容
    ai_video_count = sum(1 for info in available_content.values() if info["ai_video"])
    manim_video_count = sum(1 for info in available_content.values() if info["manim_video"])
    audio_count = sum(1 for info in available_content.values() if info["audio"])
    
    print(f"\\n📊 内容统计:")
    print(f"🤖 AI视频: {ai_video_count}/12")
    print(f"🎬 Manim动画: {manim_video_count}/12")
    print(f"🎵 音频文件: {audio_count}/12")
    
    # 确定可以处理的片段
    processable_segments = [
        seg for seg, info in available_content.items()
        if info["preferred"] and info["audio"]
    ]
    
    print(f"✅ 可处理片段: {len(processable_segments)}/12")
    print(f"片段列表: {sorted(processable_segments)}")
    
    if len(processable_segments) < 8:
        print(f"\\n⚠️ 警告: 可处理片段少于8个，视频质量可能不理想")
        choice = input("是否继续? (y/N): ").strip().lower()
        if choice != 'y':
            print("操作取消")
            return
    
    # 创建临时片段文件
    print(f"\\n🔄 开始处理 {len(processable_segments)} 个片段...")
    segment_files = []
    successful_segments = 0
    
    for segment_num in sorted(processable_segments):
        content_info = available_content[segment_num]
        segment_file = os.path.join(BASE_DIR, f"hybrid_segment_{segment_num}.mp4")
        
        if create_segment_video(segment_num, content_info, segment_file):
            segment_files.append(segment_file)
            successful_segments += 1
        else:
            print(f"⚠️ 跳过片段 {segment_num}")
    
    print(f"\\n📊 处理结果: {successful_segments}/{len(processable_segments)} 个片段成功")
    
    if successful_segments < 5:
        print("❌ 成功片段太少，无法创建完整视频")
        return
    
    # 合并最终视频
    final_output = os.path.join(BASE_DIR, "hybrid_final_video.mp4")
    
    if concatenate_final_video(segment_files, final_output):
        print(f"\\n🎉 混合视频创建完成!")
        
        # 分析视频构成
        ai_segments = sum(1 for seg in sorted(processable_segments) 
                         if available_content[seg]["preferred"] == "ai_video")
        manim_segments = successful_segments - ai_segments
        
        print(f"\\n📋 视频构成分析:")
        print(f"🤖 AI生成片段: {ai_segments}")
        print(f"🎬 Manim动画片段: {manim_segments}")
        print(f"📊 AI内容比例: {ai_segments/successful_segments*100:.1f}%")
        
        print(f"\\n✨ 相比原始视频的改进:")
        print(f"• 从 1/12 AI视频 提升到 {ai_segments}/{successful_segments}")
        print(f"• 真实视频内容比例大幅提升")
        print(f"• 保持了完整的科普内容结构")
        
        # 建议下一步
        remaining_segments = 12 - ai_segments
        if remaining_segments > 0:
            print(f"\\n💡 建议:")
            print(f"继续生成剩余 {remaining_segments} 个AI视频片段，进一步提升视频质量")
    
    # 清理临时文件
    print(f"\\n🧹 清理临时文件...")
    for segment_file in segment_files:
        if os.path.exists(segment_file):
            os.remove(segment_file)
            print(f"🗑️ 删除: {os.path.basename(segment_file)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n⏹️ 用户中断操作")
    except Exception as e:
        print(f"\\n❌ 脚本异常: {e}")