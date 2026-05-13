"""
项目 API 测试
"""

import pytest


class TestProjectAPI:
    """项目 API 测试类"""
    
    def test_get_projects_list(self, auth_client):
        """测试获取项目列表"""
        response = auth_client.get("/api/v1/projects/")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
    
    def test_create_project(self, auth_client):
        """测试创建项目"""
        project_data = {
            "project_code": "TEST001",
            "project_name": "测试项目",
            "application_name": "测试应用",
            "department": "测试部门",
            "manager_id": 1,
            "status": "planning",
            "description": "这是一个测试项目"
        }
        
        response = auth_client.post(
            "/api/v1/projects/",
            json=project_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["project_code"] == "TEST001"
        assert data["project_name"] == "测试项目"
        assert "id" in data
    
    def test_create_project_duplicate_code(self, auth_client):
        """测试创建重复项目编码的项目"""
        project_data = {
            "project_code": "TEST001",
            "project_name": "重复测试项目",
            "application_name": "测试应用",
            "department": "测试部门",
            "manager_id": 1,
            "status": "planning",
            "description": "重复编码测试"
        }
        
        response = auth_client.post(
            "/api/v1/projects/",
            json=project_data
        )
        
        # 应该返回冲突错误
        assert response.status_code in [400, 409]
    
    def test_get_project_by_id(self, auth_client):
        """测试根据ID获取项目详情"""
        # 先创建一个项目
        project_data = {
            "project_code": "TEST002",
            "project_name": "详情测试项目",
            "application_name": "测试应用",
            "department": "测试部门",
            "manager_id": 1,
            "status": "planning",
            "description": "详情测试"
        }
        create_response = auth_client.post(
            "/api/v1/projects/",
            json=project_data
        )
        project_id = create_response.json()["id"]
        
        # 获取项目详情
        response = auth_client.get(f"/api/v1/projects/{project_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["project_code"] == "TEST002"
    
    def test_get_project_not_found(self, auth_client):
        """测试获取不存在的项目"""
        response = auth_client.get("/api/v1/projects/9999")
        
        assert response.status_code == 404
    
    def test_update_project(self, auth_client):
        """测试更新项目"""
        # 先创建一个项目
        project_data = {
            "project_code": "TEST003",
            "project_name": "更新测试项目",
            "application_name": "测试应用",
            "department": "测试部门",
            "manager_id": 1,
            "status": "planning",
            "description": "更新测试"
        }
        create_response = auth_client.post(
            "/api/v1/projects/",
            json=project_data
        )
        project_id = create_response.json()["id"]
        
        # 更新项目
        update_data = {
            "project_name": "更新后的项目名称",
            "status": "in_progress"
        }
        response = auth_client.put(
            f"/api/v1/projects/{project_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["project_name"] == "更新后的项目名称"
        assert data["status"] == "in_progress"
    
    def test_delete_project(self, auth_client):
        """测试删除项目"""
        # 先创建一个项目
        project_data = {
            "project_code": "TEST004",
            "project_name": "删除测试项目",
            "application_name": "测试应用",
            "department": "测试部门",
            "manager_id": 1,
            "status": "planning",
            "description": "删除测试"
        }
        create_response = auth_client.post(
            "/api/v1/projects/",
            json=project_data
        )
        project_id = create_response.json()["id"]
        
        # 删除项目
        response = auth_client.delete(f"/api/v1/projects/{project_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "项目已删除"
    
    def test_search_projects(self, auth_client):
        """测试搜索项目"""
        # 创建测试项目
        project_data = {
            "project_code": "SEARCH001",
            "project_name": "搜索测试项目",
            "application_name": "测试应用",
            "department": "测试部门",
            "manager_id": 1,
            "status": "planning",
            "description": "搜索测试"
        }
        auth_client.post("/api/v1/projects/", json=project_data)
        
        # 搜索项目
        response = auth_client.get(
            "/api/v1/projects/",
            params={"keyword": "搜索测试"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
    
    def test_get_project_stats(self, auth_client):
        """测试获取项目统计信息"""
        response = auth_client.get("/api/v1/projects/stats/summary")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_projects" in data
        assert "status_distribution" in data
        assert "department_distribution" in data
