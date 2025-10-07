# JBoard - Ashby Brazilian-Friendly Extractor

Uma aplicação Python robusta e escalável que extrai, filtra e normaliza vagas de emprego de job boards públicos do Ashby, identificando oportunidades "Brazilian Friendly" para desenvolvedores brasileiros.

## 🎯 Objetivo da Aplicação

O JBoard Ashby Extractor é um serviço batch automatizado que permite:
- Extrair vagas de job boards públicos do Ashby de empresas pré-configuradas
- Filtrar vagas usando critérios específicos "Brazilian-friendly"
- Normalizar dados das vagas (senioridade, área técnica, etc.)
- Enviar vagas processadas para uma API externa via HTTP POST
- Fornecer arquitetura escalável preparada para deploy em Azure Container Apps

Esta aplicação **não possui endpoints HTTP** e é executada automaticamente via GitHub Actions ou Docker containers em intervalos programados.

## 🚀 Funcionalidades

### Processamento de Vagas

#### **Extração de Dados**
- **Fetch HTML**: Busca páginas públicas do Ashby de empresas configuradas
- **Parse Estruturado**: Extrai dados das vagas usando regex e parsing inteligente
- **Dados Completos**: Título, empresa, localização, senioridade, descrição e requisitos
- **URLs Diretas**: Links para candidatura nas páginas originais

#### **Sistema de Filtros Brazilian-Friendly**
- **Filtro Global**: Identifica vagas com "Brazil" no título ou localização
- **Filtros por Empresa**: Lógica específica para cada empresa (LATAM, Americas, etc.)
- **Localizações Secundárias**: Busca em campos alternativos de localização
- **Critérios Flexíveis**: Adaptáveis para diferentes padrões de empresas

#### **Normalização Inteligente**
- **Padronização de Senioridade**: Junior, Pleno, Senior, etc.
- **Categorização de Áreas**: Tecnologia, Marketing, Vendas, etc.
- **Mapeamento Consistente**: Unificação de terminologias diferentes
- **Validação de Dados**: Verificação de integridade dos campos

### Empresas Suportadas

#### **Configuração Atual**
- **EightSleep**: Filtro por "LATAM" na localização
- **Supabase**: "Americas", "US time zones" e posições remotas globais
- **Deel**: "Anywhere (LATAM)" na localização
- **Resend**: "Americas" na localização
- **Commure-Athelas**: Filtros globais padrão

#### **Extensibilidade**
- **Adição Simples**: Nova empresa via configuração em `filter_jobs_service.py`
- **Filtros Customizados**: Lógica específica por empresa
- **Configuração Dinâmica**: Lista de empresas via variável de ambiente

### Características Técnicas

#### **Arquitetura Limpa**
- **Services**: Lógica de negócio centralizada para fetch, filter e normalize
- **Clients**: Clientes HTTP para Ashby e API de destino
- **Models**: Estruturas de dados e entidades bem definidas
- **Mappers**: Conversão entre diferentes tipos de dados
- **Enums**: Padronização de senioridade e áreas técnicas

#### **Recursos Avançados**
- **Brazilian Friendly**: Sistema especializado para vagas brasileiras
- **Retry Automático**: 3 tentativas com backoff exponencial
- **Timeouts Configuráveis**: Controle de tempo limite para requisições
- **Logging Estruturado**: Sistema de logs detalhado

## 🔧 Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **HTTP Client**: requests com retry automático
- **HTML Parsing**: BeautifulSoup4 + regex patterns
- **Testing**: pytest + coverage + testify
- **Containerização**: Docker
- **Cloud**: Azure Container Apps
- **CI/CD**: GitHub Actions

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.12 ou superior
- pip (gerenciador de pacotes)
- Docker (opcional)
- Git

### Instalação Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Renato556/jboard-py-ashby-extractor
   cd jboard-py-ashby-extractor
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variáveis de ambiente:**
   ```bash
   # Criar arquivo .env na raiz do projeto
   COMPANIES=commure-athelas,eightsleep,supabase,deel,resend
   API_URL=https://sua-api.com/v1
   API_TIMEOUT=30
   ASHBY_TIMEOUT=5
   DEFAULT_URL=https://jobs.ashbyhq.com/
   ```

