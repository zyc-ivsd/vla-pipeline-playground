# test_sim.py

from sim import ArmSimulator

if __name__ == "__main__":
    sim = ArmSimulator(gui=True)

    try:
        sim.execute_action("idle")
        sim.execute_action("pick_bottle")
        sim.execute_action("follow_person")
        sim.execute_action("idle")
    finally:
        sim.close()