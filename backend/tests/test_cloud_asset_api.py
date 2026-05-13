"""
云资产管理 API 测试
"""

import pytest


class TestCloudAssetAPI:
    """云资产管理 API 测试类"""
    
    def test_get_cloud_assets_list(self, auth_client):
        """测试获取云资产列表"""
        response = auth_client.get("/api/v1/cloud-assets/")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
    
    def test_create_cloud_asset(self, auth_client):
        """测试创建云资产"""
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
        
        response = auth_client.post(
            "/api/v1/cloud-assets/",
            json=asset_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["cloud_provider"] == "aliyun"
        assert data["resource_type"] == "ECS"
        assert "id" in data
    
    def test_get_cloud_asset_by_id(self, auth_client):
        """测试根据ID获取云资产详情"""
        # 先创建一个云资产
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
        create_response = auth_client.post(
            "/api/v1/cloud-assets/",
            json=asset_data
        )
        asset_id = create_response.json()["id"]
        
        # 获取云资产详情
        response = auth_client.get(f"/api/v1/cloud-assets/{asset_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["cloud_provider"] == "aliyun"
    
    def test_get_cloud_asset_not_found(self, auth_client):
        """测试获取不存在的云资产"""
        response = auth_client.get("/api/v1/cloud-assets/9999")
        
        assert response.status_code == 404
    
    def test_update_cloud_asset(self, auth_client):
        """测试更新云资产"""
        # 先创建一个云资产
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
        create_response = auth_client.post(
            "/api/v1/cloud-assets/",
            json=asset_data
        )
        asset_id = create_response.json()["id"]
        
        # 更新云资产
        update_data = {
            "instance_spec": "ecs.g6.xlarge",
            "lifecycle": "stopped"
        }
        response = auth_client.put(
            f"/api/v1/cloud-assets/{asset_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["instance_spec"] == "ecs.g6.xlarge"
        assert data["lifecycle"] == "stopped"
    
    def test_delete_cloud_asset(self, auth_client):
        """测试删除云资产"""
        # 先创建一个云资产
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
        create_response = auth_client.post(
            "/api/v1/cloud-assets/",
            json=asset_data
        )
        asset_id = create_response.json()["id"]
        
        # 删除云资产
        response = auth_client.delete(f"/api/v1/cloud-assets/{asset_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "云资产已删除"
    
    def test_get_cloud_asset_stats(self, auth_client):
        """测试获取云资产统计信息"""
        response = auth_client.get("/api/v1/cloud-assets/stats/summary")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_assets" in data
        assert "provider_distribution" in data
        assert "type_distribution" in data
