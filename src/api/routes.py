from fastapi import APIRouter
from pydantic import BaseModel
from crew import create_crew

router = APIRouter()

class AprendizadoInput(BaseModel):
    tema: str

@router.post("/aprender")
def aprender_tema(payload: AprendizadoInput):
    crew = create_crew()
    resultado = crew.kickoff(inputs={"tema": payload.tema})
    return {"resultado": resultado.raw}
