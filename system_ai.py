"""
Sistema da Evolução - System AI Module
A IA do Sistema: analisa o Jogador e emite mensagens dinâmicas.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import random
import datetime

if TYPE_CHECKING:
    from player import Player


# ─────────────────────────────────────────────
#  BANCO DE MENSAGENS
# ─────────────────────────────────────────────

MESSAGES_WELCOME = [
    "[SISTEMA] Jogador detectado. Iniciando protocolo de evolução.",
    "[SISTEMA] Conexão estabelecida. Bem-vindo ao Sistema da Evolução.",
    "[SISTEMA] Perfil carregado. A jornada continua.",
    "[SISTEMA] Sistema online. Jogador reconhecido.",
]

MESSAGES_LEVEL_UP = [
    "[SISTEMA] ⚡ LEVEL UP! Você evoluiu para o Nível {level}.",
    "[SISTEMA] 🌟 Nível {level} alcançado. Seu poder aumentou.",
    "[SISTEMA] ⬆️ EVOLUÇÃO DETECTADA — Nível {level} desbloqueado.",
    "[SISTEMA] 💥 BREAKTHROUGH — Nível {level}. Novas possibilidades abertas.",
    "[SISTEMA] 🔥 Você quebrou seus limites. Nível {level} atingido.",
]

MESSAGES_RANK_UP = [
    "[SISTEMA] 🏆 ASCENSÃO DE RANK — Você agora é Rank {rank}!",
    "[SISTEMA] ⚔️ Rank {rank} alcançado. O Sistema registra sua evolução.",
    "[SISTEMA] 💎 Nova classificação: Rank {rank}. Impressionante.",
    "[SISTEMA] 🌟 RANK UP → {rank}. Você está se tornando algo maior.",
    "[SISTEMA] 👑 O sistema reconhece: Rank {rank}. Sua jornada avança.",
]

MESSAGES_MISSION_COMPLETE = [
    "[SISTEMA] ✅ Missão concluída. +{xp} XP registrados.",
    "[SISTEMA] 🎯 Missão completada com sucesso. +{xp} XP",
    "[SISTEMA] 📊 Progresso registrado. +{xp} XP adicionados ao perfil.",
    "[SISTEMA] ⚡ +{xp} XP — A evolução não para.",
    "[SISTEMA] ✨ Missão: {title} — CONCLUÍDA.",
]

MESSAGES_STREAK = [
    "[SISTEMA] 🔥 Sequência ativa: {streak} dias. Continue.",
    "[SISTEMA] 💪 {streak} dias consecutivos. Consistência é poder.",
    "[SISTEMA] ⚡ Streak: {streak} dias. O momentum está com você.",
    "[SISTEMA] 🌟 {streak} dias sem parar. Isso é evolução real.",
]

MESSAGES_ACHIEVEMENT = [
    "[SISTEMA] 🏅 Nova conquista desbloqueada: {name}",
    "[SISTEMA] 🌟 CONQUISTA: {name} — Registrada no seu legado.",
    "[SISTEMA] 💎 Conquista adquirida: {name}",
    "[SISTEMA] ✨ DESBLOQUEADO: {name}",
]

MESSAGES_TITLE_UNLOCKED = [
    "[SISTEMA] 👑 Novo título disponível: '{title}'",
    "[SISTEMA] 🎖️ Título desbloqueado: '{title}'",
    "[SISTEMA] ⭐ Você conquistou o título: '{title}'",
]

MESSAGES_DISCIPLINE_UP = [
    "[SISTEMA] 📈 Sua disciplina aumentou. O caminho fica mais claro.",
    "[SISTEMA] 💪 Disciplina em ascensão. O sistema monitora sua evolução.",
    "[SISTEMA] ⚔️ Você está ficando mais disciplinado. Isso é poder.",
]

MESSAGES_FOCUS_UP = [
    "[SISTEMA] 🎯 Seu foco aumentou. A mente se afina.",
    "[SISTEMA] 🧠 Foco em crescimento. Continue treinando sua mente.",
    "[SISTEMA] 🌀 Concentração elevada detectada.",
]

MESSAGES_PERFORMANCE_DROP = [
    "[SISTEMA] ⚠️ Queda de desempenho detectada. Avaliação necessária.",
    "[SISTEMA] 📉 Seu {attribute} caiu esta semana. Reaja.",
    "[SISTEMA] 🔴 ALERTA — Atividade abaixo do padrão. Retome o ritmo.",
    "[SISTEMA] ⚠️ O sistema detectou inatividade. Suas missões aguardam.",
]

MESSAGES_FOCUS_DROP = [
    "[SISTEMA] ⚠️ Seu foco caiu esta semana. Meditação recomendada.",
    "[SISTEMA] 📉 Foco em declínio. Elimine distrações.",
    "[SISTEMA] 🔴 ALERTA DE FOCO — Retome suas práticas mentais.",
]

MESSAGES_NEW_MISSION = [
    "[SISTEMA] 📋 Nova missão disponível: {mission}",
    "[SISTEMA] ⚔️ Nova missão detectada: {mission}",
    "[SISTEMA] 🎯 Missão desbloqueada: {mission}",
]

MESSAGES_RANK_PROXIMITY = [
    "[SISTEMA] 📊 Você está próximo do Rank {rank}. {xp_needed} XP restantes.",
    "[SISTEMA] ⚔️ Rank {rank} ao alcance. Não pare agora.",
    "[SISTEMA] 🏆 {xp_needed} XP para o Rank {rank}. Foco total.",
]

MESSAGES_NOFAP_MILESTONE = [
    "[SISTEMA] 🌱 {days} dias de disciplina mental. Sua força cresce.",
    "[SISTEMA] 💪 {days} dias limpos. O Sistema registra sua vontade.",
    "[SISTEMA] 🔥 {days} dias — Uma batalha vencida a cada amanhecer.",
]

MESSAGES_DAILY_REMINDER = [
    "[SISTEMA] ☀️ Novo dia. Suas missões diárias aguardam.",
    "[SISTEMA] 🌅 Dia {day} da sua jornada. Hora de evoluir.",
    "[SISTEMA] 📋 Missões do dia disponíveis. Não desperdice o dia.",
    "[SISTEMA] ⚡ O sistema está ativo. Você está?",
]

MESSAGES_MILESTONE_DAYS = {
    10:   "[SISTEMA] 🔥 10 DIAS — Você passou pelo primeiro marco. A fundação está sendo construída.",
    20:   "[SISTEMA] ⚡ 20 DIAS — Hábitos começam a se solidificar. Continue.",
    30:   "[SISTEMA] 🌟 30 DIAS — Um mês de evolução. O Sistema reconhece sua consistência.",
    50:   "[SISTEMA] 💪 50 DIAS — Meio caminho para os primeiros 100. Impressionante.",
    75:   "[SISTEMA] 🏆 75 DIAS — Três quartos de 100. Você não é mais o mesmo.",
    100:  "[SISTEMA] 💎 100 DIAS — Marco histórico alcançado. Lendas são feitas de dias como este.",
    150:  "[SISTEMA] ⭐ 150 DIAS — Cinco meses de jornada. O caminho se revela.",
    200:  "[SISTEMA] 🌠 200 DIAS — Duzentos dias de evolução real. O Sistema reverencia isso.",
    365:  "[SISTEMA] 👑 365 DIAS — UM ANO INTEIRO. Você transcendeu o ponto de partida.",
    500:  "[SISTEMA] 🌌 500 DIAS — Você já não é mais um jogador comum.",
    1000: "[SISTEMA] ♾️ 1000 DIAS — Lenda Absoluta. O Sistema não tem palavras suficientes.",
}

MESSAGES_MOTIVATION = [
    "[SISTEMA] Lembre-se: cada missão completa é um tijolo no edifício da sua evolução.",
    "[SISTEMA] A disciplina hoje é a liberdade de amanhã.",
    "[SISTEMA] O Sistema observa cada escolha. Faça as certas.",
    "[SISTEMA] Você não precisa de motivação. Você precisa de disciplina.",
    "[SISTEMA] O progresso invisível também é progresso.",
    "[SISTEMA] Cada gota de suor é registrada. Nada se perde.",
    "[SISTEMA] A versão futura de você depende das escolhas de hoje.",
    "[SISTEMA] Descanso programado é estratégia. Comodidade constante é estagnação.",
    "[SISTEMA] O Rank mais alto começa com o Rank D. Você já começou.",
    "[SISTEMA] Missões não completadas hoje são dívidas com seu futuro.",
]

MESSAGES_ATTRIBUTE_MAX = [
    "[SISTEMA] 🌟 Atributo {attribute} maximizado. Perfeição alcançada nesta área.",
    "[SISTEMA] 💎 {attribute} atingiu o limite máximo. Poder absoluto.",
    "[SISTEMA] ⚡ {attribute}: 100. O Sistema registra o feito.",
]


# ─────────────────────────────────────────────
#  CLASSE PRINCIPAL
# ─────────────────────────────────────────────

class SystemAI:
    """IA do Sistema — analisa e gera mensagens para o Jogador."""

    @staticmethod
    def welcome() -> str:
        return random.choice(MESSAGES_WELCOME)

    @staticmethod
    def level_up(level: int) -> str:
        return random.choice(MESSAGES_LEVEL_UP).format(level=level)

    @staticmethod
    def rank_up(rank: str) -> str:
        return random.choice(MESSAGES_RANK_UP).format(rank=rank)

    @staticmethod
    def mission_complete(title: str, xp: int) -> str:
        return random.choice(MESSAGES_MISSION_COMPLETE).format(title=title, xp=xp)

    @staticmethod
    def streak_update(streak: int) -> str:
        return random.choice(MESSAGES_STREAK).format(streak=streak)

    @staticmethod
    def achievement_unlocked(name: str) -> str:
        return random.choice(MESSAGES_ACHIEVEMENT).format(name=name)

    @staticmethod
    def title_unlocked(title: str) -> str:
        return random.choice(MESSAGES_TITLE_UNLOCKED).format(title=title)

    @staticmethod
    def discipline_up() -> str:
        return random.choice(MESSAGES_DISCIPLINE_UP)

    @staticmethod
    def focus_up() -> str:
        return random.choice(MESSAGES_FOCUS_UP)

    @staticmethod
    def performance_drop(attribute: str = "desempenho") -> str:
        return random.choice(MESSAGES_PERFORMANCE_DROP).format(attribute=attribute)

    @staticmethod
    def focus_drop() -> str:
        return random.choice(MESSAGES_FOCUS_DROP)

    @staticmethod
    def new_mission(mission: str) -> str:
        return random.choice(MESSAGES_NEW_MISSION).format(mission=mission)

    @staticmethod
    def rank_proximity(rank: str, xp_needed: int) -> str:
        return random.choice(MESSAGES_RANK_PROXIMITY).format(rank=rank, xp_needed=xp_needed)

    @staticmethod
    def nofap_milestone(days: int) -> str:
        return random.choice(MESSAGES_NOFAP_MILESTONE).format(days=days)

    @staticmethod
    def daily_reminder(day: int) -> str:
        return random.choice(MESSAGES_DAILY_REMINDER).format(day=day)

    @staticmethod
    def milestone_days(days: int) -> str | None:
        return MESSAGES_MILESTONE_DAYS.get(days)

    @staticmethod
    def motivation() -> str:
        return random.choice(MESSAGES_MOTIVATION)

    @staticmethod
    def attribute_max(attribute: str) -> str:
        return random.choice(MESSAGES_ATTRIBUTE_MAX).format(attribute=attribute)

    @staticmethod
    def analyze_player(player: "Player") -> list[str]:
        """Analisa o Jogador e retorna uma lista de mensagens relevantes."""
        messages: list[str] = []
        attrs = player.attributes

        # Verifica queda em foco
        if attrs.foco < 20:
            messages.append(SystemAI.focus_drop())

        # Verifica queda de disciplina
        if attrs.disciplina < 20:
            messages.append(SystemAI.performance_drop("disciplina"))

        # Verifica rank próximo
        from player import RANK_THRESHOLDS, RANKS
        current_idx = RANKS.index(player.rank) if player.rank in RANKS else 0
        if current_idx < len(RANKS) - 1:
            next_rank = RANKS[current_idx + 1]
            next_threshold = RANK_THRESHOLDS.get(next_rank, 0)
            xp_needed = next_threshold - player.xp
            if 0 < xp_needed <= 2000:
                messages.append(SystemAI.rank_proximity(next_rank, xp_needed))

        # Streak ativo
        if player.day_tracker.current_streak > 0 and player.day_tracker.current_streak % 7 == 0:
            messages.append(SystemAI.streak_update(player.day_tracker.current_streak))

        # Motivação aleatória
        if random.random() < 0.3:
            messages.append(SystemAI.motivation())

        return messages

    @staticmethod
    def generate_report(player: "Player", period: str = "daily") -> dict:
        """Gera um relatório de desempenho."""
        attrs = player.attributes
        report = {
            "period": period,
            "date": datetime.datetime.now().isoformat(),
            "player_name": player.name,
            "level": player.level,
            "rank": player.rank,
            "xp_total": player.xp,
            "missions_total": player.missions.total,
            "current_streak": player.day_tracker.current_streak,
            "attributes_snapshot": attrs.to_dict(),
            "system_messages": SystemAI.analyze_player(player),
            "highlights": [],
            "warnings": [],
        }

        # Destaques
        if attrs.disciplina >= 50:
            report["highlights"].append("Disciplina elevada — mantendo o padrão.")
        if player.day_tracker.current_streak >= 7:
            report["highlights"].append(f"Streak de {player.day_tracker.current_streak} dias ativo.")
        if player.missions.total >= 100:
            report["highlights"].append("100+ missões completadas. Você é consistente.")

        # Alertas
        if attrs.foco < 30:
            report["warnings"].append("Foco baixo — priorize meditação e planejamento.")
        if attrs.saude < 30:
            report["warnings"].append("Saúde baixa — hidratação e sono são essenciais.")
        if player.day_tracker.current_streak == 0:
            report["warnings"].append("Nenhuma sequência ativa — recomece hoje.")

        return report


system_ai = SystemAI()
