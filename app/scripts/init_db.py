# import asyncio
# from app.db.base import Base
# from app.db.session import engine

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# if __name__ == "__main__":
#     asyncio.run(init_models())


import asyncio
import sys
from pathlib import Path
# from app.db.models import Document

project_root = Path(__file__).parent.parent.parent

# print("project_root === ", project_root)
sys.path.append(str(project_root))

from app.db.base import Base
from app.db.session import engine

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())