import cript


def test_create_group():
    """
    simply tests if a valid group node can be created
    """
    my_group = cript.Group(name="my_group", admin="Navid Hariri")
    print(f"\n \n \n ADMINS IS: {my_group.admins} \n \n \n")

    my_group.admins = "Kobe Bryant"

    print(f"\n \n \n ADMINS IS: {my_group.admins} \n \n \n")
