from abc import abstractmethod
from typing import List, Tuple, Set
from pypdf import PdfReader
import sys
import random

class Street:
    """ Template class for Street objects """
    def __init__(self, full_name, classification):
        self.name = ""
        full_name_list = full_name.split(' ')
        street_suffix_index = -1
        for type in street_types:
            try:
                street_suffix_index = full_name_list.index(type)
            except ValueError:
                continue
            else:
                break

        for i in range(0, street_suffix_index, 1):
            if i == 0:
                self.name += full_name_list[i]
            else:
                self.name += f" {full_name_list[i]}"

        if street_suffix_index != len(full_name_list) - 1: # Direction: N, S, W, E
            self.name +=  f" {full_name_list[-1]}"

        self.street_type = full_name_list[street_suffix_index]
        self.classification = classification

    def get_name(self):
        return self.name

    def get_street_type(self):
        return self.street_type

    def get_classification(self):
        return self.classification

    @abstractmethod
    def __str__(self):
        pass

class SameFromAndToStreet (Street):
    """ Template class for Streets with the same from and to streets (ends) """
    def __init__(self, full_name, ends, classification):
        Street.__init__(self, full_name, classification)
        self.ends = ''

        ends_list = ends.split(' ')

        street_suffix_index = -1

        for type in street_types:
            try:
                street_suffix_index = ends_list.index(type)
            except ValueError:
                continue
            else:
                break

        for i in range(0, street_suffix_index, 1):
            if i == 0:
                self.ends += ends_list[i]
            else:
                self.ends += f" {ends_list[i]}"

        if street_suffix_index != len(ends_list) - 1:  # Direction: N, S, W, E
            self.ends += f" {ends_list[-1]}"

    def get_ends(self):
        return self.ends

    def __str__(self):
        returned = "-" * 15
        returned += f'Full name: {self.get_name()}\n'
        returned += f'Ends: {self.get_ends()}\n'
        returned += f'Classification: {self.get_classification()}\n'
        returned += "-" * 15
        return returned

class DifferentFromAndToStreet (Street):
    """ Template class for Streets with different from and to streets """
    def __init__(self, full_name, _from, _to, classification):
        Street.__init__(self, full_name, classification)
        self.from_street = ''
        self.to_street = ''
        _from_list = _from.split(' ')

        street_suffix_index = -1

        for type in street_types:
            try:
                street_suffix_index = _from_list.index(type)
            except ValueError:
                continue
            else:
                break

        for i in range(0, street_suffix_index, 1):
            if i == 0:
                self.from_street += _from_list[i]
            else:
                self.from_street += f" {_from_list[i]}"

        if street_suffix_index != len(_from_list) - 1:  # Direction: N, S, W, E
            self.from_street += f" {_from_list[-1]}"

        _to_list = _to.split(' ')
        for type in street_types:
            try:
                street_suffix_index = _to_list.index(type)
            except ValueError:
                continue
            else:
                break

        for i in range(0, street_suffix_index, 1):
            if i == 0:
                self.to_street += _to_list[i]
            else:
                self.to_street += f" {_to_list[i]}"

        if street_suffix_index != len(_to_list) - 1:  # Direction: N, S, W, E
            self.to_street += f" {_to_list[-1]}"

    def get_from_street(self):
        return self.from_street

    def get_to_street(self):
        return self.to_street

    def __str__(self):
        returned = "-" * 15
        returned += f'Full name: {self.get_name()}\n'
        returned += f'From: {self.get_from_street()}\n'
        returned += f'To: {self.get_to_street()}\n'
        returned += f'Classification: {self.get_classification()}\n'
        returned += "-" * 15
        return returned

street_types = [' ave ', ' bdge ', ' blvd ', ' crcl ', ' crct ', ' cres ', ' crt ', ' cs ',
                ' dr ', ' gdns ', ' grv ', ' gt ', ' hill ', ' hts ',
                ' lane ', ' line ', ' lwn ', ' mews ', ' path ', ' pk ',
                ' pkwy ', ' pl ', ' ramp ', ' rd ', ' rdwy ', ' sq ',
                ' st ', ' ter ', ' trl ', ' view ', ' walk ', ' way ',
                ' wds ', ' wood ', ' parkway ', ' roadway '
                ]
