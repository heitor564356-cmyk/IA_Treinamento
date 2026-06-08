"""
Sistema da Evolução - Backend Principal (Flask API)
Serve os dados do sistema para o frontend via REST API.
"""

from __future__ import annotations
import sys
import os
import json
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
except ImportError:
    print("Instalando dependências...")
    os.system("pip install flask flask-cors")
    from flask import Flask, request, jsonify
    from flask_cors import CORS

from player import Player, Attributes, xp_for_next_level, calculate_rank, ALL_TITLES
from missions import mission_manager, CATEGORY_PHYSICAL, CATEGORY_STUDY, CATEGORY_SELFCARE, CATEGORY_MENTAL
from achievements import AchievementManager, ACHIEVEMENTS_POOL
from system_ai import SystemAI
from save_manager import (
    save_player, load_player, backup_player,
    save_legacy, load_legacy, player_exists, delete_save
)
from ranking import RankingManager, DAY_MILESTONES

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
#  ESTADO GLOBAL (em memória durante a sessão)
# ─────────────────────────────────────────────
_player: Player | None = None
_ach_manager: AchievementManager = AchievementManager()
_notifications: list[str] = []

ATTRIBUTE_NAMES = {
    "forca": "Força", "resistencia": "Resistência", "inteligencia": "Inteligência",
    "conhecimento": "Conhecimento", "disciplina": "Disciplina", "foco": "Foco",
    "saude": "Saúde", "energia": "Energia", "carisma": "Carisma", "aparencia": "Aparência",
}


def _get_player() -> Player:
    global _player
    if _player is None:
        data = load_player()
        if data:
            _player = Player.from_dict(data)
    return _player


def _push_notification(msg: str):
    _notifications.append(msg)
    if len(_notifications) > 50:
        _notifications.pop(0)


def _auto_save():
    if _player:
        save_player(_player)
        save_legacy(_player)


