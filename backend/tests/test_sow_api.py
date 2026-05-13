"""
SOW API 测试
"""

import pytest


class TestSOWAPI:
    """SOW API 测试类"""
    
    def test_get_sow_list(self, auth_client):
        """测试获取 SOW 列表"""
        response = auth_client.get("/api/v1/sow/")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
    
    def test_create_sow(self, auth_client):
        """测试创建 SOW"""
        sow_data = {
            "project_id": 1,
            "title": "测试SOW",
            "content": "这是SOW内容",
            "status": "draft",
            "version": "1.0"
        }
        
        response = auth_client.post(
            "/api/v1/sow/",
            json=sow_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "测试SOW"
        assert "id" in data
    
    def test_get_sow_by_id(self, auth_client):
        """测试根据ID获取 SOW 详情"""
        # 先创建一个 SOW
        sow_data = {
            "project_id": 1,
            "title": "测试SOW",
            "content": "这是SOW内容",
            "status": "draft",
            "version": "1.0"
        }
        create_response = auth_client.post(
            "/api/v1/sow/",
            json=sow_data
        )
        sow_id = create_response.json()["id"]
        
        # 获取 SOW 详情
        response = auth_client.get(f"/api/v1/sow/{sow_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "测试SOW"
    
    def test_update_sow(self, auth_client):
        """测试更新 SOW"""
        # 先创建一个 SOW
        sow_data = {
            "project_id": 1,
            "title": "测试SOW",
            "content": "这是SOW内容",
            "status": "draft",
            "version": "1.0"
        }
        create_response = auth_client.post(
            "/api/v1/sow/",
            json=sow_data
        )
        sow_id = create_response.json()["id"]
        
        # 更新 SOW
        update_data = {
            "title": "更新后的SOW标题",
            "status": "reviewing"
        }
        response = auth_client.put(
            f"/api/v1/sow/{sow_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新后的SOW标题"
        assert data["status"] == "reviewing"
    
    def test_delete_sow(self, auth_client):
        """测试删除 SOW"""
        # 先创建一个 SOW
        sow_data = {
            "project_id": 1,
            "title": "测试SOW",
            "content": "这是SOW内容",
            "status": "draft",
            "version": "1.0"
        }
        create_response = auth_client.post(
            "/api/v1/sow/",
            json=sow_data
        )
        sow_id = create_response.json()["id"]
        
        # 删除 SOW
        response = auth_client.delete(f"/api/v1/sow/{sow_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "SOW已删除"
