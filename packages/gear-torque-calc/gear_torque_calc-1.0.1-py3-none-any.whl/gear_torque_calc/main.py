length_unit = "mm"
torque_unit = "nm"


def get_torque(
    drive_shaft_diameter=5,
    drive_shaft_torque=0.2,
    gear_small_diameter=15,
    gear_large_diameter=55,
):
    drive_shaft_radius = drive_shaft_diameter * 0.5
    gear_large_radius = gear_large_diameter * 0.5
    gear_small_radius = gear_small_diameter * 0.5

    response = dict(
        motor=dict(torque=drive_shaft_torque),
        small_gear=dict(radius=gear_small_radius,),
        large_gear=dict(radius=gear_large_radius,),
        gear_ratio=gear_large_radius / gear_small_radius,
    )

    drive_shaft_radius_meters = drive_shaft_radius / 1000
    motor_force = drive_shaft_torque / drive_shaft_radius_meters
    response["motor"]["force"] = motor_force
    response["small_gear"]["force"] = drive_shaft_torque / gear_small_radius * 1000
    response["small_gear"]["torque"] = (
        response["small_gear"]["force"] * gear_small_radius / 1000
    )

    response["large_gear"]["torque"] = (
        response["gear_ratio"] * response["small_gear"]["torque"]
    )
    response["large_gear"]["force"] = (
        response["large_gear"]["torque"] / gear_large_radius * 1000
    )

    return response
