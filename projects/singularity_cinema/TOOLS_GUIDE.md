# Singularity Cinema 工具使用指南

## 📋 概述

本项目包含完整的AI视频生成和合成工具链，专门用于解决API限流问题并创建高质量的AI+动画混合视频。

## 🗂️ 工具分布

### Step11: AI视频生成工具
> 位置: `step11_generate_video/tools/`

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `test_video_generation.py` | API连接测试 | 验证API配置 |
| `single_video_generator.py` | 单个视频生成 | 精确控制，补充生成 |
| `batch_video_generation.py` | 批量视频生成 | 自动化批量处理 |

### Step14: 视频合成工具
> 位置: `step14_compose_video/tools/`

| 工具 | 功能 | 推荐度 |
|------|------|--------|
| `create_ai_hybrid_video.sh` | AI+Manim混合合成 | ⭐⭐⭐⭐⭐ |
| `create_hybrid_final_video_fixed.py` | Python版混合合成 | ⭐⭐⭐⭐ |
| `fix_video_timestamps.sh` | 视频格式修复 | ⭐⭐⭐ |
| `create_final_video.sh` | 基础视频合成 | ⭐⭐ |

## 🚀 快速开始

### 完整工作流程

```bash
# 1. 进入项目目录
cd /Users/yu/atlascloud/ms-agent/projects/singularity_cinema

# 2. 测试API连接（可选）
conda run -n ms-agent python step11_generate_video/tools/test_video_generation.py

# 3. 批量生成AI视频
conda run -n ms-agent python step11_generate_video/tools/batch_video_generation.py

# 4. 创建混合最终视频
cd ../../output_video
../projects/singularity_cinema/step14_compose_video/tools/create_ai_hybrid_video.sh
```

### 补充特定片段

```bash
# 生成特定片段的AI视频
conda run -n ms-agent python step11_generate_video/tools/single_video_generator.py 6
conda run -n ms-agent python step11_generate_video/tools/single_video_generator.py 8

# 重新合成视频
cd ../../output_video
../projects/singularity_cinema/step14_compose_video/tools/create_ai_hybrid_video.sh
```

## 📊 预期输出

### AI视频生成结果:
```
output_video/videos/
├── ai_video_1.mp4    # 506 KB - AI助手介绍
├── ai_video_2.mp4    # 678 KB - 自动补全概念
├── ai_video_3.mp4    # 1.78 MB - 文本城市概念
├── ai_video_4.mp4    # 1.14 MB - 参数调整
├── ai_video_5.mp4    # 592 KB - Transformer架构
├── ai_video_7.mp4    # 1.19 MB - 多模态AI
└── ai_video_10.mp4   # 888 KB - AI发展历史
```

### 最终合成视频:
```
output_video/
└── ai_hybrid_final_video.mp4  # 7.4 MB, 2分12秒, 58.3% AI内容
```

## 🛠️ 故障排除

### 常见问题

#### 1. API限流 (429错误)
**症状**: "Too Many Requests" 错误
**解决**: 工具自动处理，等待60秒后重试

#### 2. 视频无法播放
**症状**: 文件存在但播放器无法打开
**解决**: 
```bash
# 使用时间戳修复工具
./step14_compose_video/tools/fix_video_timestamps.sh
```

#### 3. 分辨率不匹配
**症状**: AI视频(720x1280) vs Manim(1450x800)
**解决**: 混合工具自动处理，无需手动干预

#### 4. 音频同步问题
**症状**: 音视频不同步
**解决**: 使用`-shortest`参数的工具（已内置）

### 环境检查

```bash
# 检查Conda环境
conda list -n ms-agent | grep -E "(aiohttp|yarl|edge-tts|manim)"

# 检查FFmpeg
ffmpeg -version

# 检查API密钥
grep "apikey" projects/singularity_cinema/agent.yaml
```

## 📈 性能优化建议

### API使用优化:
1. **分时段生成**: 避开高峰期使用API
2. **分批处理**: 每次生成2-3个视频
3. **监控配额**: 关注API使用限制

### 存储优化:
1. **定期清理**: 删除临时文件和测试视频
2. **压缩存储**: 使用较高压缩比的H.264设置
3. **备份策略**: 重要视频文件及时备份

## 🔧 高级配置

### 自定义提示词
编辑 `step11_generate_video/tools/single_video_generator.py` 中的prompts字典:

```python
prompts = {
    1: "Your custom prompt for segment 1",
    2: "Your custom prompt for segment 2",
    # ...
}
```

### 视频参数调整
修改API调用参数:

```python
data = {
    "model": "openai/sora-2/text-to-video-pro",
    "duration": 4,      # 视频长度 (秒)
    "size": "720*1280"  # 分辨率
}
```

### FFmpeg参数优化
在合成脚本中调整编码参数:

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium output.mp4
```

## 📝 更新日志

### v1.2 (2024-12-04)
- ✅ 解决API限流问题
- ✅ 实现AI+Manim混合合成
- ✅ 创建完整工具链
- ✅ 提升AI视频比例至58.3%

### v1.1 (2024-12-03)
- ✅ 修复401认证错误
- ✅ 解决yarl依赖冲突
- ✅ 完成基础视频生成流程

### v1.0 (2024-12-02)
- ✅ 完成项目基础架构
- ✅ 实现15步完整工作流

---

📧 **技术支持**: 如需帮助，请查看各工具目录下的README.md文件