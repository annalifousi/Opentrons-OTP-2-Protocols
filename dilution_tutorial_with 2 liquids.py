from opentrons import protocol_api

metadata = {
    "protocolName": "Serial Dilution with Custom Transfers",
    "description": """This protocol transfers liquid from a reservoir to the first column of a 96-well plate,
                   then uses a new tip to transfer liquid from a second reservoir to all other wells.
                   After these transfers, a serial dilution is performed across the plate.""",
    "author": "New API User"
}

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", 1)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 2)
    plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)
    trash = protocol.fixed_trash

    # Load instruments
    right_pipette = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tips])

    # Transfer liquid from reservoir "A1" to only the first column of the plate
    right_pipette.pick_up_tip()
    for well in plate.columns()[0]:
        right_pipette.transfer(100, reservoir["A1"], well, new_tip='never')
    right_pipette.drop_tip()

    # Transfer liquid from reservoir "A2" to all wells except the first column
    for col in plate.columns()[1:]:
        right_pipette.pick_up_tip()
        for well in col:
            right_pipette.transfer(100, reservoir["A2"], well, new_tip='never')
        right_pipette.drop_tip()

    # Perform serial dilution
    for i in range(8):
        row = plate.rows()[i]
        right_pipette.pick_up_tip()
        right_pipette.transfer(100, row[:11], row[1:], mix_after=(3, 50), new_tip='never')
        right_pipette.drop_tip()

