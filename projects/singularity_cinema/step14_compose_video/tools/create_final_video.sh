#!/bin/bash

# Script to manually recreate the final video from all components
cd /Users/yu/atlascloud/ms-agent/output_video

echo "Creating individual segment videos..."

# Create individual segment videos (only segments with both animation and audio)
for i in {1..11}; do
    if [ -f "manim_render/scene_${i}/Scene${i}.mov" ] && [ -f "audio/segment_${i}.mp3" ]; then
        echo "Processing segment ${i}..."
        ffmpeg -i "manim_render/scene_${i}/Scene${i}.mov" -i "audio/segment_${i}.mp3" \
               -c:v libx264 -c:a aac -shortest -y "temp_segment${i}.mp4"
    fi
done

# Special handling for segment 12 (using our dummy video)
if [ -f "videos/video_12.mp4" ] && [ -f "audio/segment_12.mp3" ]; then
    echo "Processing segment 12..."
    ffmpeg -i "videos/video_12.mp4" -i "audio/segment_12.mp3" \
           -c:v libx264 -c:a aac -shortest -y "temp_segment12.mp4"
fi

echo "Creating segment list..."
# Create a list of all available segments
ls temp_segment*.mp4 | sort -V > segment_list.txt

# Create FFmpeg concat file
echo "Creating concat file..."
echo "# Concatenation file for final video" > concat_list.txt
for file in $(cat segment_list.txt); do
    echo "file '$file'" >> concat_list.txt
done

echo "Concatenating all segments..."
# Concatenate all segments
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy -y fixed_final_video.mp4

echo "Cleaning up temporary files..."
# Clean up
rm temp_segment*.mp4 segment_list.txt concat_list.txt

echo "Final video created: fixed_final_video.mp4"

# Check the final result
ffprobe fixed_final_video.mp4 2>&1 | grep "Duration\|Stream"