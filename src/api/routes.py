from fastapi import APIRouter
from pydantic import BaseModel
from crew import UXInsightCrew
# LangSmith tracing
from langchain.callbacks import tracing_v2_enabled

router = APIRouter()

class UXInput(BaseModel):
    heatmap: dict

@router.post("/analisar-ux")
def analisar_ux(payload: UXInput):
    crew_instance = UXInsightCrew()
    crew = crew_instance.crew()
    with tracing_v2_enabled(project_name="phoenix-app"):
        result = crew.kickoff(inputs={
            "heatmap": payload.heatmap
        })

    return {"descricao": result.raw}
