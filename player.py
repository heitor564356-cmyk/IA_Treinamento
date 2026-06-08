"""
Sistema da Evolução - Player Module
Gerencia todos os dados, atributos e progressão do Jogador.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import datetime


# ─────────────────────────────────────────────
#  RANKS
# ─────────────────────────────────────────────
RANKS = [
    "D", "D+",
    "C-", "C", "C+",
    "B-", "B", "B+",
    "A-", "A", "A+",
    "S-", "S", "S+",
    "SS", "SS+",
    "SSS",
    "Z", "Z+", "Z++",   # Secretos
    "EX",               # Especial
    "Ω",                # Ômega — Especial máximo
]

RANK_THRESHOLDS: dict[str, int] = {
    "D":    0,
    "D+":   500,
    "C-":   1200,
    "C":    2500,
    "C+":   4500,
    "B-":   7000,
    "B":    10000,
    "B+":   14000,
    "A-":   19000,
    "A":    25000,
    "A+":   33000,
    "S-":   43000,
    "S":    55000,
    "S+":   70000,
    "SS":   90000,
    "SS+":  115000,
    "SSS":  150000,
    "Z":    200000,
    "Z+":   275000,
    "Z++":  375000,
    "EX":   500000,
    "Ω":    750000,
}

# ─────────────────────────────────────────────
#  TÍTULOS
# ─────────────────────────────────────────────
ALL_TITLES: list[dict] = [
    # Básicos
    {"id": "iniciante",         "name": "Iniciante",              "desc": "Começou a jornada.",              "secret": False},
    {"id": "aprendiz",          "name": "Aprendiz",               "desc": "5 missões completas.",            "secret": False},
    {"id": "persistente",       "name": "Persistente",            "desc": "7 dias consecutivos.",            "secret": False},
    {"id": "disciplinado",      "name": "Disciplinado",           "desc": "Disciplina >= 30.",               "secret": False},
    {"id": "estudioso",         "name": "Estudioso",              "desc": "10 missões de estudo.",           "secret": False},
    {"id": "focado",            "name": "Focado",                 "desc": "Foco >= 30.",                     "secret": False},
    {"id": "organizado",        "name": "Organizado",             "desc": "5 missões de organização.",       "secret": False},
    {"id": "lutador",           "name": "Lutador",                "desc": "10 missões físicas.",             "secret": False},
    {"id": "guerreiro",         "name": "Guerreiro",              "desc": "Rank B ou superior.",             "secret": False},
    {"id": "sobrevivente",      "name": "Sobrevivente",           "desc": "30 dias no sistema.",             "secret": False},
    {"id": "determinado",       "name": "Determinado",            "desc": "50 missões completas.",           "secret": False},
    {"id": "estrategista",      "name": "Estrategista",           "desc": "Inteligência >= 40.",             "secret": False},
    {"id": "guardiao",          "name": "Guardião",               "desc": "Saúde >= 40.",                    "secret": False},
    {"id": "conquistador",      "name": "Conquistador",           "desc": "100 missões completas.",          "secret": False},
    {"id": "mestre_disciplina", "name": "Mestre da Disciplina",   "desc": "Disciplina >= 70.",               "secret": False},
    {"id": "mestre_mente",      "name": "Mestre da Mente",        "desc": "Inteligência >= 70.",             "secret": False},
    {"id": "mestre_corpo",      "name": "Mestre do Corpo",        "desc": "Força >= 70.",                    "secret": False},
    {"id": "lenda_viva",        "name": "Lenda Viva",             "desc": "365 dias no sistema.",            "secret": False},
    {"id": "ascendente",        "name": "Ascendente",             "desc": "Rank S ou superior.",             "secret": False},
    {"id": "imperador",         "name": "Imperador da Disciplina","desc": "Disciplina >= 90.",               "secret": False},
    {"id": "madrugador",        "name": "Madrugador",             "desc": "5 missões antes das 7h.",         "secret": False},
    {"id": "noturno",           "name": "Noturno",                "desc": "5 missões após as 22h.",          "secret": False},
    {"id": "atleta",            "name": "Atleta",                 "desc": "Resistência >= 50.",              "secret": False},
    {"id": "academico",         "name": "Acadêmico",              "desc": "Conhecimento >= 50.",             "secret": False},
    {"id": "saudavel",          "name": "Saudável",               "desc": "Saúde >= 60.",                    "secret": False},
    {"id": "energizado",        "name": "Energizado",             "desc": "Energia >= 60.",                  "secret": False},
    {"id": "carismatico",       "name": "Carismático",            "desc": "Carisma >= 50.",                  "secret": False},
    {"id": "belo",              "name": "Belo",                   "desc": "Aparência >= 50.",                "secret": False},
    {"id": "incansavel",        "name": "Incansável",             "desc": "14 dias consecutivos.",           "secret": False},
    {"id": "inabalavel",        "name": "Inabalável",             "desc": "30 dias consecutivos.",           "secret": False},
    {"id": "monolito",          "name": "Monólito",               "desc": "50 dias consecutivos.",           "secret": False},
    {"id": "eterno",            "name": "Eterno",                 "desc": "100 dias consecutivos.",          "secret": False},
    {"id": "vencedor",          "name": "Vencedor",               "desc": "Level 10 alcançado.",             "secret": False},
    {"id": "veterano",          "name": "Veterano",               "desc": "Level 20 alcançado.",             "secret": False},
    {"id": "elite",             "name": "Elite",                  "desc": "Level 30 alcançado.",             "secret": False},
    {"id": "lendario",          "name": "Lendário",               "desc": "Level 50 alcançado.",             "secret": False},
    {"id": "perfeicionista",    "name": "Perfeccionista",         "desc": "Todos atributos >= 50.",          "secret": False},
    {"id": "harmonioso",        "name": "Harmonioso",             "desc": "Todos atributos >= 60.",          "secret": False},
    {"id": "completo",          "name": "Ser Completo",           "desc": "Todos atributos >= 70.",          "secret": False},
    {"id": "treinador",         "name": "Treinador",              "desc": "200 missões físicas.",            "secret": False},
    {"id": "scholar",           "name": "Scholar",                "desc": "200 missões de estudo.",          "secret": False},
    {"id": "monge",             "name": "Monge",                  "desc": "200 missões mentais.",            "secret": False},
    {"id": "cuidador",          "name": "Cuidador",               "desc": "200 missões de autocuidado.",     "secret": False},
    {"id": "pioneiro",          "name": "Pioneiro",               "desc": "Primeiro login.",                 "secret": False},
    {"id": "consistente",       "name": "Consistente",            "desc": "21 dias consecutivos.",           "secret": False},
    {"id": "resiliente",        "name": "Resiliente",             "desc": "Voltar após 3+ dias sem login.",  "secret": False},
    {"id": "crescente",         "name": "Crescente",              "desc": "5 level ups em uma semana.",      "secret": False},
    {"id": "imparavel",         "name": "Imparável",              "desc": "Rank A+ alcançado.",              "secret": False},
    {"id": "lider",             "name": "Líder",                  "desc": "Carisma >= 70.",                  "secret": False},
    {"id": "sabio",             "name": "Sábio",                  "desc": "Conhecimento >= 80.",             "secret": False},
    {"id": "titan",             "name": "Titã",                   "desc": "Força + Resistência >= 150.",     "secret": False},

    # Secretos
    {"id": "monarca",           "name": "Monarca",                "desc": "???",                             "secret": True},
    {"id": "soberano",          "name": "Soberano",               "desc": "???",                             "secret": True},
    {"id": "ultimo_heroi",      "name": "Último Herói",           "desc": "???",                             "secret": True},
    {"id": "filho_evolucao",    "name": "Filho da Evolução",      "desc": "???",                             "secret": True},
    {"id": "ascendido",         "name": "Ascendido",              "desc": "???",                             "secret": True},
    {"id": "portador_destino",  "name": "Portador do Destino",    "desc": "???",                             "secret": True},
    {"id": "rei_constancia",    "name": "Rei da Constância",      "desc": "???",                             "secret": True},
    {"id": "alem_limite",       "name": "Além do Limite",         "desc": "???",                             "secret": True},
    {"id": "sombra_eterna",     "name": "Sombra Eterna",          "desc": "???",                             "secret": True},
    {"id": "despertar",         "name": "O Despertar",            "desc": "???",                             "secret": True},
]

# ─────────────────────────────────────────────
#  DATACLASSES
# ─────────────────────────────────────────────

@dataclass
class Attributes:
    forca: float = 0.0
    resistencia: float = 0.0
    inteligencia: float = 0.0
    conhecimento: float = 0.0
    disciplina: float = 0.0
    foco: float = 0.0
    saude: float = 0.0
    energia: float = 0.0
    carisma: float = 0.0
    aparencia: float = 0.0

    def to_dict(self) -> dict:
        return {
            "forca": self.forca,
            "resistencia": self.resistencia,
            "inteligencia": self.inteligencia,
            "conhecimento": self.conhecimento,
            "disciplina": self.disciplina,
            "foco": self.foco,
            "saude": self.saude,
            "energia": self.energia,
            "carisma": self.carisma,
            "aparencia": self.aparencia,
        }

    @staticmethod
    def from_dict(d: dict) -> "Attributes":
        a = Attributes()
        for k, v in d.items():
            if hasattr(a, k):
                setattr(a, k, float(v))
        return a

    def average(self) -> float:
        vals = list(self.to_dict().values())
        return sum(vals) / len(vals)

    def total(self) -> float:
        return sum(self.to_dict().values())


@dataclass
class NoFapTracker:
    active: bool = False
    clean_days: int = 0
    record: int = 0
    start_date: Optional[str] = None
    history: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "active": self.active,
            "clean_days": self.clean_days,
            "record": self.record,
            "start_date": self.start_date,
            "history": self.history,
        }

    @staticmethod
    def from_dict(d: dict) -> "NoFapTracker":
        t = NoFapTracker()
        t.active = d.get("active", False)
        t.clean_days = d.get("clean_days", 0)
        t.record = d.get("record", 0)
        t.start_date = d.get("start_date")
        t.history = d.get("history", [])
        return t


@dataclass
class MissionStats:
    total: int = 0
    physical: int = 0
    study: int = 0
    selfcare: int = 0
    mental: int = 0
    daily_completed_today: list[str] = field(default_factory=list)
    weekly_completed: list[str] = field(default_factory=list)
    monthly_completed: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "physical": self.physical,
            "study": self.study,
            "selfcare": self.selfcare,
            "mental": self.mental,
            "daily_completed_today": self.daily_completed_today,
            "weekly_completed": self.weekly_completed,
            "monthly_completed": self.monthly_completed,
        }

    @staticmethod
    def from_dict(d: dict) -> "MissionStats":
        m = MissionStats()
        m.total = d.get("total", 0)
        m.physical = d.get("physical", 0)
        m.study = d.get("study", 0)
        m.selfcare = d.get("selfcare", 0)
        m.mental = d.get("mental", 0)
        m.daily_completed_today = d.get("daily_completed_today", [])
        m.weekly_completed = d.get("weekly_completed", [])
        m.monthly_completed = d.get("monthly_completed", [])
        return m


@dataclass
class DayTracker:
    creation_date: str = ""
    total_days: int = 0
    current_streak: int = 0
    best_streak: int = 0
    last_login: Optional[str] = None
    study_hours: float = 0.0
    workouts_done: int = 0

    def to_dict(self) -> dict:
        return {
            "creation_date": self.creation_date,
            "total_days": self.total_days,
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "last_login": self.last_login,
            "study_hours": self.study_hours,
            "workouts_done": self.workouts_done,
        }

    @staticmethod
    def from_dict(d: dict) -> "DayTracker":
        t = DayTracker()
        t.creation_date = d.get("creation_date", "")
        t.total_days = d.get("total_days", 0)
        t.current_streak = d.get("current_streak", 0)
        t.best_streak = d.get("best_streak", 0)
        t.last_login = d.get("last_login")
        t.study_hours = d.get("study_hours", 0.0)
        t.workouts_done = d.get("workouts_done", 0)
        return t


@dataclass
class Player:
    # Identidade
    name: str = ""
    age: int = 0
    main_objective: str = ""

    # Progressão
    level: int = 1
    xp: int = 0
    xp_next: int = 500
    attribute_points: int = 0
    gold: int = 0
    rank: str = "D"
    title: str = "Iniciante"
    unlocked_titles: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)

    # Atributos
    attributes: Attributes = field(default_factory=Attributes)

    # Rastreamento
    day_tracker: DayTracker = field(default_factory=DayTracker)
    missions: MissionStats = field(default_factory=MissionStats)
    nofap: NoFapTracker = field(default_factory=NoFapTracker)

    # Histórico
    rank_history: list[dict] = field(default_factory=list)
    level_history: list[dict] = field(default_factory=list)
    attribute_history: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "age": self.age,
            "main_objective": self.main_objective,
            "level": self.level,
            "xp": self.xp,
            "xp_next": self.xp_next,
            "attribute_points": self.attribute_points,
            "gold": self.gold,
            "rank": self.rank,
            "title": self.title,
            "unlocked_titles": self.unlocked_titles,
            "achievements": self.achievements,
            "attributes": self.attributes.to_dict(),
            "day_tracker": self.day_tracker.to_dict(),
            "missions": self.missions.to_dict(),
            "nofap": self.nofap.to_dict(),
            "rank_history": self.rank_history,
            "level_history": self.level_history,
            "attribute_history": self.attribute_history,
        }

    @staticmethod
    def from_dict(d: dict) -> "Player":
        p = Player()
        p.name = d.get("name", "")
        p.age = d.get("age", 0)
        p.main_objective = d.get("main_objective", "")
        p.level = d.get("level", 1)
        p.xp = d.get("xp", 0)
        p.xp_next = d.get("xp_next", 500)
        p.attribute_points = d.get("attribute_points", 0)
        p.gold = d.get("gold", 0)
        p.rank = d.get("rank", "D")
        p.title = d.get("title", "Iniciante")
        p.unlocked_titles = d.get("unlocked_titles", [])
        p.achievements = d.get("achievements", [])
        p.attributes = Attributes.from_dict(d.get("attributes", {}))
        p.day_tracker = DayTracker.from_dict(d.get("day_tracker", {}))
        p.missions = MissionStats.from_dict(d.get("missions", {}))
        p.nofap = NoFapTracker.from_dict(d.get("nofap", {}))
        p.rank_history = d.get("rank_history", [])
        p.level_history = d.get("level_history", [])
        p.attribute_history = d.get("attribute_history", [])
        return p


# ─────────────────────────────────────────────
#  HELPER: XP necessário para o próximo nível
# ─────────────────────────────────────────────

def xp_for_next_level(level: int) -> int:
    """XP necessário para passar do nível atual para o próximo."""
    base = 500
    return int(base * (1.35 ** (level - 1)))


def calculate_rank(xp: int) -> str:
    """Calcula o rank baseado no XP total acumulado."""
    current_rank = "D"
    for rank, threshold in RANK_THRESHOLDS.items():
        if xp >= threshold:
            current_rank = rank
    return current_rank
