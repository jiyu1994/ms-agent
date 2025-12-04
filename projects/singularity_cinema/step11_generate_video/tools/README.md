# Step11 AI视频生成工具

## 🛠️ 工具概述

此目录包含解决API限流问题和批量生成AI视频的专用工具。

## 📁 工具说明

### 1. `test_video_generation.py`
**功能**: API连接测试和单个视频生成验证
- 测试AtlasCloud API连接状态
- 验证API配置和认证
- 生成单个测试视频用于验证

**使用方法**:
```bash
conda run -n ms-agent python test_video_generation.py
```

### 2. `single_video_generator.py`
**功能**: 单个AI视频生成器（保守方式）
- 逐个生成指定片段的AI视频
- 详细的错误处理和状态反馈
- 支持跳过已存在的视频
- 适合手动控制的场景

**使用方法**:
```bash
conda run -n ms-agent python single_video_generator.py <段落编号>
# 例如: python single_video_generator.py 3
```

**特点**:
- 支持段落编号 1-12
- 自动检测已存在文件
- 实时进度反馈
- 包含英文提示词映射

### 3. `batch_video_generation.py`
**功能**: 批量AI视频生成器（自动化方式）
- 自动批量生成所有12个AI视频片段
- 智能限流检测和等待机制
- 完整的错误处理和重试逻辑
- 详细的进度报告和统计

**使用方法**:
```bash
conda run -n ms-agent python batch_video_generation.py
```

**特点**:
- 基于segments.txt自动生成提示词
- 429限流自动处理（等待60秒）
- 支持断点续传
- 生成完整的成功/失败报告

## 🎯 使用建议

### 场景1: 首次生成所有视频
```bash
# 推荐使用批量生成工具
python batch_video_generation.py
```

### 场景2: 补充缺失的特定片段
```bash
# 使用单个生成器逐个处理
python single_video_generator.py 6
python single_video_generator.py 8
```

### 场景3: 测试API状态
```bash
# 先测试API连接
python test_video_generation.py
```

## ⚠️ 注意事项

1. **API限流**: 遇到429错误时，工具会自动等待，请耐心等待
2. **文件检查**: 生成前会检查已存在的文件，避免重复生成
3. **网络稳定**: 确保网络连接稳定，视频生成通常需要1-2分钟
4. **存储空间**: 确保有足够空间存储AI视频文件（约1-2MB/个）

## 📊 输出位置

所有生成的AI视频保存在:
```
/Users/yu/atlascloud/ms-agent/output_video/videos/
├── ai_video_1.mp4
├── ai_video_2.mp4
├── ...
└── ai_video_12.mp4
```

## 🔧 技术细节

- **API端点**: https://api.atlascloud.ai/api/v1/model/generateVideo
- **模型**: openai/sora-2/text-to-video-pro
- **分辨率**: 720x1280
- **时长**: 4秒
- **格式**: MP4 (H.264)