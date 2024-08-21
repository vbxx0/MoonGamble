import aiohttp
from pydantic import BaseModel

from src.settings import Settings


class AccessTokenData(BaseModel):
    access_token: str
    expires_in: int
    user_id: int


async def get_access_token(code: str):
    async with aiohttp.ClientSession() as session:
        url = 'https://oauth.vk.com/access_token'
        params = {
            'client_id': Settings.VK_CLIENT_ID,
            'client_secret': Settings.VK_SECRET_KEY,
            'redirect_uri': Settings.VK_REDIRECT_URI,
            'code': code
        }
        async with session.get(url, params=params) as respoonse:
            data = await respoonse.json()
            return AccessTokenData(**data)
