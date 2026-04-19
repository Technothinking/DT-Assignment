from engine import start_session, step

def run_cli():
    session = start_session()

    while True:
        res = step(session)

        if res["type"] == "message":
            print("\n" + res["text"])

        elif res["type"] == "question":
            print("\n" + res["text"])

            for i, opt in enumerate(res["options"]):
                print(f"{i+1}. {opt}")

            while True:
                try:
                    choice = int(input("> ")) - 1
                    if 0 <= choice < len(res["options"]):
                        break
                except:
                    pass
                print("Invalid choice.")

            res = step(session, choice)

        elif res["type"] == "summary":
            print("\n--- Reflection Summary ---")
            print(res["text"])
            break

        elif res["type"] == "end":
            print(res["text"])
            break


if __name__ == "__main__":
    run_cli()