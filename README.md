# ⚡ SISTEMA DA EVOLUÇÃO

> Transforme sua vida real em uma experiência RPG de desenvolvimento pessoal.

---

## 🗂️ Estrutura

```
/SistemaDaEvolucao
├── index.html          ← Abrir no navegador
├── style.css           ← Visual dark neon RPG
├── script.js           ← Lógica do frontend
│
├── backend/
│   ├── main.py         ← Servidor Flask (iniciar aqui)
│   ├── player.py       ← Modelo do Jogador
│   ├── missions.py     ← Sistema de missões
│   ├── achievements.py ← 100+ conquistas
│   ├── system_ai.py    ← IA do Sistema
│   ├── ranking.py      ← Ranks e progressão
│   ├── save_manager.py ← Salvar/carregar dados
│   └── requirements.txt
│
└── data/
    ├── save.json       ← Gerado automaticamente
    └── legacy.json     ← Gerado automaticamente
```

---

## 🚀 Como Iniciar

### 1. Instalar dependências

```bash
cd SistemaDaEvolucao/backend
pip install -r requirements.txt
```

### 2. Iniciar o backend

```bash
python main.py
```

O servidor sobe em: `http://localhost:5000`

### 3. Abrir o frontend

Abra o arquivo `index.html` no navegador.

> ⚠️ Se abrir com `file://`, pode haver bloqueio de CORS.
> Use uma extensão como **Live Server** no VS Code, ou rode:

```bash
# Python 3
python -m http.server 8080
# Então acesse: http://localhost:8080
```

---

## 🎮 Funcionalidades

| Módulo         | Descrição                                      |
|----------------|------------------------------------------------|
| Dashboard      | XP, Rank, Streak, Atributos em tempo real      |
| Missões        | Diárias, Semanais, Mensais, Especiais, Secretas|
| Conquistas     | 100+ conquistas por categoria                  |
| Rankings       | D → Ω com ranks secretos e especiais           |
| Títulos        | 50+ títulos + secretos                         |
| Legado         | Toda a jornada registrada                      |
| NO FAP         | Módulo opcional de disciplina mental           |
| Relatórios     | Diário, Semanal, Mensal                        |
| IA do Sistema  | Mensagens dinâmicas e análise de desempenho    |
| Auto-Save      | Backup automático em JSON                      |

---

## 🔮 Atributos

| Atributo      | Escala  |
|---------------|---------|
| Força         | 0 – 100 |
| Resistência   | 0 – 100 |
| Inteligência  | 0 – 100 |
| Conhecimento  | 0 – 100 |
| Disciplina    | 0 – 100 |
| Foco          | 0 – 100 |
| Saúde         | 0 – 100 |
| Energia       | 0 – 100 |
| Carisma       | 0 – 100 |
| Aparência     | 0 – 100 |

---

## 📡 API Endpoints Principais

| Método | Rota                      | Descrição                     |
|--------|---------------------------|-------------------------------|
| GET    | /api/player               | Dados do jogador              |
| POST   | /api/player/create        | Criar novo jogador            |
| GET    | /api/missions?type=daily  | Listar missões                |
| POST   | /api/missions/complete    | Completar missão              |
| GET    | /api/achievements         | Listar conquistas             |
| GET    | /api/rankings/info        | Info de todos os ranks        |
| GET    | /api/legacy               | Dados de legado               |
| POST   | /api/nofap/start          | Ativar módulo NO FAP          |
| POST   | /api/nofap/fall           | Registrar queda               |
| GET    | /api/reports/daily        | Relatório diário              |
| GET    | /api/system/message       | Mensagens da IA               |

---

## 🛡️ Desenvolvido por

**Sistema da Evolução** — Feito para quem leva a sério a própria evolução.

> "A disciplina hoje é a liberdade de amanhã."
