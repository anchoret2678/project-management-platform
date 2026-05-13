"""
SLA 管理 API 测试
"""

import pytest


class TestSLAAPI:
    """SLA 管理 API 测试类"""
    
    def test_get_sla_list(self, auth_client):
        """测试获取 SLA 列表"""
        response = auth_client.get("/api/v1/sla/")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
    
    def test_create_sla(self, auth_client):
        """测试创建 SLA"""
        sla_data = {
            "project_id": 1,
            "service_name": "API服务",
            "sla_type": "availability",
            "target_value": 99.9,
            "current_value": 99.5,
            "status": "normal",
            "description": "API服务SLA"
        }
        
        response = auth_client.post(
            "/api/v1/sla/",
            json=sla_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["service_name"] == "API服务"
        assert data["sla_type"] == "availability"
        assert "id" in data
    
    def test_get_sla_by_id(self, auth_client):
        """测试根据ID获取 SLA 详情"""
        # 先创建一个 SLA
        sla_data = {
            "project_id": 1,
            "service_name": "API服务",
            "sla_type": "availability",
            "target_value": 99.9,
            "current_value": 99.5,
            "status": "normal",
            "description": "API服务SLA"
        }
        create_response = auth_client.post(
            "/api/v1/sla/",
            json=sla_data
        )
        sla_id = create_response.json()["id"]
        
        # 获取 SLA 详情
        response = auth_client.get(f"/api/v1/sla/{sla_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["service_name"] == "API服务"
    
    def test_update_sla(self, auth_client):
        """测试更新 SLA"""
        # 先创建一个 SLA
        sla_data = {
            "project_id": 1,
            "service_name": "API服务",
            "sla_type": "availability",
            "target_value": 99.9,
            "current_value": 99.5,
            "status": "normal",
            "description": "API服务SLA"
        }
        create_response = auth_client.post(
            "/api/v1/sla/",
            json=sla_data
        )
        sla_id = create_response.json()["id"]
        
        # 更新 SLA
        update_data = {
            "current_value": 99.8,
            "status": "warning"
        }
        response = auth_client.put(
            f"/api/v1/sla/{sla_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["current_value"] == 99.8
        assert data["status"] == "warning"
    
    def test_delete_sla(self, auth_client):
        """测试删除 SLA"""
        # 先创建一个 SLA
        sla_data = {
            "project_id": 1,
            "service_name": "API服务",
            "sla_type": "availability",
            "target_value": 99.9,
            "current_value": 99.5,
            "status": "normal",
            "description": "API服务SLA"
        }
        create_response = auth_client.post(
            "/api/v1/sla/",
            json=sla_data
        )
        sla_id = create_response.json()["id"]
        
        # 删除 SLA
        response = auth_client.delete(f"/api/v1/sla/{sla_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "SLA已删除"
