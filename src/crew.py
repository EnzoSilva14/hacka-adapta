from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, crew, task, agent
from tools.code_read import get_code_from_repository
from tools.code_open_pr import create_pr_with_files
from langchain_openai import ChatOpenAI
import os
from langchain_community.chat_models import ChatLiteLLM
from dotenv import load_dotenv
load_dotenv()

nvidia_llm = ChatLiteLLM(
    model="meta/llama3-70b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"),
    api_base="https://integrate.api.nvidia.com/v1",
    litellm_provider="nvidia"  # ESSENCIAL!
)

@CrewBase
class UXInsightCrew():
    @agent
    def ux_analyst(self) -> Agent:
        return Agent(
            role="Especialista em UX para Produtos Digitais",
            goal="Analisar dados de comportamento de usuários e sugerir melhorias de usabilidade",
            backstory="Você é um especialista em UX com experiência em interpretar dados quantitativos para melhorar a experiência do usuário.",
            verbose=True,
            memory=True,
            llm=nvidia_llm
        )

    @agent
    def code_refactor(self) -> Agent:
        return Agent(
            role="Desenvolvedor Front-end especialista em UX",
            goal=(
                "Aplicar melhorias de UI/UX no código fonte com base nas recomendações fornecidas "
                "e criar um pull request com as alterações implementadas para revisão da equipe."
            ),
            backstory=(
                "Você é um desenvolvedor experiente em React e front-end moderno, com um olhar atento para usabilidade, "
                "acessibilidade e boas práticas de UI. Trabalha com versionamento via GitHub e colabora ativamente com "
                "o time de produto por meio de pull requests claros e bem documentados."
            ),
            verbose=True,
            memory=True,
            tools=[get_code_from_repository, create_pr_with_files],
            llm=nvidia_llm
        )

    @task
    def analyze_metrics(self) -> Task:
        return Task(
            description=(
                "Você receberá um dicionário JSON chamado 'heatmap' com dados comportamentais simulados de usuários (mock).\n"
                "Analise esses dados e gere de 3 a 5 sugestões práticas para melhorar a experiência do usuário, com foco em navegação, layout e engajamento.\n"
                "Use os campos como 'sessões', 'cliques inativos', 'intenção', 'dispositivo' e 'páginas de saída' para embasar suas recomendações."
            ),
            expected_output="Lista de sugestões de melhoria de UX com justificativa baseada nos dados fornecidos no JSON.",
            agent=self.ux_analyst()
        )

    @task
    def develop_changes_and_open_pr(self) -> Task:
        return Task(
            description=(
                "Você receberá uma análise de UX com sugestões de melhorias, junto com um código fonte base da aplicação em React.\n\n"
                "Baseado nas sugestões geradas pela análise de UX, implemente mudanças no arquivo:\n"
                "`src/features/analysis/pages/stock-detail.page.tsx`.\n\n"
                "Mantenha boas práticas de codificação e adicione comentários explicando as mudanças feitas.\n\n"
                "**Depois disso, use a ferramenta `create_pr_with_files`** para:\n"
                "- Criar um novo branch chamado `ux-improvements`\n"
                "- Substituir o conteúdo do arquivo com as suas mudanças\n"
                "- Usar a seguinte mensagem de commit: `Melhorias de UX com base na análise comportamental`\n"
                "- Criar um Pull Request com o título `UX Improvements on Stock Detail Page`\n"
                "- O corpo do PR deve conter um resumo das mudanças aplicadas e as justificativas baseadas nos dados analisados.\n\n"
                "A função `create_pr_with_files` requer os seguintes parâmetros:\n"
                "`new_branch`, `file_path`, `file_content`, `file_message`, `pr_title`, `pr_body`, `repo_full_name`, `base_branch`\n"
                "Certifique-se de preencher todos corretamente, incluindo:\n"
                "- `repo_full_name`: 'hillarykb/lazy-invest-web'\n"
                "- `base_branch`: 'main'\n"
            ),
            expected_output=(
                "Pull Request criado no GitHub com as melhorias aplicadas no arquivo "
                "`stock-detail.page.tsx` e descrição explicando as mudanças feitas."
            ),
            agent=self.code_refactor()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.ux_analyst(), self.code_refactor()],
            tasks=[self.analyze_metrics(), self.develop_changes_and_open_pr()],
            process=Process.sequential,
            verbose=True
        )
