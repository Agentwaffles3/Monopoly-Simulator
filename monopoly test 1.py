# First testing of Monopoly simulations

import MonoSim


if __name__ == "__main__":

    sim = MonoSim.Simulation(num_players=4, logging=True)
    sim.players.sort(key=str)
    print("Simulation complete\n")
    
#    for n in sim.Bank.properties:
#        print(n.propName)
#    print(sim.look_up["5"])
#     for i in sim.players:
#         print (i)
    # Return simulation results
    # sim.logger("Doubles rolled\n")
    # for i in sim.players:
    #     sim.Reporter.doubles_report(sim, i)
    #
    # sim.logger("\nTimes jailed\n")
    # for i in sim.players:
    #     sim.Reporter.jail_report(sim, i)
    #
    # sim.logger("\nLaps completed\n")
    # for i in sim.players:
    #     sim.Reporter.laps_report(sim, i)

    # print("\nTimes landed on each space\n")
    # sim.Reporter.landing_report(sim.players)
