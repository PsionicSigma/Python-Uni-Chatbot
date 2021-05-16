#file for dialog logging module



class Dialog_Logger:
    def __init__(self, bot_id):
        #init new logger for new dialog
        self.bot_id = bot_id
        self.dialog_history = []
    
    def log_querry(querry_set):
        #add a querry'n'response set to bots current dialog history
        dialog_history.append(querry_set)