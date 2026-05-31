"""
Servicio de almacenamiento para archivos de audio
"""

import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
import boto3
from botocore.exceptions import NoCredentialsError
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY
        )
        self.bucket_name = settings.MINIO_BUCKET
        
    async def ensure_bucket_exists(self):
        """Asegurar que el bucket existe"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            except NoCredentialsError:
                raise HTTPException(status_code=500, detail="Error de configuración de almacenamiento")
    
    async def upload_audio_file(
        self,
        file: UploadFile,
        user_id: int
    ) -> str:
        """Subir archivo de audio y retornar la URL"""
        await self.ensure_bucket_exists()
        
        # Validar tipo de archivo
        allowed_extensions = ['.mp3', '.wav', '.ogg', '.m4a']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Formato no permitido. Formatos aceptados: {', '.join(allowed_extensions)}"
            )
        
        # Generar nombre único
        unique_filename = f"{user_id}_{uuid.uuid4().hex}{file_ext}"
        object_key = f"audio/{unique_filename}"
        
        try:
            # Subir archivo
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                object_key,
                ExtraArgs={'ContentType': file.content_type}
            )
            
            # Retornar URL pública
            return f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{object_key}"
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")
    
    async def upload_cover_image(
        self,
        file: UploadFile,
        user_id: int
    ) -> str:
        """Subir imagen de portada y retornar la URL"""
        await self.ensure_bucket_exists()
        
        # Validar tipo de archivo
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Formato no permitido. Formatos aceptados: {', '.join(allowed_extensions)}"
            )
        
        # Generar nombre único
        unique_filename = f"{user_id}_{uuid.uuid4().hex}{file_ext}"
        object_key = f"covers/{unique_filename}"
        
        try:
            # Subir archivo
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                object_key,
                ExtraArgs={'ContentType': file.content_type}
            )
            
            # Retornar URL pública
            return f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{object_key}"
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al subir imagen: {str(e)}")
    
    async def delete_file(self, file_url: str) -> bool:
        """Eliminar archivo por URL"""
        try:
            # Extraer object_key de la URL
            object_key = file_url.split(f"/{self.bucket_name}/")[-1]
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except Exception:
            return False

storage_service = StorageService()
