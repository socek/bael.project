from baelfire.recipe import Recipe

from .tasks import (
    Create,
    SetupPy,
    GatherData,
    Directories,
    Inits,
)

from .git import (
    Ignore,
    Init,
    Commit,
)


class ProjectRecipe(Recipe):

    def gather_recipes(self):
        self.add_task(Create())
        self.add_task(SetupPy())
        self.add_task(GatherData())
        self.add_task(Directories())
        self.add_task(Inits())
        self.add_task(Ignore())
        self.add_task(Init())
        self.add_task(Commit())
