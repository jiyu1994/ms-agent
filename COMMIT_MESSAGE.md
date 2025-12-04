# Proposed Commit Message

## Title (50 characters max):
```
feat: Add AI video generation tools for singularity_cinema
```

## Body:
```
解决API限流问题并实现AI视频批量生成工具

新增功能:
- Step11 AI视频生成工具集 (3个工具)
  - test_video_generation.py: API连接测试
  - single_video_generator.py: 单个视频生成器  
  - batch_video_generation.py: 批量视频生成器
- Step14 视频合成工具集 (5个工具)
  - create_ai_hybrid_video.sh: AI+Manim智能混合合成
  - create_hybrid_final_video_fixed.py: Python版混合合成
  - fix_video_timestamps.sh: 视频格式修复
  - 其他辅助合成工具

技术改进:
- 修复AtlasCloud API 401认证错误 (step11/agent.py)
- 解决429限流问题的完整工具链
- 支持AI视频与Manim动画的智能混合合成
- 从8.3%提升到58.3%的AI视频内容比例

配置更新:
- 增加完善的.gitignore规则，忽略生成的媒体文件
- 添加完整的工具使用文档和指南

测试验证:
- 成功生成7/12个AI视频片段
- 创建7.4MB最终混合视频(2分12秒)
- 所有工具均经过实际使用验证

文档:
- TOOLS_GUIDE.md: 完整工具使用指南
- 各step工具目录的详细README
- 按ms-agent框架规范组织代码结构
```

## Alternative shorter version:
```
feat: Solve API rate limiting with AI video generation tools

- Add Step11 AI video generation tools (test, single, batch)
- Add Step14 video composition tools (hybrid, fix, merge)  
- Fix API 401 auth error and 429 rate limiting issues
- Improve AI video ratio from 8.3% to 58.3%
- Add comprehensive .gitignore and documentation
- Organize tools following ms-agent step structure
```