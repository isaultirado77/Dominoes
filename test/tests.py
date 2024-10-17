from typing import List, Any
import ast
from hstest import StageTest, CheckResult, WrongAnswer, TestCase


class TestStage1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(),
            TestCase(),
            TestCase(),
            TestCase(),
            TestCase()
        ]

    def get_list(self, replyks):
        ind = replyks.find('[')
        try:
            return ast.literal_eval(replyks[ind:])
        except (ValueError, SyntaxError):
            raise WrongAnswer("An error occurred while processing your output.\n"
                              "Please make sure that your program's output is formatted exactly as described.")

    def get_all_lists(self, replyk):
        sp = self.get_list(replyk[0])
        cp = self.get_list(replyk[1])
        pp = self.get_list(replyk[2])
        ds = self.get_list(replyk[3])
        return sp, cp, pp, ds

    def get_the_fish(self, computer_pieces, player_pieces, domino_snake):
        status_check = 'computer' if len(computer_pieces) == 7 else 'player'
        double_computer_pieces = sorted([i for i in computer_pieces if i[0] == i[1]], reverse=True)
        double_player_pieces = sorted([i for i in player_pieces if i[0] == i[1]], reverse=True)
        high_double_computer_piece = double_computer_pieces[0] if len(double_computer_pieces) > 0 else []
        high_double_player_piece = double_player_pieces[0] if len(double_player_pieces) > 0 else []
        domino_snake = domino_snake[0] if domino_snake[0][0] == domino_snake[0][1] else []
        maxes = sorted([domino_snake, high_double_computer_piece, high_double_player_piece], reverse=True)
        return maxes[0], status_check

    def check_nested_lists(self, list_to_check, list_name):
        if not list_to_check or type(list_to_check) != list or any([type(item) != list for item in list_to_check]):
            raise WrongAnswer("{0} list in your output is not a nested list. \n"
                              "Please, make it a nested list.".format(list_name))

    def count_unique(self, replyk):
        sp, cp, pp, ds = self.get_all_lists(replyk)
        self.check_nested_lists(sp, "Stock pieces")
        self.check_nested_lists(cp, "Computer pieces")
        self.check_nested_lists(pp, "Player pieces")
        self.check_nested_lists(ds, "Domino snake")
        sp += cp
        sp += pp
        sp += ds
        sp = [tuple(i) for i in sp]
        try:
            return len(set(sp))
        except:
            return False

    def check(self, reply: str, attach: Any) -> CheckResult:
        replyk = reply.strip().split('\n')
        if len(replyk) != 5:
            return CheckResult.wrong(f"Expected exactly 5 lines in your output, found {len(replyk)}")
        for i, st in enumerate(['Stock', 'Computer', 'Player', 'Domino', 'Status']):
            if not replyk[i].strip().lower().startswith(st.lower()):
                return CheckResult.wrong(f"{i} line of your output should start with \"{st}\" substring as in example")
        stock_pieces, computer_pieces, player_pieces, domino_snake = self.get_all_lists(replyk)
        if not self.count_unique(replyk):
            return CheckResult.wrong("The full set is not right. "
                                     "Make sure the full comprises 28 unique domino pieces.")
        if len(stock_pieces) != 14:
            return CheckResult.wrong(f"Expected 14 stock pieces, found {len(stock_pieces)}")
        if len(stock_pieces) + len(computer_pieces) + len(player_pieces) + len(domino_snake) != 28:
            return CheckResult.wrong(f"Expected 28 pieces in your output in total, found "
                                     f"{len(stock_pieces) + len(computer_pieces) + len(player_pieces) + len(domino_snake)}")
        if len(computer_pieces) + len(player_pieces) + len(domino_snake) != 14:
            return CheckResult.wrong("The pieces played are not right")
        if len(domino_snake) != 1:
            return CheckResult.wrong("The domino snake should have exactly one piece.")
        try:
            domino_snake_check, status_check = self.get_the_fish(computer_pieces, player_pieces, domino_snake)
        except Exception:
            return CheckResult.wrong("Something wrong with output format! "
                                     "Make sure your output format is the same as in examples!")
        if domino_snake[0] != domino_snake_check:
            return CheckResult.wrong("Domino snake is not right. "
                                     "Please make sure the starting domino is the highest double domino.\n"
                                     f"Expected: {domino_snake_check}")
        if status_check not in replyk[4].lower():
            return CheckResult.wrong("Status is not right. "
                                     "Please make sure that the status is the one, who is to make the next move "
                                     "(the one who is left with 7 pieces after pieces were distributed)")

        return CheckResult.correct()


if __name__ == '__main__':
    TestStage1('dominoes.dominoes').run_tests()