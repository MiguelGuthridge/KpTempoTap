# Keypirinha: a fast launcher for Windows (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu

import time

class TempoTapper(kp.Plugin):
    """Evaluate expressions or solve equations"""
    DEFAULT_KEEP_HISTORY = False

    keep_history = DEFAULT_KEEP_HISTORY
    
    ITEMCAT_VAR = kp.ItemCategory.USER_BASE + 1

    prev_times = []
    
    LISTEN_STR = "tempo "

    def __init__(self):
        super().__init__()

    def on_start(self):
        pass

    def on_catalog(self):
        self.on_start()

    def on_suggest(self, user_input: str, items_chain):
        if not (user_input.startswith(self.LISTEN_STR) and len(user_input) > len(self.LISTEN_STR)):
            return
        if items_chain:
            return
        suggestions = []
        
        t_curr = time.time()
        
        # Reset if over 5 seconds has passed
        if len(self.prev_times):
            if t_curr - self.prev_times[-1] > 5.0:
                self.prev_times = []
        
        self.prev_times.append(t_curr)
        
        # If we don't have at least one data point
        if len(self.prev_times) < 2:
            return
        
        t_diffs = [self.prev_times[i] - self.prev_times[i-1] for i in range(1, len(self.prev_times))]
        
        
        
        tempo = int(1 / (sum(t_diffs)/len(t_diffs)) * 60)
        
        print(t_diffs)
        
        suggestions = [self.create_item(
                    category=self.ITEMCAT_VAR,
                    label=str(tempo),
                    short_desc="Tempo Tapper - Enter to copy to clipboard",
                    target=str(tempo),
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE,
                )]
        
        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.LABEL_ASC)

    def on_execute(self, item, action):
        # Reset times
        self.prev_times = []
        if item.category() != self.ITEMCAT_VAR:
            return
        if item and (item.category() == self.ITEMCAT_VAR):
            kpu.set_clipboard(item.target())

    def on_events(self, flags):
        if flags & kp.Events.PACKCONFIG:
            self._read_config()

    def _read_config(self):
        settings = self.load_settings()
        self.keep_history = settings.get_bool(
            "keep_history", "main", self.DEFAULT_KEEP_HISTORY)
