import os

from PyInquirer import style_from_dict, Token, prompt, Separator
from argparse import ArgumentParser, Namespace
from typing import Callable, Dict, List


class ArgChooser:

    reserved: List = ['-A', '--all']
    category_print_style: str = '== {} =='
    default_category_name: str = 'Other'
    validation_error: str = 'You must choose at least one module.'
    validation_func: Callable
    style: Dict = {
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '#673ab7 bold',
        Token.Answer: '#f44336 bold',
        Token.Question: '#673ab7 bold',
        Token.Error: '#ff0000 bold'
    }

    def __init__(self,
                 category_style: str = None,
                 default_category_name: str = None,
                 style: Dict = None,
                 validation_func: Callable = None,
                 validation_error: str = None) -> None:

        self.parser: ArgumentParser = ArgumentParser()
        self.args: Dict = {}
        self.parsed_args: Dict = {}
        self.categories: Dict = {}

        if category_style is not None:
            self.change_category_formatting(category_style)
        if default_category_name is not None:
            self.change_default_category_name(default_category_name)
        if style is not None:
            self.change_style(style)
        if validation_func is not None:
            self.validation_func = validation_func
        else:
            self.validation_func = getattr(self, 'validate_answer')
        if validation_error is not None:
            self.change_validation_error(validation_error)

        self.create_default_categories()
        self.add_run_all()

    def create_default_categories(self) -> None:
        self.categories['All'] = [Separator(self.format_category_style('All'))]
        self.categories[self.default_category_name] = [Separator(self.format_category_style(self.default_category_name))]

    def add_run_all(self) -> None:
        self.parser.add_argument('-A', '--all', help='execute all methods', action='store_true')
        self.args['all'] = None
        self.add_to_category(
            self.create_new_element('all', 'execute all methods'),
            'All'
        )

    def change_category_formatting(self, category_style: str) -> None:
        self.category_print_style = category_style

    def change_style(self, style: Dict) -> None:
        self.style.update(style)

    def change_validation_error(self, validation_error: str) -> None:
        self.validation_error = validation_error

    def change_default_category_name(self, default_category_name: str) -> None:
        self.default_category_name = default_category_name

    def add_argument(self, *flags: str, help: str = None, category: str = None, method: Callable) -> None:
        if flags[0] not in self.reserved:
            self.parser.add_argument(*flags, help=help, action='store_true')
            self.args[flags[-1].replace('-', '')] = method
            self.add_to_category(
                self.create_new_element(flags[-1].replace('-', ''), help),
                category
            )
        else:
            raise ValueError("Value -A and -all is reserved for 'run_all' function.")

    def create_new_element(self, flag: str, help: str) -> Dict:
        if help is not None:
            return {
                'name': flag + ' - ' + help
            }
        else:
            return {
                'name': flag
            }

    def add_to_category(self, new_element: Dict, category: str) -> None:
        if category is not None:
            self.add_to_named_category(new_element, category)
        else:
            self.add_to_unnamed_category(new_element)

    def add_to_named_category(self, new_element: Dict, category: str) -> None:
        if category not in self.categories:
            self.add_to_new_category(new_element, category)
        else:
            self.add_to_existing_category(new_element, category)

    def add_to_unnamed_category(self, new_element: Dict) -> None:
        self.categories[self.default_category_name].append(new_element)

    def add_to_new_category(self, new_element: Dict, category: str) -> None:
        self.categories[category] = [
            Separator(self.format_category_style(category)),
            new_element
        ]

    def add_to_existing_category(self, new_element: Dict, category: str) -> None:
        self.categories[category].append(new_element)

    def format_category_style(self, category: str) -> str:
        return self.category_print_style.format(category)

    def execute(self) -> None:
        self.parse_args()
        self.decide_action()

    def parse_args(self) -> None:
        parsed_args: Namespace = self.parser.parse_args()
        self.parsed_args = dict(filter(lambda key: parsed_args.__dict__[key[0]] is True, self.args.items()))

    def decide_action(self) -> None:
        if not self.parsed_args:
            self.run_menu()
        elif 'all' in self.parsed_args:
            self.run_all()
        else:
            self.run_chosen()

    def run_all(self) -> None:
        del self.args['all']
        for func in self.args.values():
            func()

    def run_chosen(self) -> None:
        if 'all' in self.parsed_args.keys() or self.validation_func(list(self.parsed_args.keys())):
            for func in self.parsed_args.values():
                func()
        else:
            print(self.validation_error)

    def run_menu(self) -> None:
        choices: List = self.create_choices()
        questions: List = self.create_questions(choices)
        while True:
            answers = prompt(questions, style=style_from_dict(self.style))
            if 'all' in answers['Modules'] or self.validation_func(answers['Modules']):
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.validation_error)
        self.parse_menu_args(answers['Modules'])
        self.decide_action()

    def create_choices(self) -> List:
        choices = []
        # Move uncategorized section to the end
        self.categories[self.default_category_name] = self.categories.pop(self.default_category_name)

        for values in self.categories.values():
            choices.extend(values)
        return choices

    def create_questions(self, choices: List) -> List:
        return [{
            'type': 'checkbox',
            'message': 'Select modules',
            'name': 'Modules',
            'choices': choices,
            'filter': lambda answers: [answer.split(' ', 1)[0] for answer in answers],
            # 'validate': lambda answer: 'You must choose at least one module.' if len(answer) == 0 else True
        }]

    # TODO use built-in validation in PyInquirer after merging fix from #PR117 and releasing new version
    def validate_answer(self, answers: List) -> bool:
        return True if len(answers) > 0 else False

    def parse_menu_args(self, chosen_args: List) -> None:
        self.parsed_args = dict(filter(lambda key: key[0] in chosen_args, self.args.items()))