basic_streets: List[str] = []
detailed_streets: List[Street] = []

def get_basic_street_database() -> None:
    """
    Gets a list of streets found in the PDF, which only stores street names
    """
    try:
        reader = PdfReader('toronto streets.pdf')
    except:
        print('Sorry, \'toronto streets.pdf\' cannot be found, on which this program is run.')
        quit()
    else:
        print('Loading database...')
    for i in range(8, 47):
        text: str = reader.pages[i].extract_text()

        text_list = text.split('\n')
        for i in range(len(text_list) - 1, -1, -1):
            text_list[i] = text_list[i].strip()
            qualifies = False
            for type in street_types:
                if type in text_list[i].lower():
                    qualifies = True
            if not qualifies:
                text_list.pop(i)

        for e in text_list:
            if e.lower().find(get_street_type(e)) + len(get_street_type(e)) - 1 == e.lower().find(' n ') \
                    or e.lower().find(get_street_type(e)) + len(get_street_type(e)) - 1 == e.lower().find(' s ') \
                    or e.lower().find(get_street_type(e)) + len(get_street_type(e)) - 1 == e.lower().find(' w ')\
                    or e.lower().find(get_street_type(e)) + len(get_street_type(e)) -1 == e.lower().find(' e '):
                basic_streets.append(e[:e.lower().find(get_street_type(e)) + len(get_street_type(e)) + 2].strip())
            else:
                basic_streets.append(e[:e.lower().find(get_street_type(e)) + len(get_street_type(e)) - 1].strip())
    pass

def get_street_type(text: str) -> str:
    """ Filter other information in passed text to get the basic type of the street for completing basic_streets """
    all_street_suffixes = set()
    text = text.lower()
    for type in street_types:
        if text.find(type) >= 0:
            all_street_suffixes.add(type)

    if len(all_street_suffixes) == 1:
        return tuple(all_street_suffixes)[0]

    suffix = ''
    suffix_index = sys.maxsize
    for s in all_street_suffixes:
        if suffix_index > text.find(s):
            suffix = s
            suffix_index = text.find(s)

    return suffix

def get_street_type_order(text: str) -> Tuple[int]:
    """ Find the order of street types found in the passed text """
    order = []
    text = text.lower()
    for type in street_types:
        start = 0
        while text.find(type, start) >= 0:
            if type == ' st ': # Discerning st as for Street and Saint
                is_saint = False
                checked_pos = text.find(type, start)

                # Check for types
                for type2 in street_types:
                    checked_text = text[text.find(type, start) - len(type2) + 1:text.find(type, start) + 1]
                    if checked_text == type2:
                        is_saint = True
                        break

                # Check for directions
                directions = ' n ', ' w ', ' e ', ' s '
                for dir in directions:
                    checked_text = text[text.find(type, start) - len(dir) + 1:text.find(type, start) + 1]
                    if checked_text == dir:
                        is_saint = True
                        break

                if not is_saint:
                    order.append(text.find(type, start))
            elif type == ' hill ' or type == ' parkway ': # Parkview Hill Cres, and Parkway Forest Dr are exceptions
                is_name = False
                checked_pos = text.find(type, start)
                for type2 in street_types:
                    checked_text = text[text.find(type, start) + len(type) - 1:text.find(type, start) + len(type) - 1 + len(type2)]
                    if checked_text == type2:
                        is_name = True
                        break
                if not is_name:
                    order.append(text.find(type, start))
            else:
                order.append(text.find(type, start))
            start = text.find(type, start) + 1
    order = list(set(order))
    order.sort()
    return tuple(order)

