"""
Sistema da Evolução - Save Manager
Gerencia salvamento, carregamento e backup do perfil do Jogador.
"""

from __future__ import annotations
import json
import os
import shutil
import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAVE_FILE = os.path.join(DATA_DIR, "save.json")
LEGACY_FILE = os.path.join(DATA_DIR, "legacy.json")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")


def _ensure_dirs() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)


def save_player(player: "Player") -> bool:
    """Salva o perfil do Jogador em save.json."""
    try:
        _ensure_dirs()
        data = player.to_dict()
        data["saved_at"] = datetime.datetime.now().isoformat()
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[SAVE ERROR] {e}")
        return False


def load_player() -> Optional[dict]:
    """Carrega o perfil do Jogador de save.json."""
    try:
        if not os.path.exists(SAVE_FILE):
            return None
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[LOAD ERROR] {e}")
        return None


def backup_player() -> bool:
    """Cria um backup automático do save atual."""
    try:
        _ensure_dirs()
        if not os.path.exists(SAVE_FILE):
            return False
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"save_backup_{timestamp}.json")
        shutil.copy2(SAVE_FILE, backup_path)
        _cleanup_old_backups()
        return True
    except Exception as e:
        print(f"[BACKUP ERROR] {e}")
        return False


def _cleanup_old_backups(max_backups: int = 10) -> None:
    """Mantém apenas os N backups mais recentes."""
    try:
        backups = sorted([
            os.path.join(BACKUP_DIR, f)
            for f in os.listdir(BACKUP_DIR)
            if f.startswith("save_backup_")
        ])
        while len(backups) > max_backups:
            os.remove(backups.pop(0))
    except Exception:
        pass


def save_legacy(player: "Player") -> bool:
    """Salva dados de legado do Jogador."""
    try:
        _ensure_dirs()
        legacy = {
            "name": player.name,
            "creation_date": player.day_tracker.creation_date,
            "total_days": player.day_tracker.total_days,
            "study_hours": player.day_tracker.study_hours,
            "workouts_done": player.day_tracker.workouts_done,
            "missions_total": player.missions.total,
            "best_streak": player.day_tracker.best_streak,
            "final_level": player.level,
            "final_rank": player.rank,
            "unlocked_titles": player.unlocked_titles,
            "achievements": player.achievements,
            "attribute_history": player.attribute_history,
            "rank_history": player.rank_history,
            "level_history": player.level_history,
            "attributes_snapshot": player.attributes.to_dict(),
            "saved_at": datetime.datetime.now().isoformat(),
        }
        with open(LEGACY_FILE, "w", encoding="utf-8") as f:
            json.dump(legacy, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[LEGACY ERROR] {e}")
        return False


def load_legacy() -> Optional[dict]:
    """Carrega dados de legado."""
    try:
        if not os.path.exists(LEGACY_FILE):
            return None
        with open(LEGACY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[LEGACY LOAD ERROR] {e}")
        return None


def player_exists() -> bool:
    """Verifica se existe um save de Jogador."""
    return os.path.exists(SAVE_FILE)


def delete_save() -> bool:
    """Deleta o save atual (usado apenas para reset total)."""
    try:
        backup_player()
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        return True
    except Exception as e:
        print(f"[DELETE ERROR] {e}")
        return False
