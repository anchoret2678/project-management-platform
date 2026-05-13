import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings
from app.utils.exceptions import FileTooLargeException, UnsupportedFileTypeException


class FileHandler:
    """文件处理工具类"""
    
    # 允许的文件类型
    ALLOWED_EXTENSIONS = {
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'txt': 'text/plain',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
    }
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """获取文件扩展名"""
        return Path(filename).suffix.lower()[1:] if '.' in filename else ''
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """检查文件类型是否允许"""
        ext = FileHandler.get_file_extension(filename)
        return ext in FileHandler.ALLOWED_EXTENSIONS
    
    @staticmethod
    def get_mime_type(filename: str) -> str:
        """获取文件的MIME类型"""
        ext = FileHandler.get_file_extension(filename)
        return FileHandler.ALLOWED_EXTENSIONS.get(ext, 'application/octet-stream')
    
    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """生成唯一的文件名"""
        ext = FileHandler.get_file_extension(original_filename)
        unique_id = str(uuid.uuid4())
        return f"{unique_id}.{ext}" if ext else unique_id
    
    @staticmethod
    async def save_upload_file(upload_file: UploadFile, subdirectory: str = "") -> dict:
        """保存上传的文件"""
        # 检查文件大小
        content = await upload_file.read()
        file_size = len(content)
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise FileTooLargeException(f"文件大小不能超过 {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB")
        
        # 检查文件类型
        if not FileHandler.is_allowed_file(upload_file.filename):
            raise UnsupportedFileTypeException(f"不支持的文件类型，允许的类型: {', '.join(FileHandler.ALLOWED_EXTENSIONS.keys())}")
        
        # 生成保存路径
        unique_filename = FileHandler.generate_unique_filename(upload_file.filename)
        save_dir = Path(settings.UPLOAD_DIR) / subdirectory
        save_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = save_dir / unique_filename
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 返回文件信息
        return {
            "original_filename": upload_file.filename,
            "saved_filename": unique_filename,
            "file_path": str(file_path.relative_to(Path.cwd())),
            "file_size": file_size,
            "file_type": FileHandler.get_mime_type(upload_file.filename),
            "extension": FileHandler.get_file_extension(upload_file.filename)
        }
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """删除文件"""
        try:
            full_path = Path(file_path)
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """获取文件信息"""
        full_path = Path(file_path)
        if not full_path.exists():
            return None
        
        return {
            "path": str(full_path),
            "size": full_path.stat().st_size,
            "modified_time": full_path.stat().st_mtime,
            "exists": True
        }
    
    @staticmethod
    def get_download_url(file_path: str, request) -> str:
        """获取文件下载URL"""
        relative_path = str(Path(file_path).relative_to(Path.cwd()))
        return str(request.url_for("static", path=relative_path))
    
    @staticmethod
    def get_preview_url(file_path: str, request) -> Optional[str]:
        """获取文件预览URL（仅支持图片和PDF）"""
        ext = FileHandler.get_file_extension(file_path)
        if ext in ['pdf', 'jpg', 'jpeg', 'png', 'gif']:
            return FileHandler.get_download_url(file_path, request)
        return None