def get_type (street_name: str) -> str:
    """ Get the type of the street in basic_streets (already filtered) """
    assert isinstance(street_name, str), 'street_name is not a string'
    street_name = street_name.strip()
    streets_copy = None
    if len(basic_streets) == 0:
        get_basic_street_database()
    streets_copy = basic_streets.copy()
    if street_name.find('the ') == 0:
        streets_copy.sort()
    street_index = binary_search_str(street_name, streets_copy)
    if street_index < 0:
        return 'N/A'
    for type in street_types:
        if type.strip() in streets_copy[street_index].lower().split(' '):
            return type.strip().capitalize() # No whitespaces
    return 'N/A'


def binary_search_str (element, li, min=0, max=None) -> int:
    assert isinstance(li, list), 'li is not a list'
    if len(li) == 0:
        return -1

    assert isinstance(min, int), f'min is not an integer'
    if max == None:
        max = len(li) - 1
    else:
        assert isinstance(max, int), f'max is not an integer'

    if max >= min:
        mid = (min + max) // 2
        if li[mid].lower() == element.lower() or element.lower() in li[mid].lower():
            return mid
        elif element.lower() < li[mid].lower():
            return binary_search_str(element, li, min, mid - 1)
        elif element.lower() > li[mid].lower():
            return binary_search_str(element, li, mid + 1, max)
    else:
        return -1

def get_streets_of_type (type: str, amount: int = 4) -> List[str]:
    """ Return a list of [amount] streets of passed [type] """
    assert isinstance(type, str), 'type is not a string'
    type = type.strip().lower()
    assert f' {type} ' in street_types, 'type is not a street type'
    assert isinstance(amount, int) and amount > 0, 'amount is not a positive integer'
    street_set = set(basic_streets)
    returned_list = []
    for street in street_set:
        if get_type(street).lower().strip() == type:
            returned_list.append(street)
            if len(returned_list) >= amount:
                break
    return returned_list


class Question:
    """ Question in a Quiz """
    def __init__(self, q_type: str, num_of_ans: int = 0, street: str = None):
        """
        Generates a question based on a street.

        Parameters:
            q_type (str): The question type: either 'street' or 'type'. 'street' questions challenge users to pick the
                correct street with a given street type, and 'type' questions challenge users to pick the correct
                street type for a given street.
            num_of_ans (int): The number of possible answers in the question
            street (str): A street in basic_streets. When no arguments are passed, it is randomly
                picked from the aforementioned list.
        """
        assert q_type.lower().strip() == 'street' or q_type.lower() == 'type', 'q_type is not \'street\' nor \'type\''
        assert isinstance(num_of_ans, int) and (num_of_ans >= 2 or num_of_ans == 0), 'num_of_ans is not an integer above 2 nor it is 0'
        if street == None:
            street = basic_streets[random.randint(0, len(basic_streets) - 1)]
        assert isinstance(street, str), 'street is not a string'
        self.street = street
        self.street_type = get_type(street)
        self.q_type = q_type.lower().strip()
        self.answers = set()
        self.ordered_ans = list(self.answers)

        if num_of_ans == 0:
            return;

        match self.q_type:
            case 'street':
                self.answers.add(self.street.title())
                self.answers = self.answers.union(self.get_random_streets(num_of_ans - 1))
                pass
            case 'type':
                self.answers.add(self.street_type.title())
                self.answers = self.answers.union(self.get_random_types(num_of_ans - 1))
                pass

        self.ordered_ans = list(self.answers)

    def get_random_types(self, n: int = 1) -> Set[str]:
        """ Get a set of n random types that are not self.street_type """
        assert isinstance(n, int) and n > 0, 'n is a positive integer'
        types_set = set(street_types.copy())
        random_types = set()
        while len(random_types) < n:
            item = types_set.pop()
            if item.strip().lower() != self.street_type.strip().lower():
                random_types.add(item.strip().lower().capitalize())
        return random_types

    def get_random_streets(self, n: int = 1) -> Set[str]:
        """ Get a set of n random streets that are not of self.street_type """
        assert isinstance(n, int) and n > 0, 'n is a positive integer'
        random_streets = set()
        types_set = set(street_types.copy())
        while len(random_streets) < n:
            item = types_set.pop()
            if item.strip().lower() != self.street_type.strip().lower():
                how_many_times = random.randint(1, n - len(random_streets))
                random_streets = random_streets.union(get_streets_of_type(item, how_many_times))
        return random_streets

    def get_answer_len(self) -> int:
        return len(self.ordered_ans)

    def shuffle_answers(self) -> None:
        self.ordered_ans = list(self.answers)

    def render_question(self) -> str:
        """ Renders the Question object into text and returns it """
        string = 'QUESTION: '
        match self.q_type:
            case 'street':
                if len(self.ordered_ans) > 0:
                    string += f'Which of the following streets is of type {self.street_type}?\n'
                    for i in range(len(self.ordered_ans)):
                        string += f'{i + 1}. {self.remove_type_from_answer(self.ordered_ans[i])}\n'
                else:
                    string += f'Which street in Toronto is of type {self.street_type}?'
            case 'type':
                if len(self.ordered_ans) > 0:
                    string += f'Which street type is {self.remove_type_from_answer(self.street)}?\n'
                    for i in range(len(self.ordered_ans)):
                        string += f'{i + 1}. {self.ordered_ans[i]}\n'
                else:
                    string += f'Which street type is {self.remove_type_from_answer(self.street)}?'
        return string

    def get_question_type(self):
        return self.q_type

    def get_street(self):
        return self.street

    def get_street_type(self):
        return self.street_type

    def get_correct_answer(self):
        match self.q_type:
            case 'street':
                if len(self.ordered_ans) != 0:
                    return str(self.ordered_ans.index(self.street) + 1)
                return self.street_type
            case 'type':
                if len(self.ordered_ans) != 0:
                    return str(self.ordered_ans.index(self.street_type) + 1)
                return self.street_type
        return None

    def remove_type_from_answer (self, answer: str) -> str:
        answer_street_type = get_type(answer).strip().lower()
        answer = answer.lower().split(' ')
        answer.remove(answer_street_type)
        return ' '.join(answer)

    def __str__(self):
        string = '**********************************************\n'
        string += f'QUESTION:\nSTREET: {self.street}\nSTREET TYPE: {self.street_type}\n'
        string += f'QUESTION TYPE: {self.q_type}\nANSWERS: {self.answers}\n'
        string += '**********************************************'
        return string

