# MS-Agent Singularity Cinema 环境配置指南

## 环境概述
- **操作系统**: macOS (Darwin 22.6.0)
- **Python版本**: 3.10.18
- **Conda环境**: singularity

## 主要依赖版本
- **aiohttp**: 3.13.2
- **yarl**: 1.22.0 (关键兼容性版本)
- **edge-tts**: 7.2.3
- **manim**: 0.19.1
- **ms-agent**: 2.0.0

## 安装步骤

### 1. 创建Conda环境
```bash
conda create -n singularity python=3.10 -y
conda activate singularity
```

### 2. 安装系统依赖
```bash
# 安装pkg-config和cairo (解决pycairo编译问题)
conda install pkg-config cairo -y
```

### 3. 解决依赖冲突
**关键步骤**: 按特定顺序安装兼容版本
```bash
# 使用conda环境的pip直接路径
/path/to/anaconda3/envs/singularity/bin/pip install "yarl<1.10.0" "aiohttp>=3.9.0" edge-tts --force-reinstall
```

### 4. 安装MS-Agent框架
```bash
cd /path/to/ms-agent
/path/to/anaconda3/envs/singularity/bin/pip install -e .
```

### 5. 安装项目依赖
```bash
/path/to/anaconda3/envs/singularity/bin/pip install -r projects/singularity_cinema/requirements.txt
```

### 6. 安装金融数据依赖
```bash
/path/to/anaconda3/envs/singularity/bin/pip install pandas akshare baostock
```

## 遇到的问题和解决方案

### 问题1: yarl/aiohttp版本冲突
**错误现象**: `ImportError: cannot import name 'Query' from 'yarl'`
**根本原因**: yarl 1.9.4没有Query类，但aiohttp 3.8.6尝试导入
**解决方案**: 
- 升级aiohttp到3.10+版本
- 或降级yarl到<1.10.0
- 推荐: `yarl==1.9.11` + `aiohttp==3.10.5`

### 问题2: pip环境混淆
**错误现象**: pip使用系统Python 3.7而非conda环境Python 3.10
**根本原因**: conda环境未正确激活或PATH设置问题
**解决方案**: 
```bash
# 使用conda环境pip的完整路径
/Users/yu/anaconda3/envs/singularity/bin/pip install package_name
# 而不是直接使用 pip install
```

### 问题3: pycairo编译失败
**错误现象**: `pkg-config for machine host machine not found`
**根本原因**: 缺少pkg-config和cairo系统库
**解决方案**:
```bash
conda install pkg-config cairo -y
```

### 问题4: Manim依赖安装
**错误现象**: 多个依赖包编译失败
**根本原因**: 复杂的图形库依赖链
**解决方案**: 确保先安装好cairo相关依赖，然后按requirements.txt安装

### 问题5: edge-tts导入错误
**错误现象**: edge_tts导入失败
**根本原因**: 与yarl/aiohttp冲突相同
**解决方案**: 解决yarl/aiohttp版本冲突后自动修复

## 关键配置文件
- **环境**: `/Users/yu/anaconda3/envs/singularity`
- **项目根目录**: `/Users/yu/atlascloud/ms-agent`
- **配置文件**: `projects/singularity_cinema/agent.yaml`
- **API配置**: AtlasCloud API (apikey-dd675b2a3fcb4f1aa88b91503d87f730)

## 验证安装
```bash
# 激活环境
source /path/to/anaconda3/etc/profile.d/conda.sh
conda activate singularity

# 测试关键导入
python -c "import edge_tts; print('edge_tts OK')"
python -c "import manim; print('manim OK')" 
python -c "import ms_agent; print('ms-agent OK')"
```

## 运行项目
```bash
conda activate singularity
/path/to/anaconda3/envs/singularity/bin/python -m ms_agent.cli.cli run \
    --config "projects/singularity_cinema" \
    --query "您的查询内容" \
    --load_cache true \
    --trust_remote_code true
```

## 注意事项
1. **Python版本**: 必须使用3.10，3.12会导致兼容性问题
2. **依赖安装顺序**: 先安装系统依赖，再安装Python包
3. **pip路径**: 务必使用conda环境的pip完整路径
4. **API配置**: 确保AtlasCloud API密钥配置正确
5. **权限问题**: 某些系统库可能需要管理员权限安装

## 当前状态
- ✅ 环境配置完成
- ✅ 核心功能正常 (脚本生成、音频生成、动画渲染)
- ❌ 视频合成步骤未完成 (API请求错误导致)