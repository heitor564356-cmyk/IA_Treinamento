"""
Sistema da Evolução - Missions Module
Define todas as missões: diárias, semanais, mensais, especiais e secretas.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import datetime
import random


# ─────────────────────────────────────────────
#  CATEGORIAS
# ─────────────────────────────────────────────

CATEGORY_PHYSICAL = "physical"
CATEGORY_STUDY    = "study"
CATEGORY_SELFCARE = "selfcare"
CATEGORY_MENTAL   = "mental"

CATEGORY_LABELS = {
    CATEGORY_PHYSICAL: "⚔️ Físico",
    CATEGORY_STUDY:    "📚 Estudo",
    CATEGORY_SELFCARE: "🌿 Autocuidado",
    CATEGORY_MENTAL:   "🧠 Mental",
}

# ─────────────────────────────────────────────
#  DATACLASS
# ─────────────────────────────────────────────

@dataclass
class Mission:
    id: str
    title: str
    description: str
    category: str
    mission_type: str          # daily | weekly | monthly | special | secret
    xp_reward: int
    gold_reward: int
    attribute_reward: dict     # {"forca": 1.5, ...}
    difficulty: str            # easy | medium | hard | extreme
    completed: bool = False
    active: bool = True
    secret: bool = False
    unlock_condition: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "mission_type": self.mission_type,
            "xp_reward": self.xp_reward,
            "gold_reward": self.gold_reward,
            "attribute_reward": self.attribute_reward,
            "difficulty": self.difficulty,
            "completed": self.completed,
            "active": self.active,
            "secret": self.secret,
            "unlock_condition": self.unlock_condition,
        }

    @staticmethod
    def from_dict(d: dict) -> "Mission":
        return Mission(
            id=d["id"],
            title=d["title"],
            description=d["description"],
            category=d["category"],
            mission_type=d["mission_type"],
            xp_reward=d["xp_reward"],
            gold_reward=d["gold_reward"],
            attribute_reward=d.get("attribute_reward", {}),
            difficulty=d["difficulty"],
            completed=d.get("completed", False),
            active=d.get("active", True),
            secret=d.get("secret", False),
            unlock_condition=d.get("unlock_condition", ""),
        )


# ─────────────────────────────────────────────
#  BANCO DE MISSÕES
# ─────────────────────────────────────────────

MISSION_POOL: list[dict] = [

    # ── FÍSICAS DIÁRIAS ──────────────────────
    {"id": "daily_push_20",    "title": "20 Flexões",                "description": "Complete 20 flexões hoje.",                    "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 80,   "gold_reward": 10, "attribute_reward": {"forca": 1.0, "resistencia": 0.5},       "difficulty": "easy"},
    {"id": "daily_push_50",    "title": "50 Flexões",                "description": "Complete 50 flexões hoje.",                    "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 150,  "gold_reward": 20, "attribute_reward": {"forca": 2.0, "resistencia": 1.0},       "difficulty": "medium"},
    {"id": "daily_run_2km",    "title": "Corrida 2 km",              "description": "Corra pelo menos 2 km.",                       "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 120,  "gold_reward": 15, "attribute_reward": {"resistencia": 2.0, "saude": 1.0},       "difficulty": "easy"},
    {"id": "daily_run_5km",    "title": "Corrida 5 km",              "description": "Corra pelo menos 5 km.",                       "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 250,  "gold_reward": 30, "attribute_reward": {"resistencia": 3.0, "saude": 1.5},       "difficulty": "medium"},
    {"id": "daily_walk_30",    "title": "Caminhada 30 min",          "description": "Caminhe por 30 minutos.",                      "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 70,   "gold_reward": 8,  "attribute_reward": {"saude": 1.0, "energia": 0.5},           "difficulty": "easy"},
    {"id": "daily_stretch",    "title": "Alongamento Completo",      "description": "Faça 15 minutos de alongamento.",              "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 60,   "gold_reward": 8,  "attribute_reward": {"saude": 0.8, "aparencia": 0.3},         "difficulty": "easy"},
    {"id": "daily_strength",   "title": "Treino de Força",           "description": "Complete um treino de força completo.",        "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 200,  "gold_reward": 25, "attribute_reward": {"forca": 2.5, "resistencia": 1.5},       "difficulty": "medium"},
    {"id": "daily_squat_50",   "title": "50 Agachamentos",           "description": "Complete 50 agachamentos hoje.",               "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 100,  "gold_reward": 12, "attribute_reward": {"forca": 1.5, "resistencia": 0.8},       "difficulty": "easy"},
    {"id": "daily_abs",        "title": "Treino Abdominal",          "description": "30 minutos focados em abdômen.",               "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 110,  "gold_reward": 15, "attribute_reward": {"forca": 1.2, "aparencia": 0.8},         "difficulty": "easy"},
    {"id": "daily_plank",      "title": "Prancha 3 min",             "description": "Sustente a prancha por 3 minutos total.",      "category": CATEGORY_PHYSICAL, "mission_type": "daily",   "xp_reward": 90,   "gold_reward": 10, "attribute_reward": {"forca": 1.0, "disciplina": 0.5},        "difficulty": "easy"},

    # ── ESTUDO DIÁRIAS ───────────────────────
    {"id": "daily_read_30",    "title": "Leitura 30 min",            "description": "Leia por 30 minutos.",                         "category": CATEGORY_STUDY,    "mission_type": "daily",   "xp_reward": 100,  "gold_reward": 12, "attribute_reward": {"inteligencia": 1.5, "conhecimento": 1.0},"difficulty": "easy"},
    {"id": "daily_read_1h",    "title": "Leitura 1 hora",            "description": "Leia por 1 hora ininterrupta.",                "category": CATEGORY_STUDY,    "mission_type": "daily",   "xp_reward": 180,  "gold_reward": 22, "attribute_reward": {"inteligencia": 2.5, "conhecimento": 2.0},"difficulty": "medium"},
    {"id": "daily_exercises",  "title": "Exercícios Acadêmicos",     "description": "Complete exercícios de estudo.",               "category": CATEGORY_STUDY,    "mission_type": "daily",   "xp_reward": 130,  "gold_reward": 15, "attribute_reward": {"inteligencia": 2.0, "disciplina": 0.8}, "difficulty": "easy"},
    {"id": "daily_code_30",    "title": "Programar 30 min",          "description": "Programe por 30 minutos.",                     "category": CATEGORY_STUDY,    "mission_type": "daily",   "xp_reward": 150,  "gold_reward": 18, "attribute_reward": {"inteligencia": 2.0, "conhecimento": 1.5},"difficulty": "easy"},
    {"id": "daily_code_2h",    "title": "Programar 2 horas",         "description": "Programe por 2 horas focadas.",                "category": CATEGORY_STUDY,    "mission_type": "daily",   "xp_reward": 280,  "gold_reward": 35, "attribute_reward": {"inteligencia": 3.0, "conhecimento": 2.5},"difficulty": "medium"},
    {"id": "daily_review",     "title": "Revisão de Conteúdo",       "description": "Revise o conteúdo estudado recentemente.",     "category": CATEGORY_STUDY,    "mission_type": "daily",   "xp_reward": 110,  "gold_reward": 13, "attribute_reward": {"conhecimento": 2.0, "inteligencia": 1.0},"difficulty": "easy"},
    {"id": "daily_flashcards", "title": "20 Flashcards",             "description": "Estude 20 flashcards.",                        "category": CATEGORY_STUDY,    "mission_type": "daily",   "xp_reward": 90,   "gold_reward": 10, "attribute_reward": {"conhecimento": 1.5, "foco": 0.5},       "difficulty": "easy"},
    {"id": "daily_notes",      "title": "Fazer Anotações",           "description": "Anote os principais pontos estudados hoje.",   "category": CATEGORY_STUDY,    "mission_type": "daily",   "xp_reward": 70,   "gold_reward": 8,  "attribute_reward": {"conhecimento": 1.0, "organização": 0.8}, "difficulty": "easy"},

    # ── AUTOCUIDADO DIÁRIAS ──────────────────
    {"id": "daily_skincare",   "title": "Rotina Skincare",           "description": "Complete sua rotina de skincare.",             "category": CATEGORY_SELFCARE, "mission_type": "daily",   "xp_reward": 70,   "gold_reward": 8,  "attribute_reward": {"aparencia": 1.2, "saude": 0.5},         "difficulty": "easy"},
    {"id": "daily_water_3l",   "title": "Beber 3L de Água",          "description": "Beba pelo menos 3 litros de água.",            "category": CATEGORY_SELFCARE, "mission_type": "daily",   "xp_reward": 80,   "gold_reward": 10, "attribute_reward": {"saude": 1.5, "energia": 0.8},           "difficulty": "easy"},
    {"id": "daily_sleep_early","title": "Dormir antes das 23h",      "description": "Durma antes das 23 horas.",                    "category": CATEGORY_SELFCARE, "mission_type": "daily",   "xp_reward": 90,   "gold_reward": 10, "attribute_reward": {"saude": 1.5, "energia": 1.5},           "difficulty": "easy"},
    {"id": "daily_room",       "title": "Organizar Quarto",          "description": "Mantenha seu quarto organizado hoje.",         "category": CATEGORY_SELFCARE, "mission_type": "daily",   "xp_reward": 60,   "gold_reward": 7,  "attribute_reward": {"disciplina": 0.8, "aparencia": 0.3},    "difficulty": "easy"},
    {"id": "daily_no_junk",    "title": "Sem Junk Food",             "description": "Evite alimentos ultraprocessados hoje.",       "category": CATEGORY_SELFCARE, "mission_type": "daily",   "xp_reward": 80,   "gold_reward": 10, "attribute_reward": {"saude": 1.5, "disciplina": 1.0},        "difficulty": "easy"},
    {"id": "daily_hygiene",    "title": "Higiene Completa",          "description": "Complete sua rotina de higiene.",              "category": CATEGORY_SELFCARE, "mission_type": "daily",   "xp_reward": 50,   "gold_reward": 5,  "attribute_reward": {"aparencia": 0.8, "saude": 0.5},         "difficulty": "easy"},

    # ── MENTAIS DIÁRIAS ──────────────────────
    {"id": "daily_plan",       "title": "Planejamento Diário",       "description": "Planeje suas atividades do dia.",              "category": CATEGORY_MENTAL,   "mission_type": "daily",   "xp_reward": 80,   "gold_reward": 10, "attribute_reward": {"disciplina": 1.0, "foco": 1.0},         "difficulty": "easy"},
    {"id": "daily_journal",    "title": "Escrever no Diário",        "description": "Escreva no diário por 10 minutos.",            "category": CATEGORY_MENTAL,   "mission_type": "daily",   "xp_reward": 70,   "gold_reward": 8,  "attribute_reward": {"inteligencia": 0.8, "saude": 0.5},      "difficulty": "easy"},
    {"id": "daily_meditation", "title": "Meditação 10 min",          "description": "Medite por 10 minutos em silêncio.",           "category": CATEGORY_MENTAL,   "mission_type": "daily",   "xp_reward": 90,   "gold_reward": 10, "attribute_reward": {"foco": 1.5, "disciplina": 1.0},         "difficulty": "easy"},
    {"id": "daily_no_phone_1h","title": "1h Sem Celular",            "description": "Fique 1 hora sem olhar o celular.",            "category": CATEGORY_MENTAL,   "mission_type": "daily",   "xp_reward": 100,  "gold_reward": 12, "attribute_reward": {"foco": 2.0, "disciplina": 1.5},         "difficulty": "medium"},
    {"id": "daily_gratitude",  "title": "Lista de Gratidão",         "description": "Escreva 5 coisas pelas quais é grato.",       "category": CATEGORY_MENTAL,   "mission_type": "daily",   "xp_reward": 60,   "gold_reward": 7,  "attribute_reward": {"saude": 0.5, "energia": 0.8},           "difficulty": "easy"},
    {"id": "daily_visualize",  "title": "Visualização",              "description": "Visualize seus objetivos por 5 minutos.",      "category": CATEGORY_MENTAL,   "mission_type": "daily",   "xp_reward": 65,   "gold_reward": 8,  "attribute_reward": {"foco": 1.0, "disciplina": 0.8},         "difficulty": "easy"},

    # ── SEMANAIS ─────────────────────────────
    {"id": "weekly_workout_5", "title": "5 Treinos na Semana",       "description": "Complete 5 treinos nesta semana.",             "category": CATEGORY_PHYSICAL, "mission_type": "weekly",  "xp_reward": 500,  "gold_reward": 60, "attribute_reward": {"forca": 3.0, "resistencia": 2.5},       "difficulty": "medium"},
    {"id": "weekly_run_20km",  "title": "20 km de Corrida",          "description": "Acumule 20 km rodados na semana.",             "category": CATEGORY_PHYSICAL, "mission_type": "weekly",  "xp_reward": 600,  "gold_reward": 70, "attribute_reward": {"resistencia": 4.0, "saude": 2.0},       "difficulty": "hard"},
    {"id": "weekly_study_10h", "title": "10h de Estudo",             "description": "Estude pelo menos 10 horas na semana.",        "category": CATEGORY_STUDY,    "mission_type": "weekly",  "xp_reward": 700,  "gold_reward": 80, "attribute_reward": {"inteligencia": 4.0, "conhecimento": 3.0},"difficulty": "hard"},
    {"id": "weekly_no_junk",   "title": "Semana Sem Junk Food",      "description": "Evite junk food por 7 dias.",                  "category": CATEGORY_SELFCARE, "mission_type": "weekly",  "xp_reward": 450,  "gold_reward": 55, "attribute_reward": {"saude": 3.0, "disciplina": 2.5},        "difficulty": "medium"},
    {"id": "weekly_journal_7", "title": "7 Entradas no Diário",      "description": "Escreva no diário todos os dias da semana.",   "category": CATEGORY_MENTAL,   "mission_type": "weekly",  "xp_reward": 400,  "gold_reward": 50, "attribute_reward": {"disciplina": 2.0, "foco": 2.0},         "difficulty": "medium"},
    {"id": "weekly_meditation","title": "7 Meditações",              "description": "Medite todos os dias da semana.",              "category": CATEGORY_MENTAL,   "mission_type": "weekly",  "xp_reward": 500,  "gold_reward": 60, "attribute_reward": {"foco": 3.0, "saude": 2.0},              "difficulty": "medium"},
    {"id": "weekly_book",      "title": "Avançar no Livro",          "description": "Leia pelo menos 50 páginas na semana.",        "category": CATEGORY_STUDY,    "mission_type": "weekly",  "xp_reward": 350,  "gold_reward": 45, "attribute_reward": {"conhecimento": 2.5, "inteligencia": 2.0},"difficulty": "medium"},

    # ── MENSAIS ──────────────────────────────
    {"id": "monthly_30_streak","title": "30 Dias Consecutivos",      "description": "Mantenha 30 dias de streak.",                 "category": CATEGORY_MENTAL,   "mission_type": "monthly", "xp_reward": 3000, "gold_reward": 300,"attribute_reward": {"disciplina": 8.0, "foco": 6.0},         "difficulty": "hard"},
    {"id": "monthly_book",     "title": "Terminar um Livro",         "description": "Complete a leitura de um livro no mês.",      "category": CATEGORY_STUDY,    "mission_type": "monthly", "xp_reward": 2000, "gold_reward": 200,"attribute_reward": {"conhecimento": 6.0, "inteligencia": 5.0},"difficulty": "medium"},
    {"id": "monthly_fitness",  "title": "20 Treinos no Mês",         "description": "Complete 20 treinos em um mês.",              "category": CATEGORY_PHYSICAL, "mission_type": "monthly", "xp_reward": 2500, "gold_reward": 250,"attribute_reward": {"forca": 6.0, "resistencia": 5.0},       "difficulty": "hard"},
    {"id": "monthly_study_40h","title": "40 Horas de Estudo",        "description": "Estude 40 horas em um mês.",                  "category": CATEGORY_STUDY,    "mission_type": "monthly", "xp_reward": 3500, "gold_reward": 350,"attribute_reward": {"inteligencia": 8.0, "conhecimento": 7.0},"difficulty": "extreme"},
    {"id": "monthly_transform","title": "Transformação Mensal",      "description": "Melhore pelo menos 3 atributos em +5 pontos.","category": CATEGORY_MENTAL,   "mission_type": "monthly", "xp_reward": 4000, "gold_reward": 400,"attribute_reward": {"disciplina": 5.0, "foco": 5.0},         "difficulty": "extreme"},

    # ── ESPECIAIS ────────────────────────────
    {"id": "special_first",    "title": "Primeiro Passo",            "description": "Complete sua primeira missão.",               "category": CATEGORY_MENTAL,   "mission_type": "special", "xp_reward": 200,  "gold_reward": 25, "attribute_reward": {"disciplina": 1.0},                      "difficulty": "easy"},
    {"id": "special_10days",   "title": "10 Dias de Jornada",        "description": "10 dias desde o início.",                     "category": CATEGORY_MENTAL,   "mission_type": "special", "xp_reward": 500,  "gold_reward": 60, "attribute_reward": {"disciplina": 2.0, "foco": 1.5},         "difficulty": "easy"},
    {"id": "special_30days",   "title": "30 Dias de Jornada",        "description": "30 dias desde o início.",                     "category": CATEGORY_MENTAL,   "mission_type": "special", "xp_reward": 1500, "gold_reward": 150,"attribute_reward": {"disciplina": 4.0, "foco": 3.0},         "difficulty": "medium"},
    {"id": "special_100days",  "title": "100 Dias de Jornada",       "description": "100 dias desde o início.",                    "category": CATEGORY_MENTAL,   "mission_type": "special", "xp_reward": 5000, "gold_reward": 500,"attribute_reward": {"disciplina": 8.0, "foco": 6.0},         "difficulty": "hard"},
    {"id": "special_365days",  "title": "Um Ano de Evolução",        "description": "365 dias desde o início.",                    "category": CATEGORY_MENTAL,   "mission_type": "special", "xp_reward": 20000,"gold_reward": 2000,"attribute_reward": {"disciplina": 15.0, "foco": 12.0},       "difficulty": "extreme"},
    {"id": "special_rankup_b", "title": "Ascensão ao Rank B",        "description": "Alcance o Rank B.",                           "category": CATEGORY_MENTAL,   "mission_type": "special", "xp_reward": 1000, "gold_reward": 120,"attribute_reward": {"disciplina": 3.0},                      "difficulty": "medium"},
    {"id": "special_rankup_a", "title": "Ascensão ao Rank A",        "description": "Alcance o Rank A.",                           "category": CATEGORY_MENTAL,   "mission_type": "special", "xp_reward": 3000, "gold_reward": 300,"attribute_reward": {"disciplina": 5.0},                      "difficulty": "hard"},
    {"id": "special_rankup_s", "title": "Ascensão ao Rank S",        "description": "Alcance o Rank S.",                           "category": CATEGORY_MENTAL,   "mission_type": "special", "xp_reward": 8000, "gold_reward": 800,"attribute_reward": {"disciplina": 8.0},                      "difficulty": "extreme"},

    # ── SECRETAS ─────────────────────────────
    {"id": "secret_midnight",  "title": "???",                       "description": "???",                                          "category": CATEGORY_MENTAL,   "mission_type": "secret",  "xp_reward": 2000, "gold_reward": 200,"attribute_reward": {"foco": 5.0, "disciplina": 5.0},         "difficulty": "extreme", "secret": True, "unlock_condition": "Complete uma missão entre 00h e 04h."},
    {"id": "secret_perfect_w", "title": "???",                       "description": "???",                                          "category": CATEGORY_MENTAL,   "mission_type": "secret",  "xp_reward": 3000, "gold_reward": 300,"attribute_reward": {"disciplina": 8.0, "foco": 8.0},         "difficulty": "extreme", "secret": True, "unlock_condition": "Complete todas missões diárias por 7 dias seguidos."},
    {"id": "secret_all_attrs", "title": "???",                       "description": "???",                                          "category": CATEGORY_MENTAL,   "mission_type": "secret",  "xp_reward": 5000, "gold_reward": 500,"attribute_reward": {"disciplina": 5.0, "inteligencia": 5.0},  "difficulty": "extreme", "secret": True, "unlock_condition": "Todos os atributos >= 50."},
    {"id": "secret_nofap_90",  "title": "???",                       "description": "???",                                          "category": CATEGORY_MENTAL,   "mission_type": "secret",  "xp_reward": 4000, "gold_reward": 400,"attribute_reward": {"disciplina": 10.0, "foco": 8.0},        "difficulty": "extreme", "secret": True, "unlock_condition": "90 dias de NO FAP."},
]


# ─────────────────────────────────────────────
#  GERENCIADOR DE MISSÕES
# ─────────────────────────────────────────────

class MissionManager:
    def __init__(self):
        self._pool: list[Mission] = [Mission(**{k: v for k, v in m.items()}) for m in MISSION_POOL]

    def get_daily_missions(self) -> list[Mission]:
        """Retorna missões diárias ativas."""
        return [m for m in self._pool if m.mission_type == "daily" and m.active]

    def get_weekly_missions(self) -> list[Mission]:
        return [m for m in self._pool if m.mission_type == "weekly" and m.active]

    def get_monthly_missions(self) -> list[Mission]:
        return [m for m in self._pool if m.mission_type == "monthly" and m.active]

    def get_special_missions(self) -> list[Mission]:
        return [m for m in self._pool if m.mission_type == "special" and m.active]

    def get_secret_missions(self) -> list[Mission]:
        return [m for m in self._pool if m.mission_type == "secret" and m.active]

    def get_by_id(self, mission_id: str) -> Optional[Mission]:
        for m in self._pool:
            if m.id == mission_id:
                return m
        return None

    def all_missions_as_dicts(self) -> list[dict]:
        return [m.to_dict() for m in self._pool]

    def get_recommended_by_objective(self, objective: str, limit: int = 5) -> list[Mission]:
        """Retorna missões recomendadas baseadas no objetivo principal."""
        priority_map = {
            "Estética":              [CATEGORY_SELFCARE, CATEGORY_PHYSICAL],
            "Físico":                [CATEGORY_PHYSICAL, CATEGORY_SELFCARE],
            "Foco":                  [CATEGORY_MENTAL, CATEGORY_STUDY],
            "Disciplina":            [CATEGORY_MENTAL, CATEGORY_PHYSICAL],
            "Estudos":               [CATEGORY_STUDY, CATEGORY_MENTAL],
            "Saúde":                 [CATEGORY_SELFCARE, CATEGORY_PHYSICAL],
            "Social":                [CATEGORY_MENTAL, CATEGORY_SELFCARE],
            "Liderança":             [CATEGORY_MENTAL, CATEGORY_STUDY],
            "Desenvolvimento Completo": [CATEGORY_PHYSICAL, CATEGORY_STUDY, CATEGORY_MENTAL, CATEGORY_SELFCARE],
        }
        cats = priority_map.get(objective, [CATEGORY_PHYSICAL, CATEGORY_STUDY])
        result = []
        for cat in cats:
            result.extend([m for m in self._pool if m.category == cat and m.mission_type == "daily"])
        return result[:limit]


# Instância global
mission_manager = MissionManager()
