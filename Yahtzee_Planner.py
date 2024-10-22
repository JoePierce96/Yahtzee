

#Planner for Yahtzee
#Simplifications:  only allow discard and roll, only score against upper level


# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    di_scores = {1: 0,
                 2: 0,
                 3: 0,
                 4: 0,
                 5: 0,
                 6: 0}
    
    for dice in hand:
        di_scores[dice] = hand.count(dice) * dice
    return max(di_scores.values())
    

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    all_dice = range(1, num_die_sides+1)
    all_seqs = gen_all_sequences(all_dice, num_free_dice) # generate all possible be sequences of free dice
    total_score = 0.0
    value = 0.0
    
    for seq in all_seqs:
        scored_di = list(held_dice) + list(seq)
        value += score(seq)
    evalue = value / len(all_seqs)  # expected value or mean value over all seqs
    return evalue

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    holds = [()]
    for di in hand:
        for sset in holds:
            holds = holds + [tuple(sset) + (di,)]
    return set(holds)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_value = 0.0
    prev_score = 0.0
    
    for hold in gen_all_holds(hand):
        max_value = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if max_value > prev_score:
            prev_score = max_value
            
    
    return (prev_score, hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print("Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score)
    print(score(hand))

  
run_example()

