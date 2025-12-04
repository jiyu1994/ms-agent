# Step14 视频合成工具

## 🛠️ 工具概述

此目录包含用于合成最终视频的各种工具，支持AI视频与Manim动画的混合合成。

## 📁 工具说明

### 1. `create_ai_hybrid_video.sh` ⭐ 推荐
**功能**: AI视频与Manim动画的智能混合合成
- 优先使用AI视频，Manim动画作为补充
- 自动检测可用的视频源
- 统一处理音频同步
- 生成统计报告

**使用方法**:
```bash
chmod +x create_ai_hybrid_video.sh
./create_ai_hybrid_video.sh
```

**输出**: `ai_hybrid_final_video.mp4`

### 2. `create_hybrid_final_video_fixed.py`
**功能**: Python版本的混合视频合成器
- 更详细的错误处理
- 支持不同分辨率的视频合成
- 提供完整的统计分析

**使用方法**:
```bash
conda run -n ms-agent python create_hybrid_final_video_fixed.py
```

### 3. `fix_video_timestamps.sh`
**功能**: 视频时间戳修复和重编码
- 解决FFmpeg时间戳不一致问题
- 标准化视频格式
- 确保播放兼容性

**使用方法**:
```bash
chmod +x fix_video_timestamps.sh
./fix_video_timestamps.sh
```

**输出**: `properly_fixed_final_video.mp4`

### 4. `create_final_video.sh`
**功能**: 原始版本的视频合成脚本
- 基础的视频片段合成
- 适用于简单场景

## 🎯 使用建议

### 场景1: 创建AI+Manim混合视频（推荐）
```bash
# 使用智能混合脚本
./create_ai_hybrid_video.sh
```

**优势**:
- AI视频优先，真实内容比例高
- 自动统计AI vs Manim比例
- 完整的进度反馈

### 场景2: 修复视频播放问题
```bash
# 如果视频无法正常播放
./fix_video_timestamps.sh
```

### 场景3: Python环境下合成
```bash
# 如果需要更详细的控制
python create_hybrid_final_video_fixed.py
```

## 📊 输出分析

### AI混合视频统计示例:
```
🤖 AI视频片段: 7/12
🎬 Manim动画片段: 4/12
📈 AI内容比例: 58.3%
```

### 内容优先级:
1. **AI视频** (ai_video_*.mp4) - 真实场景
2. **Manim动画** (Scene*.mov) - 数学演示
3. **占位视频** (video_12.mp4) - 备用内容

## 🔧 技术特点

### 视频处理:
- **编码**: H.264 (libx264)
- **音频**: AAC编码
- **同步**: 自动音视频同步
- **格式**: MP4容器

### 质量保证:
- 时间戳标准化
- 避免负时间戳
- 确保帧率一致性
- 音视频长度匹配

## ⚠️ 注意事项

1. **分辨率差异**: AI视频(720x1280) vs Manim(1450x800)
   - 工具自动处理不同分辨率
   - 保持原始比例和质量

2. **音频同步**: 
   - 使用`-shortest`参数确保同步
   - 自动处理音频格式差异

3. **存储空间**:
   - 最终视频约7-10MB
   - 临时文件在处理后自动清理

## 📁 文件结构

### 输入源:
```
output_video/
├── videos/ai_video_*.mp4      # AI生成视频
├── manim_render/scene_*/      # Manim动画
└── audio/segment_*.mp3        # 音频文件
```

### 输出位置:
```
output_video/
├── ai_hybrid_final_video.mp4     # AI混合视频（推荐）
├── properly_fixed_final_video.mp4 # 时间戳修复版
└── hybrid_final_video.mp4         # Python生成版
```

## 🚀 性能优化

- **并行处理**: 每个片段独立处理
- **增量合成**: 支持断点续传
- **智能缓存**: 避免重复处理已存在文件
- **内存优化**: 流式处理大视频文件