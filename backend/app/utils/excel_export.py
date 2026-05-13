import pandas as pd
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Any
from fastapi.responses import StreamingResponse


class ExcelExporter:
    """Excel导出工具类"""
    
    @staticmethod
    def export_to_excel(data: List[Dict[str, Any]], sheet_name: str = "数据") -> StreamingResponse:
        """将数据导出为Excel文件"""
        if not data:
            # 创建空DataFrame
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(data)
        
        # 创建内存中的Excel文件
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{sheet_name}_{timestamp}.xlsx"
        
        # 返回StreamingResponse
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    @staticmethod
    def export_projects(projects: List[Dict[str, Any]]) -> StreamingResponse:
        """导出项目数据"""
        return ExcelExporter.export_to_excel(projects, "项目列表")
    
    @staticmethod
    def export_cloud_assets(assets: List[Dict[str, Any]]) -> StreamingResponse:
        """导出云资产数据"""
        return ExcelExporter.export_to_excel(assets, "云资产列表")
    
    @staticmethod
    def export_sows(sows: List[Dict[str, Any]]) -> StreamingResponse:
        """导出SOW数据"""
        return ExcelExporter.export_to_excel(sows, "SOW列表")
    
    @staticmethod
    def export_slas(slas: List[Dict[str, Any]]) -> StreamingResponse:
        """导出SLA数据"""
        return ExcelExporter.export_to_excel(slas, "SLA列表")
    
    @staticmethod
    def export_knowledge_documents(docs: List[Dict[str, Any]]) -> StreamingResponse:
        """导出知识库文档数据"""
        return ExcelExporter.export_to_excel(docs, "知识库文档列表")
    
    @staticmethod
    def format_data_for_export(data: List[Any], fields: List[str] = None) -> List[Dict[str, Any]]:
        """格式化数据用于导出"""
        if not data:
            return []
        
        result = []
        for item in data:
            if hasattr(item, '__dict__'):
                item_dict = item.__dict__
                # 移除SQLAlchemy内部属性
                item_dict = {k: v for k, v in item_dict.items() if not k.startswith('_')}
            elif isinstance(item, dict):
                item_dict = item
            else:
                continue
            
            # 只导出指定字段
            if fields:
                item_dict = {k: v for k, v in item_dict.items() if k in fields}
            
            # 处理特殊类型
            for key, value in item_dict.items():
                if isinstance(value, datetime):
                    item_dict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, list):
                    item_dict[key] = ", ".join(str(v) for v in value)
                elif value is None:
                    item_dict[key] = ""
            
            result.append(item_dict)
        
        return result