class Quiz:
    def __init__(self, num_of_questions: int = 1):
        assert isinstance(num_of_questions, int) and num_of_questions > 0, 'num_of_questions is not a positive integer'
        self.questions: List[Question] = []
        self.score = 0
        for i in range(num_of_questions):
            # 0 is free-response street-type, 1 is multiple choice street-type
            # 2 is free-response type-type, 3 is multiple choice type-type
            pick_type = random.randint(0, 3)
            match pick_type:
                case 0:
                    self.questions.append(Question('street'))
                case 1:
                    self.questions.append(Question('street', random.randint(2, 6)))
                case 2:
                    self.questions.append(Question('type'))
                case 3:
                    self.questions.append(Question('type', random.randint(2, 6)))

    def get_user_answer(self, question: Question) -> bool:
        """ Gets the user answer and returns True if it is correct and False if not. """
        answer = ''
        if question.get_answer_len() == 0:
            answer = input('ANSWER (free-response): ').strip().lower()
            match question.get_question_type():
                case 'street':
                    if question.get_street_type() == get_type(answer):
                        self.score += 1
                        print(f'Correct! Your score is now {self.score}/{len(self.questions)}!')
                        return True
                    else:
                        print(f'Incorrect! Your answer \'{answer}\' is of type \'{get_type(answer)}\'.\n' +
                              f'Your score is now {self.score}/{len(self.questions)}. Better luck next time!')
                        return False
                case 'type':
                    if question.get_correct_answer().lower() == answer.lower():
                        self.score += 1
                        print(f'Correct! Your score is now {self.score}/{len(self.questions)}!')
                        return True
                    else:
                        print(f'Incorrect! The answer is \'{question.get_correct_answer()}\'.\n' +
                            f'Your score is now {self.score}/{len(self.questions)}. Better luck next time!')
                        return False
        else:
            answer = input('ANSWER (1/2/3/etc.): ').strip()
            if not answer.isdigit():
                print('INVALID ANSWER! TRY AGAIN!')
                return self.get_user_answer(question)
        if question.get_correct_answer().lower() == answer:
            self.score += 1
            print(f'Correct! Your score is now {self.score}/{len(self.questions)}!')
            return True
        else:
            print(f'Incorrect! The correct answer is {question.get_correct_answer()}!\n' +
                f'Your score is now {self.score}/{len(self.questions)}. Better luck next time!')
            return False

    def execute(self):
        print('Let\'s begin the quiz!')
        for i in range(len(self.questions)):
            print(self.questions[i].render_question())
            self.get_user_answer(self.questions[i])
        print(f'Your final score is {self.score}/{len(self.questions)}! Thanks for playing!')
        main_menu()

    def __str__(self):
        string = '--------------------------------------------------\n'
        string += f'QUIZ:\n# OF QUESTIONS: {len(self.questions)}\nCURRENT SCORE: {self.score}\nQUESTIONS:\n'
        for q in self.questions:
            string += q.__str__() + '\n'
        string += '--------------------------------------------------'
        return string

