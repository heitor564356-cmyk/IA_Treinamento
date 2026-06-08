"""
Sistema da Evolução - Ranking Module
Gerencia cálculo de ranks, milestones e recompensas de dias.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from player import Player

from player import RANK_THRESHOLDS, RANKS, calculate_rank


# ─────────────────────────────────────────────
#  RECOMPENSAS POR MARCOS DE DIAS
# ─────────────────────────────────────────────

DAY_MILESTONES: dict[int, dict] = {
    10:   {"xp": 500,   "gold": 60,   "title": None,           "achievement": "ach_days_10"},
    20:   {"xp": 1000,  "gold": 120,  "title": None,           "achievement": None},
    30:   {"xp": 2000,  "gold": 250,  "title": "sobrevivente", "achievement": None},
    50:   {"xp": 3500,  "gold": 420,  "title": "inabalavel",   "achievement": "ach_days_50"},
    75:   {"xp": 5000,  "gold": 600,  "title": None,           "achievement": None},
    100:  {"xp": 8000,  "gold": 1000, "title": "monolito",     "achievement": "ach_days_100"},
    150:  {"xp": 12000, "gold": 1500, "title": None,           "achievement": None},
    200:  {"xp": 18000, "gold": 2200, "title": None,           "achievement": "ach_days_200"},
    365:  {"xp": 35000, "gold": 4200, "title": "lenda_viva",   "achievement": "ach_days_365"},
    500:  {"xp": 50000, "gold": 6000, "title": None,           "achievement": "ach_days_500"},
    1000: {"xp": 99999, "gold": 9999, "title": "eterno",       "achievement": "ach_days_1000"},
}

# ─────────────────────────────────────────────
#  INFORMAÇÕES DOS RANKS
# ─────────────────────────────────────────────

RANK_INFO: dict[str, dict] = {
    "D":    {"color": "#9e9e9e", "label": "D",    "secret": False, "special": False},
    "D+":   {"color": "#90a4ae", "label": "D+",   "secret": False, "special": False},
    "C-":   {"color": "#80cbc4", "label": "C-",   "secret": False, "special": False},
    "C":    {"color": "#4db6ac", "label": "C",    "secret": False, "special": False},
    "C+":   {"color": "#26a69a", "label": "C+",   "secret": False, "special": False},
    "B-":   {"color": "#66bb6a", "label": "B-",   "secret": False, "special": False},
    "B":    {"color": "#43a047", "label": "B",    "secret": False, "special": False},
    "B+":   {"color": "#2e7d32", "label": "B+",   "secret": False, "special": False},
    "A-":   {"color": "#ffa726", "label": "A-",   "secret": False, "special": False},
    "A":    {"color": "#fb8c00", "label": "A",    "secret": False, "special": False},
    "A+":   {"color": "#e65100", "label": "A+",   "secret": False, "special": False},
    "S-":   {"color": "#ef5350", "label": "S-",   "secret": False, "special": False},
    "S":    {"color": "#e53935", "label": "S",    "secret": False, "special": False},
    "S+":   {"color": "#b71c1c", "label": "S+",   "secret": False, "special": False},
    "SS":   {"color": "#ce93d8", "label": "SS",   "secret": False, "special": False},
    "SS+":  {"color": "#ba68c8", "label": "SS+",  "secret": False, "special": False},
    "SSS":  {"color": "#9c27b0", "label": "SSS",  "secret": False, "special": False},
    "Z":    {"color": "#7c4dff", "label": "Z",    "secret": True,  "special": False},
    "Z+":   {"color": "#651fff", "label": "Z+",   "secret": True,  "special": False},
    "Z++":  {"color": "#4527a0", "label": "Z++",  "secret": True,  "special": False},
    "EX":   {"color": "#f5a623", "label": "EX",   "secret": False, "special": True},
    "Ω":    {"color": "#00e5ff", "label": "Ω",    "secret": False, "special": True},
}


class RankingManager:

    @staticmethod
    def get_current_rank(xp: int) -> str:
        return calculate_rank(xp)

    @staticmethod
    def get_rank_info(rank: str) -> dict:
        return RANK_INFO.get(rank, {"color": "#fff", "label": rank, "secret": False, "special": False})

    @staticmethod
    def get_next_rank(current_rank: str) -> tuple[str | None, int]:
        """Retorna o próximo rank e o XP necessário para alcançá-lo."""
        if current_rank not in RANKS:
            return None, 0
        idx = RANKS.index(current_rank)
        if idx >= len(RANKS) - 1:
            return None, 0
        next_rank = RANKS[idx + 1]
        return next_rank, RANK_THRESHOLDS.get(next_rank, 0)

    @staticmethod
    def check_rank_up(player: "Player") -> str | None:
        """Verifica se o Jogador subiu de rank. Retorna o novo rank ou None."""
        new_rank = calculate_rank(player.xp)
        if new_rank != player.rank:
            old_rank = player.rank
            player.rank = new_rank
            player.rank_history.append({
                "rank": new_rank,
                "from": old_rank,
                "date": datetime.datetime.now().isoformat(),
                "xp": player.xp,
            })
            return new_rank
        return None

    @staticmethod
    def check_day_milestone(player: "Player") -> dict | None:
        """Verifica se o Jogador atingiu um marco de dias e retorna a recompensa."""
        days = player.day_tracker.total_days
        if days in DAY_MILESTONES:
            reward = DAY_MILESTONES[days]
            player.xp += reward["xp"]
            player.gold += reward["gold"]
            if reward.get("title") and reward["title"] not in player.unlocked_titles:
                player.unlocked_titles.append(reward["title"])
            return reward
        return None

    @staticmethod
    def get_rank_progress_pct(xp: int) -> float:
        """Retorna o percentual de progresso dentro do rank atual (0.0 - 1.0)."""
        current_rank = calculate_rank(xp)
        if current_rank not in RANKS:
            return 1.0
        idx = RANKS.index(current_rank)
        current_threshold = RANK_THRESHOLDS.get(current_rank, 0)
        if idx >= len(RANKS) - 1:
            return 1.0
        next_rank = RANKS[idx + 1]
        next_threshold = RANK_THRESHOLDS.get(next_rank, current_threshold + 1)
        progress = (xp - current_threshold) / (next_threshold - current_threshold)
        return max(0.0, min(1.0, progress))

    @staticmethod
    def all_ranks_info() -> list[dict]:
        result = []
        for rank in RANKS:
            info = RANK_INFO.get(rank, {})
            result.append({
                "rank": rank,
                "color": info.get("color", "#fff"),
                "xp_required": RANK_THRESHOLDS.get(rank, 0),
                "secret": info.get("secret", False),
                "special": info.get("special", False),
            })
        return result


ranking_manager = RankingManager()
