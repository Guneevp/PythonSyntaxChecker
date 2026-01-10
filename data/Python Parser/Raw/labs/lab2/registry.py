from itertools import accumulate


class Runner:
    """
    A class designed to hold runner information in an easy-to-access way.
    Runner's are identified by their name.

    === Attributes ===
    name:
        The self identified name of the runner. This is used as the id
        of each runner
    _email:
        The runner's email address. This variable may be edited later
    _speed:
        The runner's given speed category. This speed category is interpretted
        by the registry class that contains this runner in order to
        properly interpret the speed



    >>> David = Runner("David Cobo", "123@mail.com", 3)
    """
    def __init__(self, name: str, email: str, speed: int):
        self.name = name
        self._email = email
        self._category = speed

    def __repr__(self):
        return f"{self.name}"

    def edit(self, new_email: str = "", new_speed: int = 0) -> bool:
        """
        A simple function to change runner information
        """
        change = False
        if new_email:
            self._email = new_email
            change = True
        if new_speed:
            self._category = new_speed
            change = True
        return change


class Registry:
    """
    The class that holds all runner information and allows runners
    to change their email, category or withdraw from the race.

    The Registry starts empty.

    === Attributes ===
    runners:
        A list that contains all the runners registered for the race.
    group*i:
        Each argument passed to the constructor will result in an additional
        attribute being created that will store the description of that category

    There are 4 expected values for the speed attribute.
    ========
    speed == 0 -> Under twenty minutes
    speed == 1 -> Under thirty minutes
    speed == 2 -> Under forty minutes
    speed == 3 ->  Forty minutes or over
    ========

    >>> FiveK = Registry()
    >>> FiveK.register("David", "email", 4)
    >>> print(FiveK)
    "There are 1 runners in the race."
    >>> FiveK.withdraw("David")
    >>> print(FiveK)
    "There are 0 runners in the race."
    >>> FiveK.change_speed("David", 2)
    True
    >>> FiveK.make_group(4)
    [

    """
    runners: list[Runner]
    groups: str

    def __init__(self, *args: str) -> None:
        self.runners = []
        self.groups = *args

    def register(self, name: str, email: str, speed: int) -> None:
        self.runners.append(Runner(name, email, speed))


    def withdraw(self, name: str) -> None:
        for i in self.runners:
            if i.name == name:
                self.runners.remove(i)


    def make_group(self, speed: int = 0) -> list:
        accumulate = []
        for runner in self.runners:
            if runner._category == speed or int == 0:
                accumulate.append(runner)
        return accumulate


    def edit(self, name, new_email: str = "", new_speed: int = 0) -> bool:
        """
        A method to find and change a runner's self identified
        speed category. Returns False if no runner is found
        and no speed category is changed, True otherwise.
        """
        change = False
        for runner in self.runners:
            if runner.name == name:
                if new_email:
                    change = True
                    runner.edi new_email
                if new_speed:
                    runner._category = new_speed
                    change = True
        return change


    def lookup(self, name) -> str:
        for runner in self.runners:
            if runner.name == name:
                if runner._category == 1:
