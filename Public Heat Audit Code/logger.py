
class Logger:
    
    def __init__(self, filename, max_size=100, auto_shorten=True):
        self.filename = filename
        self.max_size = max_size
        self.auto_shorten = auto_shorten

        # Checks if the log file exists, creates it otherwise
        try:
            open(self.filename, "r").close()
        except:
            self.clear()

    # Clears the log file if it exists, otherwise creates the log file
    def clear(self):
        open(self.filename, "w").close()

    # Shortens the log file to half of its maximum length, deleting earlier entries first
    def shorten(self):
        arr = None
        with open(self.filename, "r") as f:
            arr = [line for line in f]
            f.close()
        with open(self.filename, "w") as f:
            start_index = int(len(arr) - self.max_size/2)
            if(start_index > 0):
                f.write("".join(arr[start_index:]))
        f.close()

    # Logs the given message in the log file
    def log(self, message):
        print("Logging: '" + str(message) + "'")
        if(self.auto_shorten):
            with open(self.filename, "r") as f:
                num_lines = sum(1 for line in f)
                if(num_lines >= self.max_size):
                    self.shorten()
            f.close()

        with open(self.filename, "a") as f:
            f.write(message + "\n")
            f.close()

    # Logs the given message as an error
    def log_error(self, error):
        self.log("ERROR: " + error)
