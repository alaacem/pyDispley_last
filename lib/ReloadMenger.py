import fasteners

class ReloadMenger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lock = fasteners.InterProcessLock(self.file_path + ".lock")
    def set_refresh_flag(self):
        with self.lock:
            with open(self.file_path, "w") as file:
                file.write("True")
    def check_for_refresh(self):
        with self.lock:
            try:
                with open(self.file_path, "r") as file:
                    flag = file.read().strip()
                    if flag == "True":
                        self.reset_refresh_flag()
                        return True
            except FileNotFoundError:
                self.reset_refresh_flag()
                pass
            return False
    def reset_refresh_flag(self):
        with self.lock:
            with open(self.file_path, "w") as file:
                file.write("False")
