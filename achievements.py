"""
Sistema da Evolução - Achievements Module
100+ conquistas em diversas categorias.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Achievement:
    id: str
    name: str
    description: str
    category: str
    icon: str
    xp_reward: int
    gold_reward: int
    secret: bool = False
    unlocked: bool = False
    unlock_date: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "icon": self.icon,
            "xp_reward": self.xp_reward,
            "gold_reward": self.gold_reward,
            "secret": self.secret,
            "unlocked": self.unlocked,
            "unlock_date": self.unlock_date,
        }

    @staticmethod
    def from_dict(d: dict) -> "Achievement":
        a = Achievement(**{k: v for k, v in d.items()})
        return a


ACHIEVEMENTS_POOL: list[dict] = [

    # ── ESTUDOS ──────────────────────────────────────
    {"id": "ach_study_1",        "name": "Primeira Leitura",         "description": "Complete sua primeira missão de leitura.",         "category": "Estudos",       "icon": "📖", "xp_reward": 100,  "gold_reward": 10},
    {"id": "ach_study_5",        "name": "Curioso",                  "description": "Complete 5 missões de estudo.",                    "category": "Estudos",       "icon": "🔍", "xp_reward": 200,  "gold_reward": 25},
    {"id": "ach_study_25",       "name": "Dedicado",                 "description": "Complete 25 missões de estudo.",                   "category": "Estudos",       "icon": "📚", "xp_reward": 500,  "gold_reward": 60},
    {"id": "ach_study_50",       "name": "Estudioso",                "description": "Complete 50 missões de estudo.",                   "category": "Estudos",       "icon": "🎓", "xp_reward": 1000, "gold_reward": 120},
    {"id": "ach_study_100",      "name": "Scholar",                  "description": "Complete 100 missões de estudo.",                  "category": "Estudos",       "icon": "🏫", "xp_reward": 2500, "gold_reward": 300},
    {"id": "ach_study_200",      "name": "Mestre do Conhecimento",   "description": "Complete 200 missões de estudo.",                  "category": "Estudos",       "icon": "🧙", "xp_reward": 5000, "gold_reward": 600},
    {"id": "ach_book_1",         "name": "Leitor",                   "description": "Termine 1 livro.",                                 "category": "Estudos",       "icon": "📗", "xp_reward": 800,  "gold_reward": 100},
    {"id": "ach_book_5",         "name": "Bibliófilo",               "description": "Termine 5 livros.",                                "category": "Estudos",       "icon": "📚", "xp_reward": 3000, "gold_reward": 350},
    {"id": "ach_study_10h",      "name": "10 Horas de Foco",         "description": "Acumule 10 horas de estudo.",                      "category": "Estudos",       "icon": "⏱️", "xp_reward": 500,  "gold_reward": 60},
    {"id": "ach_study_50h",      "name": "50 Horas de Foco",         "description": "Acumule 50 horas de estudo.",                      "category": "Estudos",       "icon": "⏰", "xp_reward": 2000, "gold_reward": 250},
    {"id": "ach_study_100h",     "name": "100 Horas de Foco",        "description": "Acumule 100 horas de estudo.",                     "category": "Estudos",       "icon": "🕰️", "xp_reward": 4000, "gold_reward": 500},
    {"id": "ach_code_1",         "name": "Hello World",              "description": "Complete uma missão de programação.",              "category": "Estudos",       "icon": "💻", "xp_reward": 150,  "gold_reward": 18},
    {"id": "ach_code_10",        "name": "Programador",              "description": "Complete 10 missões de programação.",              "category": "Estudos",       "icon": "🖥️", "xp_reward": 600,  "gold_reward": 75},

    # ── TREINO ───────────────────────────────────────
    {"id": "ach_work_1",         "name": "Primeira Suor",            "description": "Complete seu primeiro treino.",                    "category": "Treino",        "icon": "💪", "xp_reward": 100,  "gold_reward": 10},
    {"id": "ach_work_10",        "name": "Em Movimento",             "description": "Complete 10 treinos.",                             "category": "Treino",        "icon": "🏃", "xp_reward": 300,  "gold_reward": 35},
    {"id": "ach_work_50",        "name": "Atleta",                   "description": "Complete 50 treinos.",                             "category": "Treino",        "icon": "🏋️", "xp_reward": 1200, "gold_reward": 150},
    {"id": "ach_work_100",       "name": "Guerreiro do Ferro",       "description": "Complete 100 treinos.",                            "category": "Treino",        "icon": "⚔️", "xp_reward": 3000, "gold_reward": 350},
    {"id": "ach_work_200",       "name": "Titã",                     "description": "Complete 200 treinos.",                            "category": "Treino",        "icon": "🦾", "xp_reward": 6000, "gold_reward": 700},
    {"id": "ach_run_10km",       "name": "Corredor Iniciante",       "description": "Acumule 10 km de corrida.",                        "category": "Treino",        "icon": "👟", "xp_reward": 400,  "gold_reward": 50},
    {"id": "ach_run_50km",       "name": "Corredor Dedicado",        "description": "Acumule 50 km de corrida.",                        "category": "Treino",        "icon": "🏅", "xp_reward": 1500, "gold_reward": 180},
    {"id": "ach_run_marathon",   "name": "Maratonista",              "description": "Acumule 42 km de corrida total.",                  "category": "Treino",        "icon": "🏆", "xp_reward": 2000, "gold_reward": 250},
    {"id": "ach_pushup_100",     "name": "100 Flexões",              "description": "Complete 100 flexões em um dia.",                  "category": "Treino",        "icon": "💥", "xp_reward": 500,  "gold_reward": 60},
    {"id": "ach_force_50",       "name": "Força Bruta",              "description": "Atributo Força alcança 50.",                       "category": "Treino",        "icon": "🔥", "xp_reward": 800,  "gold_reward": 100},
    {"id": "ach_force_80",       "name": "Superpoder",               "description": "Atributo Força alcança 80.",                       "category": "Treino",        "icon": "⚡", "xp_reward": 2500, "gold_reward": 300},

    # ── SAÚDE ────────────────────────────────────────
    {"id": "ach_water_7",        "name": "Hidratado",                "description": "Beba água por 7 dias seguidos.",                   "category": "Saúde",         "icon": "💧", "xp_reward": 300,  "gold_reward": 35},
    {"id": "ach_sleep_7",        "name": "Descanso Sagrado",         "description": "Durma cedo por 7 dias seguidos.",                  "category": "Saúde",         "icon": "🌙", "xp_reward": 350,  "gold_reward": 40},
    {"id": "ach_no_junk_30",     "name": "Alimentação Limpa",        "description": "30 dias sem junk food.",                           "category": "Saúde",         "icon": "🥗", "xp_reward": 1500, "gold_reward": 180},
    {"id": "ach_health_50",      "name": "Corpo Saudável",           "description": "Atributo Saúde alcança 50.",                       "category": "Saúde",         "icon": "❤️", "xp_reward": 800,  "gold_reward": 100},
    {"id": "ach_health_80",      "name": "Saúde de Ferro",           "description": "Atributo Saúde alcança 80.",                       "category": "Saúde",         "icon": "💚", "xp_reward": 2500, "gold_reward": 300},
    {"id": "ach_energy_50",      "name": "Energia Plena",            "description": "Atributo Energia alcança 50.",                     "category": "Saúde",         "icon": "⚡", "xp_reward": 700,  "gold_reward": 85},
    {"id": "ach_skincare_30",    "name": "Pele de Cristal",          "description": "30 dias de skincare consecutivos.",                "category": "Saúde",         "icon": "✨", "xp_reward": 1000, "gold_reward": 120},

    # ── DISCIPLINA ───────────────────────────────────
    {"id": "ach_disc_plan_7",    "name": "Planejador",               "description": "Planeje seus dias por 7 dias seguidos.",           "category": "Disciplina",    "icon": "📋", "xp_reward": 400,  "gold_reward": 50},
    {"id": "ach_disc_30",        "name": "Disciplina de Aço",        "description": "Atributo Disciplina alcança 30.",                  "category": "Disciplina",    "icon": "🔩", "xp_reward": 400,  "gold_reward": 50},
    {"id": "ach_disc_60",        "name": "Mestre da Disciplina",     "description": "Atributo Disciplina alcança 60.",                  "category": "Disciplina",    "icon": "⚔️", "xp_reward": 1500, "gold_reward": 180},
    {"id": "ach_disc_90",        "name": "Imperador",                "description": "Atributo Disciplina alcança 90.",                  "category": "Disciplina",    "icon": "👑", "xp_reward": 4000, "gold_reward": 500},
    {"id": "ach_focus_50",       "name": "Mente Afiada",             "description": "Atributo Foco alcança 50.",                        "category": "Disciplina",    "icon": "🎯", "xp_reward": 700,  "gold_reward": 85},
    {"id": "ach_focus_80",       "name": "Concentração Total",       "description": "Atributo Foco alcança 80.",                        "category": "Disciplina",    "icon": "🌀", "xp_reward": 2500, "gold_reward": 300},
    {"id": "ach_meditation_30",  "name": "Meditador",                "description": "Complete 30 missões de meditação.",                "category": "Disciplina",    "icon": "🧘", "xp_reward": 1200, "gold_reward": 150},

    # ── CONSISTÊNCIA ─────────────────────────────────
    {"id": "ach_streak_3",       "name": "3 Dias",                   "description": "3 dias consecutivos.",                             "category": "Consistência",  "icon": "🔥", "xp_reward": 150,  "gold_reward": 18},
    {"id": "ach_streak_7",       "name": "Uma Semana",               "description": "7 dias consecutivos.",                             "category": "Consistência",  "icon": "🔥", "xp_reward": 350,  "gold_reward": 40},
    {"id": "ach_streak_14",      "name": "Duas Semanas",             "description": "14 dias consecutivos.",                            "category": "Consistência",  "icon": "🔥", "xp_reward": 700,  "gold_reward": 85},
    {"id": "ach_streak_21",      "name": "21 Dias — Hábito",         "description": "21 dias consecutivos. Hábito formado.",            "category": "Consistência",  "icon": "🌟", "xp_reward": 1200, "gold_reward": 150},
    {"id": "ach_streak_30",      "name": "Um Mês Inteiro",           "description": "30 dias consecutivos.",                            "category": "Consistência",  "icon": "⭐", "xp_reward": 2000, "gold_reward": 250},
    {"id": "ach_streak_50",      "name": "50 Dias",                  "description": "50 dias consecutivos.",                            "category": "Consistência",  "icon": "💫", "xp_reward": 3500, "gold_reward": 420},
    {"id": "ach_streak_75",      "name": "75 Dias",                  "description": "75 dias consecutivos.",                            "category": "Consistência",  "icon": "🌠", "xp_reward": 5000, "gold_reward": 600},
    {"id": "ach_streak_100",     "name": "Cem Dias",                 "description": "100 dias consecutivos.",                           "category": "Consistência",  "icon": "💎", "xp_reward": 8000, "gold_reward": 1000},
    {"id": "ach_streak_200",     "name": "200 Dias",                 "description": "200 dias consecutivos.",                           "category": "Consistência",  "icon": "🏆", "xp_reward": 15000,"gold_reward": 1800},
    {"id": "ach_streak_365",     "name": "Um Ano",                   "description": "365 dias consecutivos.",                           "category": "Consistência",  "icon": "👑", "xp_reward": 30000,"gold_reward": 3600},
    {"id": "ach_days_10",        "name": "10 Dias de Jornada",       "description": "10 dias desde o início.",                          "category": "Consistência",  "icon": "📅", "xp_reward": 200,  "gold_reward": 25},
    {"id": "ach_days_50",        "name": "50 Dias de Jornada",       "description": "50 dias desde o início.",                          "category": "Consistência",  "icon": "📅", "xp_reward": 1000, "gold_reward": 120},
    {"id": "ach_days_100",       "name": "100 Dias de Jornada",      "description": "100 dias desde o início.",                         "category": "Consistência",  "icon": "📅", "xp_reward": 2500, "gold_reward": 300},
    {"id": "ach_days_200",       "name": "200 Dias de Jornada",      "description": "200 dias desde o início.",                         "category": "Consistência",  "icon": "📅", "xp_reward": 5000, "gold_reward": 600},
    {"id": "ach_days_365",       "name": "365 Dias de Jornada",      "description": "365 dias desde o início.",                         "category": "Consistência",  "icon": "🎆", "xp_reward": 15000,"gold_reward": 1800},
    {"id": "ach_days_500",       "name": "500 Dias de Jornada",      "description": "500 dias desde o início.",                         "category": "Consistência",  "icon": "🎇", "xp_reward": 25000,"gold_reward": 3000},
    {"id": "ach_days_1000",      "name": "1000 Dias de Jornada",     "description": "1000 dias desde o início.",                        "category": "Consistência",  "icon": "♾️", "xp_reward": 50000,"gold_reward": 6000},

    # ── MISSÕES ──────────────────────────────────────
    {"id": "ach_mission_1",      "name": "Primeiro Passo",           "description": "Complete sua primeira missão.",                    "category": "Missões",       "icon": "👣", "xp_reward": 50,   "gold_reward": 5},
    {"id": "ach_mission_10",     "name": "Em Ritmo",                 "description": "Complete 10 missões.",                             "category": "Missões",       "icon": "🎵", "xp_reward": 200,  "gold_reward": 25},
    {"id": "ach_mission_25",     "name": "Comprometido",             "description": "Complete 25 missões.",                             "category": "Missões",       "icon": "✅", "xp_reward": 500,  "gold_reward": 60},
    {"id": "ach_mission_50",     "name": "Determinado",              "description": "Complete 50 missões.",                             "category": "Missões",       "icon": "🎯", "xp_reward": 1000, "gold_reward": 120},
    {"id": "ach_mission_100",    "name": "Centurião",                "description": "Complete 100 missões.",                            "category": "Missões",       "icon": "🛡️", "xp_reward": 2500, "gold_reward": 300},
    {"id": "ach_mission_250",    "name": "Veterano",                 "description": "Complete 250 missões.",                            "category": "Missões",       "icon": "⚔️", "xp_reward": 6000, "gold_reward": 720},
    {"id": "ach_mission_500",    "name": "Lendário",                 "description": "Complete 500 missões.",                            "category": "Missões",       "icon": "🌟", "xp_reward": 15000,"gold_reward": 1800},
    {"id": "ach_daily_all",      "name": "Dia Perfeito",             "description": "Complete todas as missões diárias em um dia.",     "category": "Missões",       "icon": "💯", "xp_reward": 800,  "gold_reward": 100},
    {"id": "ach_weekly_all",     "name": "Semana Perfeita",          "description": "Complete todas as missões semanais.",              "category": "Missões",       "icon": "🏅", "xp_reward": 2000, "gold_reward": 250},

    # ── STREAKS ──────────────────────────────────────
    {"id": "ach_nofap_7",        "name": "7 Dias Limpos",            "description": "7 dias de NO FAP.",                                "category": "Streaks",       "icon": "🌱", "xp_reward": 400,  "gold_reward": 50},
    {"id": "ach_nofap_30",       "name": "30 Dias Limpos",           "description": "30 dias de NO FAP.",                               "category": "Streaks",       "icon": "🌿", "xp_reward": 2000, "gold_reward": 250},
    {"id": "ach_nofap_90",       "name": "90 Dias Limpos",           "description": "90 dias de NO FAP.",                               "category": "Streaks",       "icon": "🌳", "xp_reward": 6000, "gold_reward": 750},

    # ── NÍVEIS ───────────────────────────────────────
    {"id": "ach_level_5",        "name": "Nível 5",                  "description": "Alcance o nível 5.",                               "category": "Níveis",        "icon": "⬆️", "xp_reward": 200,  "gold_reward": 25},
    {"id": "ach_level_10",       "name": "Nível 10",                 "description": "Alcance o nível 10.",                              "category": "Níveis",        "icon": "⬆️", "xp_reward": 500,  "gold_reward": 60},
    {"id": "ach_level_20",       "name": "Nível 20",                 "description": "Alcance o nível 20.",                              "category": "Níveis",        "icon": "⬆️", "xp_reward": 1200, "gold_reward": 150},
    {"id": "ach_level_30",       "name": "Nível 30",                 "description": "Alcance o nível 30.",                              "category": "Níveis",        "icon": "⬆️", "xp_reward": 2500, "gold_reward": 300},
    {"id": "ach_level_50",       "name": "Nível 50",                 "description": "Alcance o nível 50.",                              "category": "Níveis",        "icon": "⬆️", "xp_reward": 6000, "gold_reward": 720},
    {"id": "ach_level_100",      "name": "Nível 100",                "description": "Alcance o nível 100.",                             "category": "Níveis",        "icon": "🌟", "xp_reward": 20000,"gold_reward": 2500},

    # ── RANKINGS ─────────────────────────────────────
    {"id": "ach_rank_c",         "name": "Rank C",                   "description": "Alcance o Rank C.",                                "category": "Rankings",      "icon": "🏅", "xp_reward": 300,  "gold_reward": 35},
    {"id": "ach_rank_b",         "name": "Rank B",                   "description": "Alcance o Rank B.",                                "category": "Rankings",      "icon": "🥈", "xp_reward": 800,  "gold_reward": 100},
    {"id": "ach_rank_a",         "name": "Rank A",                   "description": "Alcance o Rank A.",                                "category": "Rankings",      "icon": "🥇", "xp_reward": 2500, "gold_reward": 300},
    {"id": "ach_rank_s",         "name": "Rank S",                   "description": "Alcance o Rank S.",                                "category": "Rankings",      "icon": "💎", "xp_reward": 8000, "gold_reward": 1000},
    {"id": "ach_rank_ss",        "name": "Rank SS",                  "description": "Alcance o Rank SS.",                               "category": "Rankings",      "icon": "💠", "xp_reward": 20000,"gold_reward": 2500},
    {"id": "ach_rank_sss",       "name": "Rank SSS",                 "description": "Alcance o Rank SSS.",                              "category": "Rankings",      "icon": "🌟", "xp_reward": 50000,"gold_reward": 6000},

    # ── SECRETAS ─────────────────────────────────────
    {"id": "ach_secret_1",       "name": "???",                      "description": "Conquista secreta.",                               "category": "Secretas",      "icon": "🔒", "xp_reward": 5000, "gold_reward": 600,  "secret": True},
    {"id": "ach_secret_2",       "name": "???",                      "description": "Conquista secreta.",                               "category": "Secretas",      "icon": "🔒", "xp_reward": 5000, "gold_reward": 600,  "secret": True},
    {"id": "ach_secret_3",       "name": "???",                      "description": "Conquista secreta.",                               "category": "Secretas",      "icon": "🔒", "xp_reward": 10000,"gold_reward": 1200, "secret": True},
    {"id": "ach_secret_omega",   "name": "???",                      "description": "Conquista secreta suprema.",                       "category": "Secretas",      "icon": "🔒", "xp_reward": 99999,"gold_reward": 9999, "secret": True},
]


class AchievementManager:
    def __init__(self):
        self._pool: list[Achievement] = [Achievement(**{k: v for k, v in a.items()}) for a in ACHIEVEMENTS_POOL]

    def get_all(self) -> list[Achievement]:
        return self._pool

    def get_by_id(self, ach_id: str) -> Optional[Achievement]:
        for a in self._pool:
            if a.id == ach_id:
                return a
        return None

    def get_unlocked(self) -> list[Achievement]:
        return [a for a in self._pool if a.unlocked]

    def get_by_category(self, category: str) -> list[Achievement]:
        return [a for a in self._pool if a.category == category]

    def unlock(self, ach_id: str, unlock_date: str) -> Optional[Achievement]:
        a = self.get_by_id(ach_id)
        if a and not a.unlocked:
            a.unlocked = True
            a.unlock_date = unlock_date
            return a
        return None

    def all_as_dicts(self) -> list[dict]:
        return [a.to_dict() for a in self._pool]

    @staticmethod
    def from_dicts(dicts: list[dict]) -> "AchievementManager":
        mgr = AchievementManager()
        for d in dicts:
            a = mgr.get_by_id(d["id"])
            if a:
                a.unlocked = d.get("unlocked", False)
                a.unlock_date = d.get("unlock_date")
        return mgr


achievement_manager = AchievementManager()
