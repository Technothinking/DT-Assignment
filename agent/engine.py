import json
import copy
import os

# Loading the Tree
def load_tree():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tree_path = os.path.join(script_dir, "..", "tree", "reflection-tree.json")
    
    with open(tree_path, "r", encoding="utf-8") as f:
        tree_data = json.load(f)
    return {node["id"]: node for node in tree_data["nodes"]}


def init_state():
    return {
        "answers": {},
        "axis1": {"internal": 0, "external": 0},
        "axis2": {"contribution": 0, "entitlement": 0},
        "axis3": {"self": 0, "others": 0}
    }


def apply_signal(state, signal):
    if not signal:
        return
    axis, value = signal.split(":")
    state[axis][value] += 1


def apply_signal_map(state, node, selected_option):
    if "signalMap" in node:
        signal = node["signalMap"].get(selected_option)
        apply_signal(state, signal)


def evaluate_condition(state, condition):
    left, op, right = condition.split()

    def get_value(expr):
        axis, key = expr.split(".")
        return state[axis][key]

    l_val = get_value(left)
    r_val = get_value(right)

    if op == ">=":
        return l_val >= r_val
    elif op == ">":
        return l_val > r_val
    elif op == "==":
        return l_val == r_val
    elif op == "<":
        return l_val < r_val
    elif op == "<=":
        return l_val <= r_val

    return False


def interpolate(state, text):
    for key, value in state["answers"].items():
        placeholder = "{" + key + ".answer}"
        text = text.replace(placeholder, value)
    
    # Map axis dominants to their narrative descriptions
    axis1_map = {
        "internal": "a sense of control",
        "external": "a pull from external circumstances"
    }
    axis2_map = {
        "contribution": "contributing and moving things forward",
        "entitlement": "noticing gaps in what others were doing"
    }
    axis3_map = {
        "self": "your own experience",
        "others": "how your actions affected others"
    }
    
    a1_dominant = dominant(state, "axis1")
    a2_dominant = dominant(state, "axis2")
    a3_dominant = dominant(state, "axis3")
    
    text = text.replace("{axis1.text}", axis1_map[a1_dominant])
    text = text.replace("{axis2.text}", axis2_map[a2_dominant])
    text = text.replace("{axis3.text}", axis3_map[a3_dominant])
    
    return text


# Generate summary
def dominant(state, axis):
    return max(state[axis], key=state[axis].get)


def generate_summary(state):
    def axis1_text(val):
        return {
            "internal": "a sense of control",
            "external": "a pull from external circumstances"
        }[val]

    def axis2_text(val):
        return {
            "contribution": "contributing and moving things forward",
            "entitlement": "noticing gaps in what others were doing"
        }[val]

    def axis3_text(val):
        return {
            "self": "your own experience",
            "others": "how your actions affected others"
        }[val]

    a1 = dominant(state, "axis1")
    a2 = dominant(state, "axis2")
    a3 = dominant(state, "axis3")

    summary = f"""
    You approached the day with {axis1_text(a1)}.

    You leaned toward {axis2_text(a2)}.

    Your perspective centered more on {axis3_text(a3)}.

    A small shift tomorrow can change the entire experience.
    """

    return summary.strip()


def start_session():
    tree = load_tree()
    state = init_state()

    return {
        "current": "START",
        "state": state,
        "tree": tree,
        "trace": []
    }


def step(session, user_input=None):
    tree = session["tree"]
    state = session["state"]
    current = session["current"]
    trace = session["trace"]

    node = tree[current]

    if "signal" in node:
        apply_signal(state, node["signal"])
        trace.append(f"Applied signal: {node['signal']}")

    if node["type"] == "start":
        session["current"] = node["next"]
        return {
            "type": "message",
            "text": node["text"]
        }

    elif node["type"] == "question":
        if user_input is None:
            return {
                "type": "question",
                "text": interpolate(state, node["text"]),
                "options": node["options"]
            }

        selected = node["options"][user_input]
        state["answers"][node["id"]] = selected

        apply_signal_map(state, node, selected)
        trace.append(f"Selected: {selected}")

        if "nextMap" in node:
            session["current"] = node["nextMap"][selected]
        else:
            session["current"] = node["next"]

        return step(session)

    elif node["type"] == "decision":
        for cond in node["conditions"]:
            if evaluate_condition(state, cond["if"]):
                session["current"] = cond["goto"]
                trace.append(f"Condition matched: {cond['if']}")
                return step(session)

    elif node["type"] in ["reflection", "bridge"]:
        session["current"] = node["next"]
        return {
            "type": "message",
            "text": interpolate(state, node["text"])
        }

    elif node["type"] == "summary":
        session["current"] = node["next"]

        return {
            "type": "summary",
            "text": interpolate(state, node["text"]),
            "trace": trace,
            "state": state
        }

    elif node["type"] == "end":
        return {
            "type": "end",
            "text": node["text"]
        }