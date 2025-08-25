# Job Boards Scraper (Ashby) — Brazilian‑friendly

Este projeto coleta vagas publicadas em boards (Ashby) de empresas específicas, identifica aquelas amigáveis para candidatos do Brasil e normaliza as informações para uso posterior.

## Como funciona

- Em um agendamento recorrente, a aplicação:
  1. Busca as vagas em páginas públicas (Ashby) de empresas pré‑definidas.
  2. Mapeia e filtra vagas com critérios “Brazilian‑friendly” (ex.: menções a Brazil/Brasil, LATAM, Americas, remoto global, etc., conforme regras por empresa).
  3. Normaliza os campos das vagas (ex.: senioridade, área/field).
  4. Compara o resultado com a última execução e registra diferenças, persistindo um arquivo `last_<empresa>.json` por empresa.
- Logs informam progresso, total de vagas extraídas/filtradas e diferenças encontradas.

Empresas suportadas atualmente incluem: Commure/Athelas, EightSleep, Supabase, Deel e PostHog.

## Requisitos

- Variáveis de ambiente:
  - `DEFAULT_URL`: URL base do job board (Ashby) da qual as rotas específicas de cada empresa serão derivadas.
    - Exemplo ilustrativo: `https://jobs.ashbyhq.com/` (ajuste conforme seu caso real).
  - `TIME_BETWEEN_EXECUTIONS`: intervalo em minutos entre execuções agendadas (ex.: `30`).
- Rede com acesso de saída para alcançar o(s) job board(s).
- Permissões de escrita no diretório de trabalho para persistir `last_<empresa>.json`.

## Rodando com Docker Compose (recomendado)

1) Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias descritas no `.env.example`

2) Suba o serviço:
```
docker compose up -d
``` 

3) Acompanhe os logs:
```
docker compose logs -f jobs-scraper
``` 

## Rodando localmente (opcional)

- Requer Python 3.12+ e dependências instaladas (ex.: `pip install -r requirements.txt`).
- Configure o `.env` com as envs descritas no `.env.example`.
- Execute:
```
python main.py
``` 

## Saída e persistência

- A aplicação cria/atualiza arquivos `last_<empresa>.json` contendo o estado da última execução, usados para detectar diferenças em execuções futuras.
- As diferenças detectadas são logadas; integre a etapa de publicação/consumo conforme a sua fila/serviço desejado.

## Dicas e solução de problemas

- Verifique `DEFAULT_URL`: deve ser realmente a base a partir da qual as páginas específicas de cada empresa são montadas. Se a busca não retorna dados, revise a URL.
- Ajuste `TIME_BETWEEN_EXECUTIONS` para controlar a frequência de consultas.
- Garanta que o container tem acesso à internet e permissões de escrita no diretório mapeado.
- Consulte os logs para entender causas de ausência de vagas ou erros de rede.
