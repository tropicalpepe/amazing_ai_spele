# Specifikācija: Lietotāja Saskarne (UI/UX Team)

**Atbildība:** Lietotāja interakcijas, ekrānu zīmēšana un notikumu (events) savienošana ar loģiku.
**Atkarības:** UI ir "klients". Tas izsauc Loģikas funkcijas un patērē Datu komandas `GameState`.

## Sistēmas Plūsma un Līgumi (UI Controller)

Tā kā UI var būt implementēts dažādos veidos (Web, Desktop Tkinter), šeit ir definētas **notikumu apstrādes funkcijas (Event Handlers)**, kas obligāti jāsavieno ar vizuālajām pogām.

```python
# Šis ir konceptuāls UI Kontrolieris. Jūs varat to realizēt kā klasi.

class GameUIController:
    def __init__(self):
        self.current_state: 'GameState' = None
        self.ai_algorithm: str = "minimax" # vai "alpha-beta"
        
    def on_init_app(self):
        """
        Izsauc `generate_starting_numbers()`.
        Attēlo 5 pogas ekrānā un parāda sākuma izvēlni.
        """
        pass

    def on_start_game(self, selected_number: int, player_starts: bool, algorithm: str):
        """
        Izsauc, kad lietotājs izvēlas sākuma skaitli un nospiež "Sākt".
        Inicializē GameState(selected_number, 0, 0, 0, player_starts).
        Pārslēdz UI uz galveno spēles skatu.
        """
        pass

    def on_divide_clicked(self, divisor: int):
        """
        Izsauc, kad lietotājs nospiež "/2" vai "/3" pogu.
        
        Solis 1: if not is_valid_move(self.current_state.current_number, divisor):
                    parādīt kļūdas paziņojumu lietotājam.
                    return
        Solis 2: self.current_state = apply_move(self.current_state, divisor)
        Solis 3: Atjaunina vizuālos labels (punktus, skaitli).
        Solis 4: if is_game_over(self.current_state.current_number):
                    trigger_end_game()
                    return
        Solis 5: trigger_ai_turn() # Dod komandu AI veikt savu gājienu.
        """
        pass
        
    def trigger_end_game(self):
        """
        Izsauc `calculate_final_payout(self.current_state)`.
        Parāda pēcspēles ekrānu ar uzvarētāju un pogu "Restartēt".
        """
        pass

    def on_restart_clicked(self):
        """
        Nodzēš current_state, atgriež lietotāju uz sākuma izvēlni.
        """
        pass