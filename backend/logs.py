from datetime import datetime

agent_logs = []


def add_log(step, status):

    agent_logs.append(
        {
            "step": step,
            "status": status,
            "time": datetime.now().strftime(
                "%H:%M:%S"
            )
        }
    )


def get_logs():
    return agent_logs


def clear_logs():
    agent_logs.clear()