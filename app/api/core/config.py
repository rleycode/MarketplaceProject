from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    OZON_API_KEY: str
    OZON_CLIENT_ID: str
    WB_API_KEY: str
    YANDEX_API_KEY: str
    campaign_id: int 
    
    class Config:
        env_file = ".env"
    
    @property
    def get_url_db(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
        
        
setting = Settings() # type: ignore