import qrcode
import io
import base64
from PIL import Image

class QRCodeService:
    """二维码生成服务"""
    
    @staticmethod
    def generate_qr_code(data, size=(200, 200)):
        """
        生成二维码图片
        
        Args:
            data: 要编码的数据
            size: 图片尺寸，默认200x200
            
        Returns:
            base64编码的图片数据
        """
        try:
            # 创建二维码实例
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            
            # 添加数据
            qr.add_data(data)
            qr.make(fit=True)
            
            # 创建图片
            img = qr.make_image(fill_color="black", back_color="white")
            
            # 调整图片尺寸
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # 转换为base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            print(f"生成二维码失败: {e}")
            return None
    
    @staticmethod
    def generate_qr_code_url(url):
        """
        为URL生成二维码
        
        Args:
            url: 要生成二维码的URL
            
        Returns:
            base64编码的二维码图片
        """
        return QRCodeService.generate_qr_code(url)
