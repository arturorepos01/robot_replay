class ReplayContext:

    def __init__(self):

        self.browser = None
        self.page = None
        self.current_state = None
        self.current_url = ""
        self.last_action = None
        self.flow_id = ""
        self.retry = 0
        self.statistics = {}
        self.errors = []
        self.driver = None
        self.credentials = None