4. **Executar aplicação:**
   ```bash
   python -m src.main
   ```

5. **Executar com logs detalhados:**
   ```bash
   PYTHONPATH=. python -m src.main
   ```

### Execução com Docker

```bash
# Build da imagem
docker build -t ashby-extractor .

# Executar container
docker run --env-file .env ashby-extractor

# Executar com compose
docker-compose up ashby-extractor
```

## 🧪 Execução de Testes

### Testes Unitários

```bash
# Executar todos os testes
python -m pytest test/ -v

# Executar testes com coverage
python -m pytest test/ -v --cov=src --cov-report=html

# Executar testes específicos
python -m pytest test/services/test_filter_jobs_service.py -v
```

### Testes por Módulo

```bash
# Testes dos services
python -m pytest test/services/ -v

# Testes dos clients
python -m pytest test/clients/ -v

# Testes dos mappers
python -m pytest test/mappers/ -v

# Testes dos models
python -m pytest test/models/ -v
```

### Cobertura de Testes

```bash
# Gerar relatório de cobertura
python -m pytest test/ -v --cov=src --cov-report=html

# Visualizar relatório no navegador
# Abrir htmlcov/index.html

# Coverage com fail under 90%
python -m pytest test/ -v --cov=src --cov-fail-under=90
```

### Estrutura de Testes

- **Cobertura Mínima**: 90%
- **Testes Unitários**: Todos os services, clients e mappers
- **Mocks**: APIs externas e dependências HTTP
- **Fixtures**: Dados de teste reutilizáveis
- **Integração**: Fluxo completo end-to-end

## 🏗️ Arquitetura e Estrutura

### Estrutura do Projeto

```
src/
├── main.py                    # Ponto de entrada da aplicação
├── clients/                   # Clientes para APIs externas
│   ├── ashby_client.py       # Cliente para job boards do Ashby
│   └── database_client.py    # Cliente HTTP para API de destino
├── services/                  # Lógica de negócio
│   ├── jobs_service.py       # Orquestração do processo
│   ├── fetch_jobs_service.py # Busca e parsing das vagas
│   ├── filter_jobs_service.py# Filtros Brazilian-friendly
│   └── normalize_jobs_service.py # Normalização de dados
├── mappers/                   # Mapeamento entre modelos
│   └── job_mapper.py         # Conversão de tipos de dados
└── models/                    # Modelos de dados
    ├── job.py                # Vaga raw do Ashby
    ├── friendly_job.py       # Vaga mapeada para filtros
    ├── normalized_job.py     # Vaga normalizada final
    └── enums/                # Enumeradores
        ├── field_enum.py     # Áreas técnicas
        └── seniority_enum.py # Níveis de senioridade
```

### Fluxo de Processamento

1. **Fetch**: Busca HTML das páginas públicas do Ashby
2. **Parse**: Extrai dados estruturados das vagas usando regex/parsing
3. **Filter**: Aplica filtros Brazilian-friendly por empresa
4. **Normalize**: Padroniza senioridade, área técnica e outros campos
5. **Send**: Envia via HTTP POST para API de destino

### Cliente HTTP Robusto

#### **Características Avançadas**
- **Retry Automático**: 3 tentativas com backoff exponencial
- **Timeouts Configuráveis**: Padrão 30s, configurável via `API_TIMEOUT`
- **Tratamento de Erros**: Logs detalhados para diagnóstico

## 🔄 Deploy e Workflows

### Azure Deploy Workflow

O projeto utiliza GitHub Actions para deploy automático no Azure Container Apps.

#### Triggers
- **Push**: Branches `main` e `master`
- **Manual**: `workflow_dispatch` para deploy sob demanda

#### Etapas do Pipeline

##### Test and Setup
- Checkout do código
- Setup Python 3.12
- Cache de dependências pip
- Instalação de requirements (`pip install -r requirements.txt`)
- Execução de testes com coverage mínimo 90%

