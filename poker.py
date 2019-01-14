#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools
# Можно свободно определять свои функции и т.п.
# -----------------


from collections import Counter
from itertools import combinations, product

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""

    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def compare_hands(hand_left, hand_right):
    """Сравнивает руки и возвращает лучшую из них"""

    hand_left_r = hand_rank(hand_left)
    hand_right_r = hand_rank(hand_right)
    result = compare_hand_rank(hand_left_r, hand_right_r)
    if result is hand_left_r:
        return hand_left
    elif result is hand_right_r:
        return hand_right
    else:
        return None


def compare_hand_rank(left, right):
    """Функция на вход принимает результат ф-ии hand_rank.
       Сравнивает ранги и возвращает старший."""

    if left[0] > right[0]:
        return left
    elif left[0] < right[0]:
        return right

    # Тут мы окажемся, если ранги равны
    rank = left[0]

    if rank in [7, 6, 3, 1]:
        if left[1] > right[1]:
            return left
        elif left[1] < right[1]:
            return right
        elif left[2] > right[2]:
            return left
        elif left[2] < right[2]:
            return right
        else:  # руки равны!
            return None

    elif rank == 2:
        if max(left[1]) > max(right[1]):
            return left
        elif max(left[1]) < max(right[1]):
            return right
        if min(left[1]) > min(right[1]):
            return left
        elif min(left[1]) < min(right[1]):
            return right
        else:  # руки равны!
            return None

    elif rank in [0, 5]:
        if max(left[1]) > max(right[1]):
            return left
        elif max(left[1]) < max(right[1]):
            return right
        else:  # руки равны!
            return None
    elif rank in [4, 8]:
        if left[1] > right[1]:
            return left
        elif left[1] < right[1]:
            return right
        else:  # руки равны!
            return None


def convert_rank(rank):
    """Функция конвертирует ранг в его числовое представление"""

    return int(rank.replace('T', '10').replace('J', '11').replace('Q', '12').replace('K', '13').replace('A', '14'))


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""

    ranks = []
    for card in hand:
        ranks.append(convert_rank(card[0]))
    ranks.sort(reverse=True)
    return ranks


def flush(hand):
    """Возвращает True, если все карты одной масти"""

    suits = []
    for card in hand:
        suits.append(card[1].lower())
    return len(set(suits)) == 1


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""

    straight_count = 1
    for i in range(1, len(ranks)):
        if ranks[i - 1] - 1 == ranks[i]:
            straight_count += 1
        else:
            straight_count = 1

    return straight_count >= 5


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""

    cards_count = Counter(ranks)
    result = {}
    for rank, count in cards_count.iteritems():
        if count == n:
            result.update({rank: count})
    if result:
        return sorted(result)[-1]
    else:
        return None


def two_pair(ranks):
    """Если есть две пары, то возвращает два соответствующих ранга,
    иначе возвращает None"""

    cards_count = Counter(ranks)
    pairs = {}
    for rank, count in cards_count.iteritems():
        if count == 2:
            pairs.update({rank: count})
    if len(pairs) == 2:
        return pairs.keys()
    else:
        return None


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """

    combinations_iter = combinations(hand, 5)
    hand_top = combinations_iter.next()

    for hand5 in combinations_iter:
        cur_hand = compare_hands(hand_top, hand5)
        # None будет, если значения рук одинаковое.
        if cur_hand is not None and cur_hand is not hand_top:
            hand_top = hand5
    return hand_top


def get_joker_iter(joker):
    """Функция определяет цвет джокера и возвращает соответствующий ему набор дополнительных карт"""

    if joker[1].lower() == 'b':
        # color = 'B'
        additional_cards = product(RANKS, ['C', 'S'])
    else:
        # color = 'R'
        additional_cards = product(RANKS, ['H', 'D'])
    return additional_cards


def best_wild_hand(wild_hand):
    """best_hand но с джокерами"""

    hand_without_jokers = []
    jokers = []

    for card in wild_hand:
        # Проверим на наличие джокера
        if '?' in card:
            jokers.append(get_joker_iter(card))
        else:
            hand_without_jokers.append(card)

    if not jokers:
        return best_hand(hand_without_jokers)

    all_cards = product([hand_without_jokers], *jokers)

    # для первоначального значения
    top_hand = best_hand(parse_hand(all_cards.next()))

    for hand_unparsed in all_cards:
        # Тут просто приводим "вид руки" к обычному списку карт
        hand = parse_hand(hand_unparsed)
        # получаем лучшую возможную руку из имеющийся руки hand
        cur_hand = best_hand(hand)
        # сравним текущую руку с лучшей
        tmp_hand = compare_hands(cur_hand, top_hand)
        # Теперь обновим лучшую руку
        if tmp_hand is not None and tmp_hand is not top_hand:
            # None будет, если значения рук одинаковое.
            top_hand = tmp_hand

    return top_hand


def parse_hand(hand_unparsed):
    """ Совсем вспомогательная функция, помогает разобрать то что мы "собрали" при подготовке руки с джокерами. """
    hand = []

    for item in hand_unparsed:
        if type(item) is list:
            hand = list(item)
        elif type(item) is tuple:
            joker_card = "".join(item)  # Карта "заменяющая" джокер
            if joker_card in hand:
                # Двух одинаковых карт в колоде не может быть
                continue
            else:
                hand += ["".join(item)]

    return hand


def test_best_hand():
    print "test_best_hand..."
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'


def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
