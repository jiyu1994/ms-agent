#!/bin/bash

# Fix video duration mismatch - loop short AI videos to match audio length
cd /Users/yu/atlascloud/ms-agent/output_video

echo "🔧 修复AI视频时长不匹配问题..."

# Create fixed segments with proper duration matching
for i in {1..12}; do
    audio_file="audio/segment_${i}.mp3"
    
    if [ -f "$audio_file" ]; then
        # Get audio duration in seconds
        audio_duration=$(ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio_file")
        echo "片段 $i: 音频时长 ${audio_duration}s"
        
        if [ -f "videos/ai_video_${i}.mp4" ]; then
            video_file="videos/ai_video_${i}.mp4"
            video_duration=$(ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video_file")
            echo "  AI视频时长: ${video_duration}s"
            
            # If video is shorter than audio, loop the video
            if (( $(echo "$video_duration < $audio_duration" | bc -l) )); then
                echo "  🔄 循环播放AI视频以匹配音频长度..."
                
                # Calculate how many loops we need
                loops=$(echo "scale=0; ($audio_duration / $video_duration) + 1" | bc)
                echo "  需要循环 $loops 次"
                
                # Create looped video
                ffmpeg -stream_loop $loops -i "$video_file" -i "$audio_file" \
                       -c:v libx264 -c:a aac -shortest \
                       -avoid_negative_ts make_zero -fflags +genpts \
                       -y "duration_fixed_segment${i}.mp4"
                
                if [ $? -eq 0 ]; then
                    echo "  ✅ 片段 $i AI视频循环成功"
                else
                    echo "  ❌ 片段 $i AI视频循环失败"
                fi
            else
                echo "  ✅ 时长已匹配，直接合成"
                ffmpeg -i "$video_file" -i "$audio_file" \
                       -c:v libx264 -c:a aac -shortest \
                       -avoid_negative_ts make_zero -fflags +genpts \
                       -y "duration_fixed_segment${i}.mp4"
            fi
            
        elif [ -f "manim_render/scene_${i}/Scene${i}.mov" ]; then
            echo "  🎬 使用Manim动画"
            ffmpeg -i "manim_render/scene_${i}/Scene${i}.mov" -i "$audio_file" \
                   -c:v libx264 -c:a aac -shortest \
                   -avoid_negative_ts make_zero -fflags +genpts \
                   -y "duration_fixed_segment${i}.mp4"
                   
        elif [ $i -eq 12 ] && [ -f "videos/video_12.mp4" ]; then
            echo "  📹 使用原有video_12"
            ffmpeg -i "videos/video_12.mp4" -i "$audio_file" \
                   -c:v libx264 -c:a aac -shortest \
                   -avoid_negative_ts make_zero -fflags +genpts \
                   -y "duration_fixed_segment${i}.mp4"
        else
            echo "  ⚠️ 没有可用视频源"
        fi
    else
        echo "片段 $i: 没有音频文件"
    fi
done

echo "📝 创建修复后的合并列表..."
echo "# Duration-fixed video concatenation file" > duration_fixed_concat_list.txt
for i in {1..12}; do
    if [ -f "duration_fixed_segment${i}.mp4" ]; then
        echo "file 'duration_fixed_segment${i}.mp4'" >> duration_fixed_concat_list.txt
    fi
done

echo "🔗 合并修复后的视频..."
ffmpeg -f concat -safe 0 -i duration_fixed_concat_list.txt \
       -c copy -avoid_negative_ts make_zero \
       -y duration_fixed_final_video.mp4

if [ -f "duration_fixed_final_video.mp4" ]; then
    echo "✅ 修复完成!"
    
    # Show final video info
    echo "📊 最终视频信息:"
    ffprobe duration_fixed_final_video.mp4 2>&1 | grep "Duration\\|Stream"
    
    # Show file size
    file_size=$(ls -lh duration_fixed_final_video.mp4 | awk '{print $5}')
    echo "📁 文件大小: $file_size"
    
    # Compare with original
    echo ""
    echo "🔍 与原版对比:"
    echo "原版 ai_hybrid_final_video.mp4:"
    if [ -f "ai_hybrid_final_video.mp4" ]; then
        ffprobe ai_hybrid_final_video.mp4 2>&1 | grep "Duration" | head -1
    fi
    echo "修复版 duration_fixed_final_video.mp4:"
    ffprobe duration_fixed_final_video.mp4 2>&1 | grep "Duration" | head -1
    
else
    echo "❌ 修复失败"
fi

echo "🧹 清理临时文件..."
rm duration_fixed_segment*.mp4 duration_fixed_concat_list.txt

echo "🎉 时长修复完成: duration_fixed_final_video.mp4"