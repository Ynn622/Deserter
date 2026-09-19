from zoneinfo import ZoneInfo
from datetime import datetime


class TaiwanTime:
    """台灣時間處理類別"""
    
    TIMEZONE = ZoneInfo("Asia/Taipei")
    
    @classmethod
    def now(cls) -> datetime:
        """
        取得台灣目前時間。
        
        Returns: 
            datetime: 台灣目前時間的 datetime 物件。
        """
        return datetime.now(cls.TIMEZONE)
    
    @classmethod
    def string(cls, time: bool = True, ms: bool = False) -> str:
        """
        取得台灣目前時間字串。
        
        Args:
            time (bool): 是否包含時分秒 (預設 True)。
            ms (bool): 是否包含毫秒 (預設 False)。
            
        Returns: 
            str: "YYYY-MM-DD"、"YYYY-MM-DD HH:MM:SS" 或 "YYYY-MM-DD HH:MM:SS:SSS"
        """
        taiwan_now = cls.now()
        
        if not time:
            # YYYY-MM-DD
            return taiwan_now.strftime("%Y-%m-%d")
        
        base_time = taiwan_now.strftime("%Y-%m-%d %H:%M:%S")
        
        if ms:
            # YYYY-MM-DD HH:MM:SS:SSS
            return base_time + f":{taiwan_now.microsecond // 1000:03d}"
        else:
            # YYYY-MM-DD HH:MM:SS
            return base_time

    @staticmethod
    def roc_date(value: object) -> str:
        """將民國年或西元年日期轉換成 YYYY-MM-DD 格式。"""
        text = str(value).strip().replace("/", "").replace("-", "")
        if len(text) == 7 and text.isdigit():
            return f"{int(text[:3]) + 1911:04d}-{text[3:5]}-{text[5:]}"
        if len(text) == 8 and text.isdigit():
            return f"{text[:4]}-{text[4:6]}-{text[6:]}"
        try:
            return datetime.fromisoformat(str(value)).date().isoformat()
        except ValueError:
            return str(value)
