from crewai_tools import tool

@tool("UX JSON Data Extractor")
def analisar_heatmap_json(content: dict) -> str:
    """Transforma o JSON de dados de comportamento em texto descritivo"""
    def pretty(val):
        if isinstance(val, dict):
            return ", ".join(f"{k}: {v}" for k, v in val.items())
        elif isinstance(val, list):
            return "\n".join(str(i) for i in val)
        return str(val)

    texto = []
    for k, v in content.items():
        texto.append(f"{k.upper()}:\n{pretty(v)}\n")
    return "\n".join(texto)
