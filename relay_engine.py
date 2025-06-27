# core/relay_engine.py

import time
import uuid
from utils.logger import log_event
from utils.context_memory import ContextMemory
from agents.model_dispatcher import call_model
from agents.middleware_handler import run_middleware
from agents.metamind_overseer import MetaMind

class RelayEngine:
    def __init__(self, config):
        self.config = config
        self.session_id = str(uuid.uuid4())
        self.memory = ContextMemory()
        self.meta = MetaMind()
        self.max_loops = config.get("max_loops", 5)
        self.current_loop = 0

    def execute_chain(self, user_input):
        log_event("Session started", self.session_id)
        self.memory.store("user_input", user_input)
        prompt = user_input

        while self.current_loop < self.max_loops:
            log_event("Loop iteration", self.current_loop + 1)
            for step in self.config["chain"]:
                agent_name = step["agent"]
                middleware = step.get("middleware")

                log_event("Dispatching", f"{agent_name} with middleware: {middleware}")

                # Call the model
                output = call_model(agent_name, prompt)

                # Middleware processing
                if middleware:
                    output = run_middleware(middleware, output)

                # Store result
                self.memory.store(f"{agent_name}_output_{self.current_loop}", output)
                prompt = output  # Pass to next agent

            # MetaMind evaluates current loop
            decision = self.meta.evaluate(self.memory, self.current_loop)
            if decision == "terminate":
                log_event("Loop terminated by MetaMind", self.current_loop)
                break

            self.current_loop += 1
            time.sleep(0.25)  # simulate pacing

        return self.memory.get_latest()
