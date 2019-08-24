# First testing of Monopoly simulations

import MonoSim
# import Visualizer
# import random


if __name__ == "__main__":

    sim = MonoSim.Simulation(num_players=2, logging=True)

    # sim.run_sim()

    out = sim.step_sim({"next player": 0})
    while sim.turn_counter < 50:
        # print(out["next player"])
        out = sim.step_sim(out)

    sim.players.sort(key=str)
    print("Simulation complete\n")

    # for i in sim.players:
    #     sim.Reporter.laps_report(sim, i)
    # sim.Reporter.landing_report(sim, sim.players)

