#!/bin/bash

# Script to fix video timestamp issues
cd /Users/yu/atlascloud/ms-agent/output_video

echo "Creating properly timestamped segments..."

# Re-encode all segments with proper timestamps
for i in {1..11}; do
    if [ -f "manim_render/scene_${i}/Scene${i}.mov" ] && [ -f "audio/segment_${i}.mp3" ]; then
        echo "Re-encoding segment ${i} with proper timestamps..."
        ffmpeg -i "manim_render/scene_${i}/Scene${i}.mov" -i "audio/segment_${i}.mp3" \
               -c:v libx264 -c:a aac -shortest \
               -video_track_timescale 15360 -avoid_negative_ts make_zero \
               -fflags +genpts -y "fixed_segment${i}.mp4"
    fi
done

# Handle segment 12 with dummy video
if [ -f "videos/video_12.mp4" ] && [ -f "audio/segment_12.mp3" ]; then
    echo "Re-encoding segment 12 with proper timestamps..."
    ffmpeg -i "videos/video_12.mp4" -i "audio/segment_12.mp3" \
           -c:v libx264 -c:a aac -shortest \
           -video_track_timescale 15360 -avoid_negative_ts make_zero \
           -fflags +genpts -y "fixed_segment12.mp4"
fi

echo "Creating proper concat list..."
# Create FFmpeg concat demuxer list
echo "# Fixed concatenation file" > fixed_concat_list.txt
for i in {1..12}; do
    if [ -f "fixed_segment${i}.mp4" ]; then
        echo "file 'fixed_segment${i}.mp4'" >> fixed_concat_list.txt
    fi
done

echo "Concatenating with demuxer..."
# Use demuxer for proper timestamp handling
ffmpeg -f concat -safe 0 -i fixed_concat_list.txt \
       -c copy -avoid_negative_ts make_zero \
       -y properly_fixed_final_video.mp4

echo "Verifying the result..."
ffprobe properly_fixed_final_video.mp4 2>&1 | grep "Duration\|Stream"

echo "Testing for timestamp errors..."
ffmpeg -v error -i properly_fixed_final_video.mp4 -f null - 2>&1 | head -5

echo "Cleaning up intermediate files..."
rm fixed_segment*.mp4 fixed_concat_list.txt

echo "Final video created: properly_fixed_final_video.mp4"