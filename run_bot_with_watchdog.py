import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotReloader(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = self.start_bot()

    def start_bot(self):
        print("Iniciando o bot...")
        return subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        # Reinicia apenas quando o arquivo monitorado mudar
        if event.src_path.endswith(self.script):
            print(f"{self.script} modificado. Reiniciando o bot...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except Exception:
                pass
            self.process = self.start_bot()

if __name__ == "__main__":
    script_name = "bot.py"
    event_handler = BotReloader(script_name)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print("Monitorando alterações em bot.py. Feche esta janela para encerrar o bot.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando...")
        try:
            event_handler.process.terminate()
        except Exception:
            pass
        observer.stop()
    observer.join()
