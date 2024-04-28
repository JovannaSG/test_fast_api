from sqlalchemy import select
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, JSONResponse

from backend.schemas import CSV_StructureTable, LessonTable
from backend.database import engine, async_session


app = FastAPI()


@app.get("/{step_id}")
async def get_step_result(step_id: int):
    async with async_session() as session:
        query = select(CSV_StructureTable).filter(
            CSV_StructureTable.step_id == step_id
        )
        result = await session.execute(query)
        data = [dict(r._mapping) for r in result]
    return {"message": data}
