import asyncio
import aiohttp

# 从您的成功测试中获取的参数
API_KEY = "apikey-dd675b2a3fcb4f1aa88b91503d87f730"
BASE_URL = "https://api.atlascloud.ai"
MODEL = "openai/sora-2/text-to-video-pro"

# 测试1: 使用您的方式
async def test_your_way():
    print("=== 测试您的成功方式 ===")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": MODEL,
        "duration": 4,
        "prompt": "A beautiful sunset over the ocean with gentle waves",
        "size": "720*1280"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BASE_URL}/api/v1/model/generateVideo",
            headers=headers,
            json=data
        ) as resp:
            print(f"状态码: {resp.status}")
            if resp.status != 200:
                print(f"错误: {await resp.text()}")
            else:
                result = await resp.json()
                print(f"成功: {result}")

# 测试2: 模拟项目的方式
async def test_project_way():
    print("\n=== 测试项目方式 ===")
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    
    # 模拟可能存在的额外header设置
    # headers['Authorization'] = 'enable'  # 这会导致401错误
    
    payload = {
        'model': MODEL,
        'duration': 4,
        'prompt': "A beautiful sunset over the ocean with gentle waves",
        'size': "720*1280"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BASE_URL}/api/v1/model/generateVideo",
            headers=headers,
            json=payload
        ) as resp:
            print(f"状态码: {resp.status}")
            if resp.status != 200:
                print(f"错误: {await resp.text()}")
            else:
                result = await resp.json()
                print(f"成功: {result}")

# 测试3: 检查headers被覆盖的情况
async def test_header_override():
    print("\n=== 测试Headers覆盖问题 ===")
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    
    print(f"初始headers: {headers}")
    
    # 模拟项目中可能的错误
    headers['Authorization'] = 'enable'  # 这就是可能的问题
    print(f"覆盖后headers: {headers}")
    
    payload = {
        'model': MODEL,
        'duration': 4,
        'prompt': "A beautiful sunset over the ocean with gentle waves",
        'size': "720*1280"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BASE_URL}/api/v1/model/generateVideo",
            headers=headers,
            json=payload
        ) as resp:
            print(f"状态码: {resp.status}")
            if resp.status != 200:
                print(f"错误: {await resp.text()}")

async def main():
    await test_your_way()
    await test_project_way()
    await test_header_override()

if __name__ == "__main__":
    asyncio.run(main())