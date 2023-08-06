[![CircleCI](https://circleci.com/gh/AndreaCensi/comptests.svg?style=shield)](https://circleci.com/gh/AndreaCensi/comptests)

comptests
=========

Testing utilities built on top of [ConfTools][conftools], [CompMake][compmake]
and [QuickApp][quickapp].


Basic Usage
-----------

This is the usage for packages that register objects using [ConfTools][conftools].

# Defining tests

Call the function ``comptests_for_all`` to create a decorator:

    # get the library (ObjSpec)
    library_robots = get_conftools_robots()

    # Create a test decorator
    for_all_robots = comptests_for_all(library_robots)

    # Use the decorator to specify tests. Test functions
    # must take two arguments: id object and object itself

    @for_all_robots
    def check_robot_type(id_robot, robot):
        assert isinstance(robot, RobotInterface)

You can also register tests for pairs:

    library_nuisances = get_conftools_nuisances()
    for_all_robot_nuisance_pairs = comptests_for_all_pairs(library_robots, library_nuisances)

    @for_all_robot_nuisance_pairs
    def check_nuisances_obs(id_robot, robot, id_nuisance, nuisance):
        check_conversions(robot.get_spec().get_observations(), nuisance)

# Running tests

Use the command line:

    comptests <module>

This looks for the ``get_comptests()`` function in ``<module>``:

    def get_comptests():
        get_comptests():
        # get testing configuration directory
        from pkg_resources import resource_filename
        dirname = resource_filename("boot_agents", "configs")
        # load unittests
        from . import unittests
        from comptests import get_comptests_app
        # Get the Quickapp for the boot_config
        app = get_comptests_app(get_boot_config())
        return [app]

Finding coverage information
============================

It's very usuful to use the ``coverage`` tool together with comptests.

Install the ``coverage`` tool:

    pip install coverage

If ``coverage`` is installed then comptests automatically computes
the coverage information for nosetests execution.

To do the coverage information for the comptests, run like this:

    coverage run =comptests -c "make recurse=1" <package>

Note that you cannot use parallel testing (using ``parmake``) otherwise
coverage gets confused.

This displays the results:

    coverage report -m

Then create the HTML report:

    coverage html -d outdir
