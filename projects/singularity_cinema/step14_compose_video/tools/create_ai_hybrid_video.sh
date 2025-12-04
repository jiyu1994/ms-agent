#!/bin/bash

# Script to create hybrid video with AI videos and Manim animations
cd /Users/yu/atlascloud/ms-agent/output_video

echo "🎬 创建混合AI+Manim视频..."

# Process each segment - AI video first, then Manim as fallback
for i in {1..12}; do
    audio_file="audio/segment_${i}.mp3"
    
    if [ -f "$audio_file" ]; then
        # Check for AI video first
        if [ -f "videos/ai_video_${i}.mp4" ]; then
            echo "片段 ${i}: 使用AI视频"
            ffmpeg -i "videos/ai_video_${i}.mp4" -i "$audio_file" \
                   -c:v libx264 -c:a aac -shortest \
                   -video_track_timescale 15360 -avoid_negative_ts make_zero \
                   -fflags +genpts -y "hybrid_segment${i}.mp4"
        elif [ -f "manim_render/scene_${i}/Scene${i}.mov" ]; then
            echo "片段 ${i}: 使用Manim动画"
            ffmpeg -i "manim_render/scene_${i}/Scene${i}.mov" -i "$audio_file" \
                   -c:v libx264 -c:a aac -shortest \
                   -video_track_timescale 15360 -avoid_negative_ts make_zero \
                   -fflags +genpts -y "hybrid_segment${i}.mp4"
        elif [ $i -eq 12 ] && [ -f "videos/video_12.mp4" ]; then
            echo "片段 ${i}: 使用原有video_12"
            ffmpeg -i "videos/video_12.mp4" -i "$audio_file" \
                   -c:v libx264 -c:a aac -shortest \
                   -video_track_timescale 15360 -avoid_negative_ts make_zero \
                   -fflags +genpts -y "hybrid_segment${i}.mp4"
        else
            echo "⚠️ 片段 ${i} 没有可用视频源"
        fi
    else
        echo "⚠️ 片段 ${i} 没有音频文件"
    fi
done

echo "📝 创建合并列表..."
# Create FFmpeg concat demuxer list
echo "# AI混合视频合并文件" > hybrid_concat_list.txt
for i in {1..12}; do
    if [ -f "hybrid_segment${i}.mp4" ]; then
        echo "file 'hybrid_segment${i}.mp4'" >> hybrid_concat_list.txt
    fi
done

echo "🔗 合并最终视频..."
# Use demuxer for proper timestamp handling
ffmpeg -f concat -safe 0 -i hybrid_concat_list.txt \
       -c copy -avoid_negative_ts make_zero \
       -y ai_hybrid_final_video.mp4

echo "✅ 验证结果..."
ffprobe ai_hybrid_final_video.mp4 2>&1 | grep "Duration\\|Stream"

echo "📊 统计AI视频使用情况..."
ai_count=0
manim_count=0
for i in {1..12}; do
    if [ -f "videos/ai_video_${i}.mp4" ]; then
        ai_count=$((ai_count + 1))
    elif [ -f "manim_render/scene_${i}/Scene${i}.mov" ]; then
        manim_count=$((manim_count + 1))
    fi
done

echo "🤖 AI视频片段: ${ai_count}/12"
echo "🎬 Manim动画片段: ${manim_count}/12"

if command -v bc &> /dev/null; then
    percentage=$(echo "scale=1; $ai_count * 100 / 12" | bc)
    echo "📈 AI内容比例: ${percentage}%"
else
    echo "📈 AI内容比例: 约$(( ai_count * 100 / 12 ))%"
fi

echo "🧹 清理临时文件..."
rm hybrid_segment*.mp4 hybrid_concat_list.txt

echo "🎉 AI混合视频创建完成: ai_hybrid_final_video.mp4"

# Final file info
if [ -f "ai_hybrid_final_video.mp4" ]; then
    file_size=$(ls -lh ai_hybrid_final_video.mp4 | awk '{print $5}')
    echo "📁 文件大小: $file_size"
else
    echo "❌ 视频创建失败"
fi