"""
知识库 API 测试
"""

import pytest


class TestKnowledgeAPI:
    """知识库 API 测试类"""
    
    def test_get_knowledge_list(self, auth_client):
        """测试获取知识库列表"""
        response = auth_client.get("/api/v1/knowledge/")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
    
    def test_create_knowledge(self, auth_client):
        """测试创建知识条目"""
        knowledge_data = {
            "title": "测试知识条目",
            "content": "这是测试知识内容",
            "category": "技术文档",
            "tags": ["测试", "文档"],
            "is_public": True
        }
        
        response = auth_client.post(
            "/api/v1/knowledge/",
            json=knowledge_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "测试知识条目"
        assert "id" in data
    
    def test_get_knowledge_by_id(self, auth_client):
        """测试根据ID获取知识条目详情"""
        # 先创建一个知识条目
        knowledge_data = {
            "title": "测试知识条目",
            "content": "这是测试知识内容",
            "category": "技术文档",
            "tags": ["测试", "文档"],
            "is_public": True
        }
        create_response = auth_client.post(
            "/api/v1/knowledge/",
            json=knowledge_data
        )
        knowledge_id = create_response.json()["id"]
        
        # 获取知识条目详情
        response = auth_client.get(f"/api/v1/knowledge/{knowledge_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "测试知识条目"
    
    def test_update_knowledge(self, auth_client):
        """测试更新知识条目"""
        # 先创建一个知识条目
        knowledge_data = {
            "title": "测试知识条目",
            "content": "这是测试知识内容",
            "category": "技术文档",
            "tags": ["测试", "文档"],
            "is_public": True
        }
        create_response = auth_client.post(
            "/api/v1/knowledge/",
            json=knowledge_data
        )
        knowledge_id = create_response.json()["id"]
        
        # 更新知识条目
        update_data = {
            "title": "更新后的标题",
            "content": "更新后的内容"
        }
        response = auth_client.put(
            f"/api/v1/knowledge/{knowledge_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新后的标题"
        assert data["content"] == "更新后的内容"
    
    def test_delete_knowledge(self, auth_client):
        """测试删除知识条目"""
        # 先创建一个知识条目
        knowledge_data = {
            "title": "测试知识条目",
            "content": "这是测试知识内容",
            "category": "技术文档",
            "tags": ["测试", "文档"],
            "is_public": True
        }
        create_response = auth_client.post(
            "/api/v1/knowledge/",
            json=knowledge_data
        )
        knowledge_id = create_response.json()["id"]
        
        # 删除知识条目
        response = auth_client.delete(f"/api/v1/knowledge/{knowledge_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "知识条目已删除"
