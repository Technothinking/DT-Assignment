import json

# ---------- LOAD TREE ----------
with open("../tree/reflection-tree.json", "r", encoding="utf-8") as f:
    tree_data = json.load(f)

tree = {node["id"]: node for node in tree_data["nodes"]}

# ---------- STATE ----------
state = {
    "answers": {},
    "axis1": {"internal": 0, "external": 0},
    "axis2": {"contribution": 0, "entitlement": 0},
    "axis3": {"self": 0, "others": 0}
}

# ---------- SIGNAL HANDLER ----------
def apply_signal(signal):
    if not signal:
        return
    axis, value = signal.split(":")
    state[axis][value] += 1

def apply_signal_map(node, selected_option):
    if "signalMap" in node:
        signal = node["signalMap"].get(selected_option)
        apply_signal(signal)

# ---------- CONDITION EVALUATOR ----------
def evaluate_condition(condition):
    # Example: "axis1.internal >= axis1.external"
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

# ---------- TEXT INTERPOLATION ----------
def interpolate(text):
    for key, value in state["answers"].items():
        placeholder = "{" + key + ".answer}"
        text = text.replace(placeholder, value)
    return text

# ---------- ENGINE ----------
def run():
    current = "START"

    while True:
        node = tree[current]

        # Apply direct signal (if exists)
        if "signal" in node:
            apply_signal(node["signal"])

        # ---- START ----
        if node["type"] == "start":
            print("\n" + node["text"])
            current = node["next"]

        # ---- QUESTION ----
        elif node["type"] == "question":
            print("\n" + interpolate(node["text"]))

            for i, opt in enumerate(node["options"]):
                print(f"{i+1}. {opt}")

            while True:
                try:
                    choice = int(input("> ")) - 1
                    if 0 <= choice < len(node["options"]):
                        break
                except:
                    pass
                print("Invalid choice. Try again.")

            selected = node["options"][choice]
            state["answers"][node["id"]] = selected

            # Apply signal from option
            apply_signal_map(node, selected)

            # Routing
            if "nextMap" in node:
                current = node["nextMap"][selected]
            else:
                current = node["next"]

        # ---- DECISION ----
        elif node["type"] == "decision":
            for cond in node["conditions"]:
                if evaluate_condition(cond["if"]):
                    current = cond["goto"]
                    break

        # ---- REFLECTION ----
        elif node["type"] == "reflection":
            print("\n" + interpolate(node["text"]))
            input("\n(Press Enter to continue)")
            current = node["next"]

        # ---- BRIDGE ----
        elif node["type"] == "bridge":
            print("\n" + node["text"])
            input("\n(Press Enter to continue)")
            current = node["next"]

        # ---- SUMMARY ----
        elif node["type"] == "summary":
            print("\n--- Reflection Summary ---")
            print(generate_summary())
            current = node["next"]

        # ---- END ----
        elif node["type"] == "end":
            print("\nSession complete. See you tomorrow.")
            break


# ---------- SUMMARY GENERATOR ----------
def dominant(axis):
    data = state[axis]
    return max(data, key=data.get)

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

def generate_summary():
    a1 = dominant("axis1")
    a2 = dominant("axis2")
    a3 = dominant("axis3")

    summary = f"""
    You approached the day with {axis1_text(a1)} — shaping how you responded to what happened.

    In your interactions, you leaned toward {axis2_text(a2)}.

    Your perspective centered more on {axis3_text(a3)}.

    Taken together, this influences not just what you did today — but how the day felt.

    Tomorrow, even a small shift in one of these can change the entire experience.
    """
    if a1 == "external" and a2 == "entitlement":
        extra = "\nThere may have been moments where things felt outside your control and others didn’t step up. That combination can feel heavy — but it also hides small opportunities to act."
    else:
        extra = ""

    return summary


# ---------- RUN ----------
if __name__ == "__main__":
    run()