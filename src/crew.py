from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
load_dotenv()

def create_crew(llm=None):
    # === AGENTES ===
    tutor = Agent(
        role='Tutor de Aprendizagem Personalizada',
        goal='Facilitar o aprendizado contínuo e eficaz, respondendo perguntas de forma clara...',
        backstory='Você é um tutor experiente com habilidade em explicar conceitos complexos...',
        verbose=True,
        llm=llm
    )

    pedagogo = Agent(
        role='Especialista em Metodologias Educacionais',
        goal='Criar trilhas personalizadas para estilos de aprendizagem diversos',
        backstory='Você é um pedagogo especialista em ensino adaptativo.',
        verbose=True,
        llm=llm
    )

    animador = Agent(
        role='Designer de Conteúdo Visual',
        goal='Criar mapas mentais e visualizações com SVG/animações',
        backstory='Você domina anime.js e torna o conteúdo visualmente compreensível.',
        verbose=True,
        llm=llm
    )

    exercicios = Agent(
        role='Criador de Exercícios e Simulados',
        goal='Gerar questões com dificuldade adaptativa',
        backstory='Você é focado em fixação de conhecimento com prática.',
        verbose=True,
        llm=llm
    )

    motivacional = Agent(
        role='Agente Motivacional',
        goal='Gerar missões e recompensas para engajar o aluno',
        backstory='Você cuida da energia e ânimo do estudante.',
        verbose=True,
        llm=llm
    )

    memoria = Agent(
        role='Guardião da Memória',
        goal='Rastrear e agendar revisões futuras',
        backstory='Você sabe tudo que o aluno já viu e revisou.',
        verbose=True,
        llm=llm
    )

    verificador = Agent(
        role='Verificador de Conteúdo',
        goal='Checar fatos e datas com precisão usando fontes externas',
        backstory='Você combate informações falsas ou erradas com verificação factual.',
        verbose=True,
        llm=llm
    )

    colaborador = Agent(
        role='Facilitador de Estudo Coletivo',
        goal='Conectar alunos para estudo em grupo ou desafios colaborativos',
        backstory='Você promove o aprendizado social e competitivo.',
        verbose=True,
        llm=llm
    )

    conteudista = Agent(
        role='Produtor de Conteúdo Didático',
        goal='Gerar fichamentos e apresentações para alunos e professores',
        backstory='Você transforma conteúdo em material bem formatado.',
        verbose=True,
        llm=llm
    )

    # === TAREFAS ===
    tasks = [
        Task(
            description="Gerar introdução clara para o tema solicitado.",
            expected_output="Texto introdutório claro e bem contextualizado.",
            agent=tutor
        ),
        Task(
            description="Criar trilha de aprendizado adaptada ao estilo do aluno.",
            expected_output="Trilha com 3 etapas (vídeo, flashcard, quiz).",
            agent=pedagogo
        ),
        Task(
            description="Gerar mapa mental animado (estrutura SVG + transições).",
            expected_output="SVG animado usando anime.js ou estrutura semelhante.",
            agent=animador
        ),
        Task(
            description="Criar 5-10 exercícios com múltiplas escolhas e gabarito.",
            expected_output="Lista de questões com níveis variados de dificuldade.",
            agent=exercicios
        ),
        Task(
            description="Validar informações com fontes externas e corrigir erros.",
            expected_output="Lista de afirmações com validação factual.",
            agent=verificador
        ),
        Task(
            description="Criar missão de estudo de 20 minutos com recompensa.",
            expected_output="Missão com instruções, objetivo e mensagem motivacional.",
            agent=motivacional
        ),
        Task(
            description="Registrar o conteúdo estudado e agendar revisão em 3 dias.",
            expected_output="Registro salvo e revisão programada.",
            agent=memoria
        ),
        Task(
            description="Sugerir estudo colaborativo com outro aluno compatível.",
            expected_output="Sugestão de dupla + tema e desafio proposto.",
            agent=colaborador
        ),
        Task(
            description="Gerar resumo e slide em markdown para apresentação.",
            expected_output="Resumo + slide estruturado para professor ou aluno.",
            agent=conteudista
        )
    ]

    return Crew(
        agents=[
            tutor, pedagogo, animador, exercicios,
            motivacional, memoria, verificador,
            colaborador, conteudista
        ],
        tasks=tasks,
        process=Process.sequential
    )
