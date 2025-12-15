import streamlit as st
import random

st.title("🚀 Kosmiczny Podróżnik: Tekstowa Przygoda")
st.markdown("---")

# --- Stałe Gry ---
MAP_SIZE = 5
ENEMY_PROBABILITY = 0.3 # Szansa na pojawienie się wroga po ruchu
ATTACK_DAMAGE = 20
ENEMY_HP = 50

# --- Inicjalizacja Stanu Sesji ---

def initialize_game_state():
    """Ustawia początkowy stan gry."""
    if 'player_hp' not in st.session_state:
        st.session_state.player_hp = 100
        st.session_state.player_pos = (0, 0)
        st.session_state.current_log = ["Rozpoczynasz podróż! Twoim celem jest dotarcie do współrzędnych (4, 4)."]
        st.session_state.enemy_active = False
        st.session_state.enemy_hp = ENEMY_HP
        st.session_state.score = 0
        st.session_state.game_over = False

initialize_game_state()

# --- Funkcje Logiki Gry ---

def move(dx, dy):
    """Przenosi gracza i sprawdza, czy spotkał wroga."""
    if st.session_state.game_over:
        st.session_state.current_log.append("Gra skończona! Zrestartuj, by grać dalej.")
        return

    old_x, old_y = st.session_state.player_pos
    new_x = max(0, min(MAP_SIZE - 1, old_x + dx))
    new_y = max(0, min(MAP_SIZE - 1, old_y + dy))

    if st.session_state.enemy_active:
        st.session_state.current_log.append("⚠️ Najpierw musisz pokonać wroga, zanim się ruszysz!")
        return

    st.session_state.player_pos = (new_x, new_y)
    st.session_state.current_log.append(f"Przeniesiono do: ({new_x}, {new_y})")

    # Sprawdzenie warunku zwycięstwa
    if new_x == MAP_SIZE - 1 and new_y == MAP_SIZE - 1:
        st.session_state.current_log.append("🎉 ZWYCIĘSTWO! Dotarłeś do celu!")
        st.session_state.game_over = True
        return

    # Losowe pojawienie się wroga
    if random.random() < ENEMY_PROBABILITY:
        st.session_state.enemy_active = True
        st.session_state.enemy_hp = ENEMY_HP
        st.session_state.current_log.append("🚨 Spotykasz wrogiego Kosmicznego Robota!")

    # Utrzymanie logu na rozsądnej długości
    if len(st.session_state.current_log) > 10:
        st.session_state.current_log = st.session_state.current_log[-10:]

def attack():
    """Symuluje 'strzelanie' do wroga."""
    if st.session_state.game_over:
        st.session_state.current_log.append("Gra skończona!")
        return
        
    if not st.session_state.enemy_active:
        st.session_state.current_log.append("Nie ma wroga do zaatakowania.")
        return

    # Atak Gracza
    player_hit = random.randint(10, ATTACK_DAMAGE)
    st.session_state.enemy_hp -= player_hit
    st.session_state.current_log.append(f"🔥 STRZELASZ! Zadano {player_hit} obrażeń.")

    if st.session_state
