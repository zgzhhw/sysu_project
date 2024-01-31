import threading
import random

class Paxos:
    def __init__(self, server, proposal_id=0, accepted_proposal=None, accepted_value=None):
        self.server = server
        self.proposal_id = proposal_id
        self.accepted_proposal = accepted_proposal
        self.accepted_value = accepted_value
        self.lock = threading.Lock()
        

    def prepare(self, proposal_id):
        with self.lock:
            if proposal_id > self.proposal_id:
                self.proposal_id = proposal_id
                return True, self.accepted_proposal, self.accepted_value
            else:
                return False, None, None

    def accept(self, proposal_id, value):
        with self.lock:
            if proposal_id >= self.proposal_id:
                self.proposal_id = proposal_id
                self.accepted_proposal = proposal_id
                self.accepted_value = value
                return True
            else:
                return False

    def decide(self, value):
        with self.lock:
            print(f"Paxos decided: {value}")
            # 在这里调用服务器方法执行决策的动作

class PaxosServer:
    def __init__(self, server_id):
        self.server_id = server_id
        self.paxos_instance = Paxos(self)
        self.MAX_ID = 0

    def run_paxos(self, proposal_id, value):
        prepare_result, prev_proposal, prev_value = self.paxos_instance.prepare(proposal_id)

        if prepare_result:
            accept_result = self.paxos_instance.accept(proposal_id, value)

            if accept_result:
                self.paxos_instance.decide(value)

    def generate_id(self):
        val = random.randint(self.MAX_ID+1, self.MAX_ID + 10)
        self.MAX_ID = val
        return val