def input_street_name():
    """ Look up street option """
    while True:
        master_input = input('Which street is it whose type you are looking for? (\'exit\' to exit to main menu) ')
        if master_input.lower() == 'quit':
            print('Quitting program...')
            quit()
        elif master_input.lower() == 'exit':
            break
        else:
            print(f'The street type is {get_type(master_input)}.')
    main_menu()

def main_menu() -> None:
    master_input = ''
    while not master_input.isdigit() or (master_input.isdigit() and (int(master_input) < 1 or int(master_input) > 4)):
        master_input = input('What would you like to do next?\n1. Look up street\n2. Look up streets of type\n' + \
                             '3. Quiz\n4. Quit\nANSWER (1/2/3/4): ').strip()
        if not master_input.isdigit() or (master_input.isdigit() and (int(master_input) < 1 or int(master_input) > 4)):
            print('INVALID INPUT. PLEASE TRY AGAIN.')
    match int(master_input):
        case 1:
            input_street_name()
        case 2:
            type = ''
            amount = 0
            while True:
                type = input('Which street type are you looking for? (\'exit\' to exit to main menu) ').strip().lower()
                if type == 'exit':
                    return main_menu()
                else:
                    in_the_list = False
                    for t in street_types:
                        t = t.strip()
                        if type.lower() == t.lower():
                            in_the_list = True
                            break
                    if not in_the_list:
                        print('INVALID INPUT. PLEASE TRY AGAIN.')
                    else:
                        break
            while True:
                amount = input('How many streets would you like? (\'exit\' to exit to main menu) ').strip()
                if amount.lower() == 'exit':
                    return main_menu()
                elif amount.isdigit() and int(amount) > 0:
                    amount = int(amount)
                    break
                else:
                    print('INVALID INPUT. PLEASE TRY AGAIN.')

            # Fetch and print out the street list
            street_list = get_streets_of_type(type, amount)
            if len(street_list) == 0:
                print(f'There are no streets of type \'{type}\'\n')
            else:
                print(f'List of Streets of Type \'{type}\':')
                for i in range(len(street_list)):
                    print(f'{i + 1}. {street_list[i]}')
                print()
            return main_menu()
        case 3:
            quiz = None
            while True:
                master_input = input('How many questions would you like? (\'exit\' to exit to main menu) ').strip()
                if master_input.lower() == 'exit':
                    return main_menu()
                elif master_input.isdigit() and int(master_input) > 0:
                    quiz = Quiz(int(master_input))
                    break
                else:
                    print('INVALID INPUT. PLEASE TRY AGAIN.')
            quiz.execute()
        case 4:
            print('Quitting program...')
            quit()

if __name__ == "__main__":
    get_basic_street_database()
    # print(get_type('brookmere')) # Something wrong with Brookmere Rd
    main_menu()
