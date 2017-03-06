from .core import ProjectCore
from argparse import ArgumentParser
from baelfire.application.application import Application
from baelfire.application.commands.graph.graph import Graph
from logging import getLogger

log = getLogger(__name__)


class BaelApplication(Application):
    core_cls = ProjectCore

    tasks = {
        'develop': 'bael.project.develop:Develop',
        'create': 'bael.project.develop:Create',
    }

    def create_parser(self):
        self.parser = ArgumentParser()
        self._add_task_group()
        self._add_logging_group()

    def _add_task_group(self):
        tasks = self.parser.add_argument_group(
            'Tasks',
            'Project related options',
        )

        tasks.add_argument(
            '-c',
            '--create',
            dest='create',
            help='Create full project path.',
            action="store_true",
        )
        tasks.add_argument(
            '-d',
            '--develop',
            dest='develop',
            help='Download requiretments.',
            action="store_true",
        )
        tasks.add_argument(
            '-g',
            '--graph',
            dest='graph',
            help='Draw task dependency graph.',
            action="store_true",
        )

    def run_command_or_print_help(self, args):
        if args.create or args.develop:
            task = self._get_task(args)
            try:
                try:
                    task.run()
                finally:
                    report_path = task.save_report()
            except:
                log.error('Error in %s' % (report_path,))
                raise
            if args.graph:
                Graph(report_path).render()
        elif args.graph:
            Graph(self.get_graph_path()).render()
        else:
            self.parser.print_help()

    def get_graph_path(self):
        core = self.core_cls()
        core.init()
        core.phase_settings()
        return core.paths.get('report')

    def _get_task(self, args):
        if args.create:
            return self.import_task(self.tasks['create'])(self.core_cls())
        elif args.develop:
            return self.import_task(self.tasks['develop'])(self.core_cls())
        else:
            raise RuntimeError('No task selected!')


def run():
    BaelApplication().run()
