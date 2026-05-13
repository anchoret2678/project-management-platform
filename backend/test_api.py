#!/usr/bin/env python3
"""
企业项目管理平台 - API测试脚本
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}


def print_response(response, description=""):
    """打印响应结果"""
    print(f"\n{'='*60}")
    if description:
        print(f"测试: {description}")
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print("响应数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(f"响应文本: {response.text}")
    print('='*60)


def test_health_check():
    """测试健康检查"""
    print("1. 测试健康检查...")
    response = requests.get("http://localhost:8000/health")
    print_response(response, "健康检查")


def test_auth():
    """测试认证功能"""
    print("\n2. 测试认证功能...")
    
    # 登录
    print("登录测试...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", 
                           data=login_data)
    print_response(response, "用户登录")
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        HEADERS["Authorization"] = f"Bearer {access_token}"
        
        # 获取当前用户信息
        print("获取当前用户信息...")
        response = requests.get(f"{BASE_URL}/auth/me", headers=HEADERS)
        print_response(response, "获取当前用户信息")
        
        return True
    return False


def test_projects():
    """测试项目管理功能"""
    print("\n3. 测试项目管理功能...")
    
    # 获取项目列表
    print("获取项目列表...")
    response = requests.get(f"{BASE_URL}/projects/", headers=HEADERS)
    print_response(response, "获取项目列表")
    
    # 创建测试项目
    print("创建测试项目...")
    project_data = {
        "project_code": "TEST001",
        "project_name": "测试项目",
        "application_name": "测试应用",
        "department": "测试部门",
        "manager_id": 1,
        "status": "planning",
        "description": "这是一个测试项目"
    }
    response = requests.post(f"{BASE_URL}/projects/", 
                           json=project_data, 
                           headers=HEADERS)
    print_response(response, "创建项目")
    
    if response.status_code == 200:
        project = response.json()
        project_id = project.get("id")
        
        # 获取项目详情
        print("获取项目详情...")
        response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=HEADERS)
        print_response(response, "获取项目详情")
        
        # 更新项目
        print("更新项目...")
        update_data = {
            "project_name": "更新后的测试项目",
            "status": "in_progress"
        }
        response = requests.put(f"{BASE_URL}/projects/{project_id}", 
                              json=update_data, 
                              headers=HEADERS)
        print_response(response, "更新项目")
        
        # 获取项目统计
        print("获取项目统计...")
        response = requests.get(f"{BASE_URL}/projects/stats/summary", headers=HEADERS)
        print_response(response, "项目统计")
        
        return project_id
    return None


def test_cloud_assets():
    """测试云资产管理功能"""
    print("\n4. 测试云资产管理功能...")
    
    # 获取云资产列表
    print("获取云资产列表...")
    response = requests.get(f"{BASE_URL}/cloud-assets/", headers=HEADERS)
    print_response(response, "获取云资产列表")
    
    # 创建测试云资产
    print("创建测试云资产...")
    asset_data = {
        "project_id": 1,
        "cloud_provider": "aliyun",
        "resource_type": "ECS",
        "instance_spec": "ecs.g6.large",
        "region": "cn-hangzhou",
        "zone": "cn-hangzhou-h",
        "account_info": "test-account",
        "lifecycle": "running"
    }
    response = requests.post(f"{BASE_URL}/cloud-assets/", 
                           json=asset_data, 
                           headers=HEADERS)
    print_response(response, "创建云资产")
    
    if response.status_code == 200:
        asset = response.json()
        asset_id = asset.get("id")
        
        # 获取云资产详情
        print("获取云资产详情...")
        response = requests.get(f"{BASE_URL}/cloud-assets/{asset_id}", headers=HEADERS)
        print_response(response, "获取云资产详情")
        
        # 获取云资产统计
        print("获取云资产统计...")
        response = requests.get(f"{BASE_URL}/cloud-assets/stats/summary", headers=HEADERS)
        print_response(response, "云资产统计")
        
        return asset_id
    return None


def test_search():
    """测试搜索功能"""
    print("\n5. 测试搜索功能...")
    
    # 搜索项目
    print("搜索项目...")
    response = requests.get(f"{BASE_URL}/projects/", 
                          params={"keyword": "测试"}, 
                          headers=HEADERS)
    print_response(response, "搜索项目")
    
    # 搜索建议
    print("获取项目搜索建议...")
    response = requests.get(f"{BASE_URL}/projects/search/suggestions", 
                          params={"keyword": "测试"}, 
                          headers=HEADERS)
    print_response(response, "项目搜索建议")


def main():
    """主测试函数"""
    print("企业项目管理平台 - API测试")
    print("="*60)
    
    try:
        # 测试健康检查
        test_health_check()
        
        # 测试认证
        if not test_auth():
            print("认证测试失败，请检查服务是否正常运行")
            return
        
        # 测试项目管理
        project_id = test_projects()
        
        # 测试云资产管理
        asset_id = test_cloud_assets()
        
        # 测试搜索功能
        test_search()
        
        print("\n" + "="*60)
        print("API测试完成!")
        print(f"项目ID: {project_id}")
        print(f"云资产ID: {asset_id}")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n错误: 无法连接到服务器")
        print("请确保后端服务已启动: python run.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()