def _check_titles(player: Player) -> list[str]:
    """Verifica e desbloqueia títulos baseado nos atributos e progresso."""
    unlocked = []
    attrs = player.attributes
    total = player.missions.total
    streak = player.day_tracker.current_streak
    days = player.day_tracker.total_days
    level = player.level
    rank = player.rank

    conditions = {
        "iniciante":         True,
        "pioneiro":          True,
        "aprendiz":          total >= 5,
        "persistente":       streak >= 7,
        "disciplinado":      attrs.disciplina >= 30,
        "estudioso":         player.missions.study >= 10,
        "focado":            attrs.foco >= 30,
        "organizado":        player.missions.selfcare >= 5,
        "lutador":           player.missions.physical >= 10,
        "guerreiro":         rank in ["B", "B+", "A-", "A", "A+", "S-", "S", "S+", "SS", "SS+", "SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "sobrevivente":      days >= 30,
        "determinado":       total >= 50,
        "estrategista":      attrs.inteligencia >= 40,
        "guardiao":          attrs.saude >= 40,
        "conquistador":      total >= 100,
        "mestre_disciplina": attrs.disciplina >= 70,
        "mestre_mente":      attrs.inteligencia >= 70,
        "mestre_corpo":      attrs.forca >= 70,
        "lenda_viva":        days >= 365,
        "ascendente":        rank in ["S", "S+", "SS", "SS+", "SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "imperador":         attrs.disciplina >= 90,
        "atleta":            attrs.resistencia >= 50,
        "academico":         attrs.conhecimento >= 50,
        "saudavel":          attrs.saude >= 60,
        "energizado":        attrs.energia >= 60,
        "carismatico":       attrs.carisma >= 50,
        "belo":              attrs.aparencia >= 50,
        "incansavel":        streak >= 14,
        "inabalavel":        streak >= 30,
        "monolito":          streak >= 50,
        "eterno":            streak >= 100,
        "vencedor":          level >= 10,
        "veterano":          level >= 20,
        "elite":             level >= 30,
        "lendario":          level >= 50,
        "perfeicionista":    all(v >= 50 for v in attrs.to_dict().values()),
        "harmonioso":        all(v >= 60 for v in attrs.to_dict().values()),
        "completo":          all(v >= 70 for v in attrs.to_dict().values()),
        "treinador":         player.missions.physical >= 200,
        "scholar":           player.missions.study >= 200,
        "monge":             player.missions.mental >= 200,
        "cuidador":          player.missions.selfcare >= 200,
        "consistente":       streak >= 21,
        "imparavel":         rank in ["A+", "S-", "S", "S+", "SS", "SS+", "SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "lider":             attrs.carisma >= 70,
        "sabio":             attrs.conhecimento >= 80,
        "titan":             (attrs.forca + attrs.resistencia) >= 150,
        # Secretos
        "monarca":           rank in ["SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "soberano":          rank in ["Z", "Z+", "Z++", "EX", "Ω"],
        "ultimo_heroi":      total >= 1000,
        "filho_evolucao":    days >= 365 and all(v >= 60 for v in attrs.to_dict().values()),
        "ascendido":         rank in ["Z+", "Z++", "EX", "Ω"],
        "portador_destino":  level >= 100,
        "rei_constancia":    streak >= 365,
        "alem_limite":       rank == "Ω",
        "sombra_eterna":     rank in ["Z++", "EX", "Ω"] and player.nofap.clean_days >= 90,
        "despertar":         all(v >= 80 for v in attrs.to_dict().values()),
    }

    for title_data in ALL_TITLES:
        tid = title_data["id"]
        if tid not in player.unlocked_titles and conditions.get(tid, False):
            player.unlocked_titles.append(tid)
            unlocked.append(title_data["name"])
            _push_notification(SystemAI.title_unlocked(title_data["name"]))

    return unlocked


def _check_achievements(player: Player) -> list[str]:
    """Verifica conquistas e desbloqueia as elegíveis."""
    unlocked = []
    now = datetime.datetime.now().isoformat()
    attrs = player.attributes
    streak = player.day_tracker.current_streak
    days = player.day_tracker.total_days
    level = player.level
    rank = player.rank
    nofap = player.nofap.clean_days

    conditions: dict[str, bool] = {
        "ach_mission_1":     player.missions.total >= 1,
        "ach_mission_10":    player.missions.total >= 10,
        "ach_mission_25":    player.missions.total >= 25,
        "ach_mission_50":    player.missions.total >= 50,
        "ach_mission_100":   player.missions.total >= 100,
        "ach_mission_250":   player.missions.total >= 250,
        "ach_mission_500":   player.missions.total >= 500,
        "ach_study_1":       player.missions.study >= 1,
        "ach_study_5":       player.missions.study >= 5,
        "ach_study_25":      player.missions.study >= 25,
        "ach_study_50":      player.missions.study >= 50,
        "ach_study_100":     player.missions.study >= 100,
        "ach_study_200":     player.missions.study >= 200,
        "ach_study_10h":     player.day_tracker.study_hours >= 10,
        "ach_study_50h":     player.day_tracker.study_hours >= 50,
        "ach_study_100h":    player.day_tracker.study_hours >= 100,
        "ach_code_1":        True,
        "ach_code_10":       player.missions.study >= 10,
        "ach_work_1":        player.missions.physical >= 1,
        "ach_work_10":       player.missions.physical >= 10,
        "ach_work_50":       player.missions.physical >= 50,
        "ach_work_100":      player.missions.physical >= 100,
        "ach_work_200":      player.missions.physical >= 200,
        "ach_force_50":      attrs.forca >= 50,
        "ach_force_80":      attrs.forca >= 80,
        "ach_health_50":     attrs.saude >= 50,
        "ach_health_80":     attrs.saude >= 80,
        "ach_energy_50":     attrs.energia >= 50,
        "ach_disc_30":       attrs.disciplina >= 30,
        "ach_disc_60":       attrs.disciplina >= 60,
        "ach_disc_90":       attrs.disciplina >= 90,
        "ach_focus_50":      attrs.foco >= 50,
        "ach_focus_80":      attrs.foco >= 80,
        "ach_streak_3":      streak >= 3,
        "ach_streak_7":      streak >= 7,
        "ach_streak_14":     streak >= 14,
        "ach_streak_21":     streak >= 21,
        "ach_streak_30":     streak >= 30,
        "ach_streak_50":     streak >= 50,
        "ach_streak_75":     streak >= 75,
        "ach_streak_100":    streak >= 100,
        "ach_streak_200":    streak >= 200,
        "ach_streak_365":    streak >= 365,
        "ach_days_10":       days >= 10,
        "ach_days_50":       days >= 50,
        "ach_days_100":      days >= 100,
        "ach_days_200":      days >= 200,
        "ach_days_365":      days >= 365,
        "ach_days_500":      days >= 500,
        "ach_days_1000":     days >= 1000,
        "ach_level_5":       level >= 5,
        "ach_level_10":      level >= 10,
        "ach_level_20":      level >= 20,
        "ach_level_30":      level >= 30,
        "ach_level_50":      level >= 50,
        "ach_level_100":     level >= 100,
        "ach_rank_c":        rank in ["C", "C+", "B-", "B", "B+", "A-", "A", "A+", "S-", "S", "S+", "SS", "SS+", "SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "ach_rank_b":        rank in ["B", "B+", "A-", "A", "A+", "S-", "S", "S+", "SS", "SS+", "SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "ach_rank_a":        rank in ["A", "A+", "S-", "S", "S+", "SS", "SS+", "SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "ach_rank_s":        rank in ["S", "S+", "SS", "SS+", "SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "ach_rank_ss":       rank in ["SS", "SS+", "SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "ach_rank_sss":      rank in ["SSS", "Z", "Z+", "Z++", "EX", "Ω"],
        "ach_nofap_7":       nofap >= 7,
        "ach_nofap_30":      nofap >= 30,
        "ach_nofap_90":      nofap >= 90,
    }

    for ach_id, condition in conditions.items():
        if condition and ach_id not in player.achievements:
            ach = _ach_manager.get_by_id(ach_id)
            if ach:
                player.achievements.append(ach_id)
                player.xp += ach.xp_reward
                player.gold += ach.gold_reward
                unlocked.append(ach.name)
                _push_notification(SystemAI.achievement_unlocked(ach.name))

    return unlocked


# ─────────────────────────────────────────────
#  ROTAS API
# ─────────────────────────────────────────────

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "system": "Sistema da Evolução", "version": "1.0"})


@app.route("/api/player/exists", methods=["GET"])
def player_exists_route():
    return jsonify({"exists": player_exists()})


@app.route("/api/player/create", methods=["POST"])
def create_player():
    global _player, _ach_manager
    data = request.json
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    player = Player()
    player.name = data.get("name", "Jogador")
    player.age = int(data.get("age", 18))
    player.main_objective = data.get("main_objective", "Desenvolvimento Completo")

    # Inicializar tracker de dias
    now = datetime.datetime.now().isoformat()
    player.day_tracker.creation_date = now
    player.day_tracker.total_days = 1
    player.day_tracker.current_streak = 1
    player.day_tracker.best_streak = 1
    player.day_tracker.last_login = now

    # Atributos iniciais por objetivo
    obj_bonus = {
        "Físico":                 {"forca": 5, "resistencia": 5},
        "Estética":               {"aparencia": 5, "saude": 5},
        "Foco":                   {"foco": 5, "inteligencia": 3},
        "Disciplina":             {"disciplina": 7, "foco": 3},
        "Estudos":                {"inteligencia": 5, "conhecimento": 5},
        "Saúde":                  {"saude": 7, "energia": 3},
        "Social":                 {"carisma": 7, "aparencia": 3},
        "Liderança":              {"carisma": 5, "inteligencia": 5},
        "Desenvolvimento Completo": {"disciplina": 3, "foco": 3, "saude": 2, "energia": 2},
    }
    bonuses = obj_bonus.get(player.main_objective, {})
    for attr, val in bonuses.items():
        current = getattr(player.attributes, attr, 0)
        setattr(player.attributes, attr, current + val)

    player.unlocked_titles = ["iniciante", "pioneiro"]
    player.title = "Iniciante"

    # Registrar histórico inicial de atributos
    player.attribute_history.append({
        "date": now,
        "snapshot": player.attributes.to_dict(),
    })

    _player = player
    _ach_manager = AchievementManager()

    # Desbloquear conquistas e títulos iniciais
    _check_achievements(player)
    _check_titles(player)

    save_player(player)
    save_legacy(player)

    return jsonify({
        "success": True,
        "message": SystemAI.welcome(),
        "player": player.to_dict(),
    })


@app.route("/api/player", methods=["GET"])
def get_player():
    player = _get_player()
    if not player:
        return jsonify({"error": "Nenhum Jogador encontrado"}), 404

    # Verificar login diário
    _update_daily_login(player)

    return jsonify(player.to_dict())


def _update_daily_login(player: Player):
    now = datetime.datetime.now()
    last = player.day_tracker.last_login
    changed = False
    if last:
        last_dt = datetime.datetime.fromisoformat(last)
        delta = (now.date() - last_dt.date()).days
        if delta == 1:
            player.day_tracker.current_streak += 1
            player.day_tracker.total_days += 1
            if player.day_tracker.current_streak > player.day_tracker.best_streak:
                player.day_tracker.best_streak = player.day_tracker.current_streak
            _push_notification(SystemAI.daily_reminder(player.day_tracker.total_days))
            changed = True
        elif delta > 1:
            player.day_tracker.current_streak = 1
            player.day_tracker.total_days += 1
            changed = True
    if changed:
        player.day_tracker.last_login = now.isoformat()
        # Verificar marcos
        milestone_msg = SystemAI.milestone_days(player.day_tracker.total_days)
        if milestone_msg:
            _push_notification(milestone_msg)
        reward = RankingManager.check_day_milestone(player)
        if reward:
            _push_notification(f"[SISTEMA] 🎁 Marco de {player.day_tracker.total_days} dias! +{reward['xp']} XP +{reward['gold']} Ouro")
        _check_achievements(player)
        _check_titles(player)
        _auto_save()


@app.route("/api/missions", methods=["GET"])
def get_missions():
    mtype = request.args.get("type", "daily")
    missions_map = {
        "daily":   mission_manager.get_daily_missions(),
        "weekly":  mission_manager.get_weekly_missions(),
        "monthly": mission_manager.get_monthly_missions(),
        "special": mission_manager.get_special_missions(),
        "secret":  mission_manager.get_secret_missions(),
    }
    missions = missions_map.get(mtype, mission_manager.get_daily_missions())
    return jsonify([m.to_dict() for m in missions])


@app.route("/api/missions/complete", methods=["POST"])
def complete_mission():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404

    data = request.json
    mission_id = data.get("mission_id")
    study_hours = float(data.get("study_hours", 0))

    mission = mission_manager.get_by_id(mission_id)
    if not mission:
        return jsonify({"error": "Missão não encontrada"}), 404

    if mission_id in player.missions.daily_completed_today:
        return jsonify({"error": "Missão já completada hoje"}), 400

    # Completar missão
    mission.completed = True
    player.missions.daily_completed_today.append(mission_id)
    player.missions.total += 1
    old_xp = player.xp
    player.xp += mission.xp_reward
    player.gold += mission.gold_reward

    # Contagem por categoria
    if mission.category == CATEGORY_PHYSICAL:
        player.missions.physical += 1
        player.day_tracker.workouts_done += 1
    elif mission.category == CATEGORY_STUDY:
        player.missions.study += 1
        player.day_tracker.study_hours += study_hours if study_hours > 0 else 0.5
    elif mission.category == CATEGORY_SELFCARE:
        player.missions.selfcare += 1
    elif mission.category == CATEGORY_MENTAL:
        player.missions.mental += 1

    # Atributos
    for attr, gain in mission.attribute_reward.items():
        current = getattr(player.attributes, attr, 0)
        new_val = min(100.0, current + gain)
        setattr(player.attributes, attr, new_val)
        if new_val >= 100:
            _push_notification(SystemAI.attribute_max(ATTRIBUTE_NAMES.get(attr, attr)))

    _push_notification(SystemAI.mission_complete(mission.title, mission.xp_reward))

    # Level up
    level_ups = []
    while player.xp >= player.xp_next:
        player.xp -= player.xp_next
        player.level += 1
        player.attribute_points += 3
        player.gold += 50 * player.level
        player.xp_next = xp_for_next_level(player.level)
        level_ups.append(player.level)
        _push_notification(SystemAI.level_up(player.level))
        player.level_history.append({"level": player.level, "date": datetime.datetime.now().isoformat()})

    # Rank up
    new_rank = RankingManager.check_rank_up(player)
    if new_rank:
        _push_notification(SystemAI.rank_up(new_rank))

    # Conquistas e Títulos
    new_achievements = _check_achievements(player)
    new_titles = _check_titles(player)

    # Snapshot de atributo periódico
    if player.missions.total % 10 == 0:
        player.attribute_history.append({
            "date": datetime.datetime.now().isoformat(),
            "snapshot": player.attributes.to_dict(),
        })

    _auto_save()

    return jsonify({
        "success": True,
        "xp_gained": mission.xp_reward,
        "gold_gained": mission.gold_reward,
        "level_ups": level_ups,
        "new_rank": new_rank,
        "new_achievements": new_achievements,
        "new_titles": new_titles,
        "notifications": _notifications[-5:],
        "player": player.to_dict(),
    })


@app.route("/api/achievements", methods=["GET"])
def get_achievements():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404

    result = []
    for ach_data in ACHIEVEMENTS_POOL:
        entry = dict(ach_data)
        entry["unlocked"] = ach_data["id"] in player.achievements
        if entry.get("secret") and not entry["unlocked"]:
            entry["name"] = "???"
            entry["description"] = "Conquista secreta."
        result.append(entry)
    return jsonify(result)


@app.route("/api/titles", methods=["GET"])
def get_titles():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404

    from player import ALL_TITLES
    result = []
    for t in ALL_TITLES:
        entry = dict(t)
        entry["unlocked"] = t["id"] in player.unlocked_titles
        if entry.get("secret") and not entry["unlocked"]:
            entry["name"] = "???"
            entry["desc"] = "Título secreto."
        result.append(entry)
    return jsonify(result)


@app.route("/api/player/set_title", methods=["POST"])
def set_title():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404

    data = request.json
    title_id = data.get("title_id")
    from player import ALL_TITLES
    title_data = next((t for t in ALL_TITLES if t["id"] == title_id), None)
    if not title_data:
        return jsonify({"error": "Título não encontrado"}), 404
    if title_id not in player.unlocked_titles:
        return jsonify({"error": "Título não desbloqueado"}), 403

    player.title = title_data["name"]
    _auto_save()
    return jsonify({"success": True, "title": player.title})


@app.route("/api/player/add_xp", methods=["POST"])
def add_xp():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404
    data = request.json
    amount = int(data.get("amount", 0))
    player.xp += amount
    new_rank = RankingManager.check_rank_up(player)
    while player.xp >= player.xp_next:
        player.xp -= player.xp_next
        player.level += 1
        player.attribute_points += 3
        player.xp_next = xp_for_next_level(player.level)
    _auto_save()
    return jsonify({"success": True, "player": player.to_dict(), "new_rank": new_rank})


@app.route("/api/player/spend_points", methods=["POST"])
def spend_attribute_points():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404
    data = request.json
    attribute = data.get("attribute")
    amount = int(data.get("amount", 1))
    if player.attribute_points < amount:
        return jsonify({"error": "Pontos insuficientes"}), 400
    if not hasattr(player.attributes, attribute):
        return jsonify({"error": "Atributo inválido"}), 400
    current = getattr(player.attributes, attribute)
    setattr(player.attributes, attribute, min(100.0, current + amount * 2.0))
    player.attribute_points -= amount
    _check_titles(player)
    _auto_save()
    return jsonify({"success": True, "player": player.to_dict()})


@app.route("/api/nofap/start", methods=["POST"])
def nofap_start():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404
    player.nofap.active = True
    player.nofap.clean_days = 0
    player.nofap.start_date = datetime.datetime.now().isoformat()
    _auto_save()
    return jsonify({"success": True, "message": "[SISTEMA] Módulo NO FAP ativado. A jornada começa agora."})


@app.route("/api/nofap/checkin", methods=["POST"])
def nofap_checkin():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404
    player.nofap.clean_days += 1
    if player.nofap.clean_days > player.nofap.record:
        player.nofap.record = player.nofap.clean_days
    new_ach = _check_achievements(player)
    msg = SystemAI.nofap_milestone(player.nofap.clean_days)
    _push_notification(msg)
    _auto_save()
    return jsonify({"success": True, "clean_days": player.nofap.clean_days, "message": msg, "new_achievements": new_ach})


@app.route("/api/nofap/fall", methods=["POST"])
def nofap_fall():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404
    player.nofap.history.append({
        "date": datetime.datetime.now().isoformat(),
        "days_reached": player.nofap.clean_days,
    })
    player.nofap.clean_days = 0
    player.nofap.start_date = datetime.datetime.now().isoformat()
    _auto_save()
    return jsonify({
        "success": True,
        "message": "[SISTEMA] Recaída registrada. XP, Nível e Rank preservados. Recomeçar é parte da jornada.",
        "player": player.to_dict(),
    })


@app.route("/api/reports/daily", methods=["GET"])
def daily_report():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404
    report = SystemAI.generate_report(player, "daily")
    return jsonify(report)


@app.route("/api/reports/weekly", methods=["GET"])
def weekly_report():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404
    report = SystemAI.generate_report(player, "weekly")
    return jsonify(report)


@app.route("/api/reports/monthly", methods=["GET"])
def monthly_report():
    player = _get_player()
    if not player:
        return jsonify({"error": "Jogador não encontrado"}), 404
    report = SystemAI.generate_report(player, "monthly")
    return jsonify(report)


@app.route("/api/legacy", methods=["GET"])
def get_legacy():
    legacy = load_legacy()
    if not legacy:
        player = _get_player()
        if player:
            save_legacy(player)
            legacy = load_legacy()
    return jsonify(legacy or {})


@app.route("/api/notifications", methods=["GET"])
def get_notifications():
    msgs = list(_notifications)
    _notifications.clear()
    return jsonify({"notifications": msgs})


@app.route("/api/rankings/info", methods=["GET"])
def rankings_info():
    return jsonify(RankingManager.all_ranks_info())


@app.route("/api/system/message", methods=["GET"])
def system_message():
    player = _get_player()
    if not player:
        return jsonify({"message": SystemAI.motivation()})
    msgs = SystemAI.analyze_player(player)
    if not msgs:
        msgs = [SystemAI.motivation()]
    return jsonify({"messages": msgs})


@app.route("/api/player/reset", methods=["POST"])
def reset_player():
    global _player, _ach_manager
    data = request.json or {}
    confirm = data.get("confirm", False)
    if not confirm:
        return jsonify({"error": "Confirmação necessária: {\"confirm\": true}"}), 400
    delete_save()
    _player = None
    _ach_manager = AchievementManager()
    return jsonify({"success": True, "message": "[SISTEMA] Perfil deletado. Um novo começo aguarda."})


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  SISTEMA DA EVOLUÇÃO — Backend v1.0")
    print("  Servidor: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
