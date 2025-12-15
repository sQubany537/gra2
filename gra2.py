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
    # Inicjalizacja odbywa się tylko raz, przy pierwszym uruchomieniu
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
    
    # Krok 1: Sprawdzenie, czy gra się skończyła
    if st.session_state.game_over:
        st.session_state.current_log.append("Gra skończona! Zrestartuj, by grać dalej.")
        return

    # Krok 2: SPRAWDZENIE BLOKADY RUCHU (Tutaj był potencjalny błąd składniowy)
    if st.session_state.enemy_active:
        st.session_state.current_log.append("⚠️ Najpierw musisz pokonać wroga, zanim się ruszysz!")
        return

    # Krok 3: Obliczanie nowej pozycji
    old_x, old_y = st.session_state.player_pos
    new_x = max(0, min(MAP_SIZE - 1, old_x + dx))
    new_y = max(0, min(MAP_SIZE - 1, old_y + dy))

    # Krok 4: Aktualizacja pozycji i logu
    st.session_state.player_pos = (new_x, new_y)
    st.session_state.current_log.append(f"Przeniesiono do: ({new_x}, {new_y})")

    # Krok 5: Sprawdzenie warunku zwycięstwa
    if new_x == MAP_SIZE - 1 and new_y == MAP_SIZE - 1:
        st.session_state.current_log.append("🎉 ZWYCIĘSTWO! Dotarłeś do celu!")
        st.session_state.game_over = True
        return

    # Krok 6: Losowe pojawienie się wroga
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

    if st.session_state.enemy_hp <= 0:
        st.session_state.enemy_active = False
        st.session_state.score += 100
        st.session_state.current_log.append(f"💥 Wróg pokonany! Zdobywasz 100 punktów. HP gracza: {st.session_state.player_hp}")
        return

    # Kontratak Wroga
    enemy_damage = random.randint(5, 15)
    st.session_state.player_hp -= enemy_damage
    st.session_state.current_log.append(f"⚡ Wróg kontratakuje! Tracisz {enemy_damage} HP. Pozostałe HP wroga: {st.session_state.enemy_hp}")

    # Sprawdzenie porażki
    if st.session_state.player_hp <= 0:
        st.session_state.current_log.append("💀 TWOJA STATKA ZOSTAŁA ZNISZCZONA. KONIEC GRY.")
        st.session_state.game_over = True

def run_away():
    """Próba ucieczki od wroga."""
    if st.session_state.game_over: return
    if not st.session_state.enemy_active:
        st.session_state.current_log.append("Nie ma przed kim uciekać.")
        return

    if random.random() < 0.5:
        st.session_state.enemy_active = False
        st.session_state.current_log.append("💨 Ucieczka udana! Możesz się teraz ruszać.")
    else:
        st.session_state.current_log.append("❌ Ucieczka nieudana! Wróg atakuje!")
        enemy_damage = random.randint(10, 20)
        st.session_state.player_hp -= enemy_damage
        st.session_state.current_log.append(f"Tracisz {enemy_damage} HP w trakcie ucieczki. Aktualne HP: {st.session_state.player_hp}")
        if st.session_state.player_hp <= 0:
            st.session_state.current_log.append("💀 KONIEC GRY.")
            st.session_state.game_over = True

def reset_game():
    """Resetuje stan gry."""
    st.session_state.player_hp = 100
    st.session_state.player_pos = (0, 0)
    st.session_state.current_log = ["Gra zrestartowana. Rozpocznij nową podróż!"]
    st.session_state.enemy_active = False
    st.session_state.enemy_hp = ENEMY_HP
    st.session_state.score = 0
    st.session_state.game_over = False

# --- Wyświetlanie Stanu Gry (UI) ---

st.sidebar.header("📊 Statystyki Gracza")
st.sidebar.metric("Życie (HP)", st.session_state.player_hp)
st.sidebar.metric("Pozycja (X, Y)", f"({st.session_state.player_pos[0]}, {st.session_state.player_pos[1]})")
st.sidebar.metric("Wynik", st.session_state.score)

if st.session_state.enemy_active:
    st.sidebar.subheader("Wróg Aktywny! 🤖")
    st.sidebar.progress(st.session_state.enemy_hp / ENEMY_HP, text=f"HP Wroga: {st.session_state.enemy_hp}/{ENEMY_HP}")

st.sidebar.button("🔄 Nowa Gra", on_click=reset_game)

# --- Mapa (Wizualizacja Emojami) ---

st.header("🗺️ Twoja Lokalizacja")
map_display = []
current_x, current_y = st.session_state.player_pos

for y in range(MAP_SIZE):
    row = []
    for x in range(MAP_SIZE):
        if x == current_x and y == current_y:
            row.append("🛰️") # Gracz
        elif x == MAP_SIZE - 1 and y == MAP_SIZE - 1:
            row.append("🎯") # Cel
        else:
            row.append("⚫") # Puste pole
    map_display.append(" ".join(row))

st.code("\n".join(map_display), language='text')

# --- Interakcje (Przyciski) ---

st.header("🧭 Akcje")
c1, c2, c3 = st.columns(3)

if not st.session_state.enemy_active:
    # Przyciski ruchu (aktywne, gdy nie ma wroga)
    c2.button("⬆️ Północ (Y+1)", on_click=move, args=(0, 1,))
    c1.button("⬅️ Zachód (X-1)", on_click=move, args=(-1, 0,))
    c3.button("➡️ Wschód (X+1)", on_click=move, args=(1, 0,))
    c2.button("⬇️ Południe (Y-1)", on_click=move, args=(0, -1,))
else:
    # Przyciski walki (aktywne, gdy jest wróg)
    st.warning("Wróg blokuje Twój ruch! Walcz lub uciekaj!")
    c1, c2 = st.columns(2)
    c1.button("💥 STRZELAJ (Atakuj)", on_click=attack)
    c2.button("🏃 UCIECZKA", on_click=run_away)

# --- Log Gry ---
st.header("📜 Log Zdarzeń")
# Wyświetlanie logu w odwróconej kolejności, by najnowsze było na górze
for entry in reversed(st.session_state.current_log):
    st.markdown(f"* {entry}")