##### Build and Deploy
- Build da imagem Docker
- Push para Azure Container Registry
- Deploy no Azure Container Apps
- Configuração automática de variáveis de ambiente
- Validação de conectividade com API CRUD

#### Variáveis de Ambiente
```yaml
# Azure
AZURE_CREDENTIALS: Credenciais de service principal
ACR_USERNAME: Username do Azure Container Registry
ACR_PASSWORD: Password do Azure Container Registry

# Aplicação
COMPANIES: "deel,supabase,eightsleep,commure-athelas,resend"
DEFAULT_URL: "https://jobs.ashbyhq.com/"
API_TIMEOUT: "30"
ASHBY_TIMEOUT: "5"
```

#### Secrets Necessários
- **AZURE_CREDENTIALS**: Credenciais de service principal
- **ACR_USERNAME**: Usuário do Container Registry
- **ACR_PASSWORD**: Senha do Container Registry

#### Características Avançadas
- **Schedule Automático**: A cada 6 horas via container interno
- **Service Discovery**: Integração automática com API CRUD
- **Logs Centralizados**: Disponíveis no Azure Portal

### 🔒 Segurança em Produção

**⚠️ IMPORTANTE**: Arquitetura de segurança enterprise implementada.

**Características de Segurança:**
- ✅ **Rede Privada**: Execução em VNet privada do Azure
- ✅ **Zero Internet Exposure**: Nenhum endpoint público direto
- ✅ **Comunicação Interna**: Acesso apenas via rede interna
- ✅ **API Gateway**: Acesso externo controlado via gateway
- ✅ **Isolamento Completo**: Máxima segurança por isolamento
- ✅ **SSL/TLS**: Criptografia em todas as comunicações

### CI/CD Pipeline

**Deploy Automático:**
```bash
# Build e push da imagem
docker build -t ashby-extractor .
docker tag ashby-extractor your-registry.azurecr.io/ashby-extractor
docker push your-registry.azurecr.io/ashby-extractor
```

## 🔍 Sistema de Filtros Detalhado

### Como Adicionar Nova Empresa

1. **Edite o arquivo:**
   ```python
   # src/services/filter_jobs_service.py
   ```

2. **Adicione função específica:**
   ```python
   def _[empresa]_filter(job_listing: FriendlyJob) -> bool:
       # Implemente lógica específica
       return True
   ```

3. **Adicione condição:**
   ```python
   # Em _filter_by_company()
   elif company == "nova-empresa":
       return self._nova_empresa_filter(job_listing)
   ```

### Filtros Implementados

#### **Filtro Global** (aplicado a todas as empresas)
- ✅ **Localização Principal**: "Brazil" no título ou localização
- ✅ **Localizações Secundárias**: "Brazil" em campos alternativos

#### **Filtros Específicos por Empresa**
- **EightSleep**: "LATAM" na localização
- **Supabase**: "Americas", "US time zones", posições remotas globais
- **Deel**: "Anywhere (LATAM)" na localização
- **Resend**: "Americas" na localização

## 🤝 Colaboração e Desenvolvimento

### Padrões de Código
- **Python**: PEP 8
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- **Testes**: Cobertura mínima de 90%
- **Logs**: Usar `logging` module, não `print()`

### Contribuindo
1. Fork o projeto
2. Crie uma branch feature (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add some amazing-feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

### Code Review
- Todos os PRs devem passar nos testes
- Cobertura mínima de 80%
- Aprovação de pelo menos 1 reviewer
- Validação automática do CI/CD

## 📄 Licenciamento

### Licença MIT

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

**Resumo da Licença:**
- ✅ Uso comercial
- ✅ Modificação
- ✅ Distribuição
- ✅ Uso privado
- ❌ Responsabilidade
- ❌ Garantia

### Direitos de Uso
- Permitido uso em projetos comerciais
- Permitida modificação do código
- Créditos aos autores originais apreciados
- Não há garantias de funcionamento
