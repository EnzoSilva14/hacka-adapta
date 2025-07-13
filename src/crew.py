from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, crew, task, agent

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
            llm="gpt-4o"
        )

    @agent
    def code_refactor(self) -> Agent:
        return Agent(
            role="Desenvolvedor Front-end especialista em UX",
            goal="Aplicar melhorias de UI/UX no código fonte baseado nas recomendações fornecidas",
            backstory="Você é um desenvolvedor experiente em React e front-end moderno, com foco em criar experiências fluidas e acessíveis.",
            verbose=True,
            memory=True,
            llm="gpt-4o"
        )

    @task
    def analyze_mocked_heatmap(self) -> Task:
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
    def apply_ui_fixes_to_code(self) -> Task:
        return Task(
            description=(
                "Você receberá um dicionário JSON chamado 'heatmap' com dados comportamentais, "
                "junto com um código fonte base da aplicação em React.\n\n"
                "Baseado nas sugestões geradas pela análise de UX, implemente mudanças diretamente no código, como ajustes de layout, foco em mobile, organização visual ou clareza de navegação.\n\n"
                "Mantenha o estilo do código limpo e com boas práticas, e inclua comentários no código explicando as mudanças feitas."
            ),
            expected_output="Arquivo(s) atualizados com as mudanças no código aplicando as recomendações de UI/UX.",
            agent=self.code_refactor()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.ux_analyst(), self.code_refactor()],
            tasks=[self.analyze_mocked_heatmap(), self.apply_ui_fixes_to_code()],
            process=Process.sequential,
            verbose=True
        )
