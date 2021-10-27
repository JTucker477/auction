#!/usr/bin/env python

import sys
import logging
from gsp import GSP
from util import argmax_index

class ungodly_hourbb:
    """Balanced bidding agent"""
    def __init__(self, id, value, budget):
        self.id = id
        self.value = value
        self.budget = budget

    def initial_bid(self, reserve):
        return self.value / 2


    # FOr a given slot, min_bid is how much you need to tie with the other agent in the last round. 
    def slot_info(self, t, history, reserve):
        """Compute the following for each slot, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns list of tuples [(slot_id, min_bid, max_bid)], where
        min_bid is the bid needed to tie the other-agent bid for that slot
        in the last round.  If slot_id = 0, max_bid is 2* min_bid.
        Otherwise, it's the next highest min_bid (so bidding between min_bid
        and max_bid would result in ending up in that slot)
        """
        prev_round = history.round(t-1)
        other_bids = [a_id_b for a_id_b in prev_round.bids if a_id_b[0] != self.id]

        clicks = prev_round.clicks
        def compute(s):
            (min, max) = GSP.bid_range_for_slot(s, clicks, reserve, other_bids)
            if max == None:
                max = 2 * min
            return (s, min, max)
            
        info = list(map(compute, list(range(len(clicks)))))
#        sys.stdout.write("slot info: %s\n" % info)
        return info

    # Going to use this to maximize the positiont hat gives us the est utility. 
    def expected_utils(self, t, history, reserve):
        """
        Figure out the expected utility of bidding such that we win each
        slot, assuming that everyone else keeps their bids constant from
        the previous round.

        returns a list of utilities per slot.
        """
        # TODO: Fill this in

        # Expected value = pos_j * (v_j - t_j )

        # Maybe position effect is click/total click

        # the expected utility for each position

        # for t, find the jth highest bid for 
        # # utility = clicks * (v_i - b^t)

        # John

        utilities = []
        past_slot = self.slot_info(t, history, reserve)
        for slot in range(len(history.round(t-1).clicks)):
        
            t_j = past_slot[slot][1]
            pos_j = history.round(t-1).clicks[slot]
            utilities.append(pos_j * (self.value - t_j))

                
        return utilities

    def target_slot(self, t, history, reserve):
        """Figure out the best slot to target, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns (slot_id, min_bid, max_bid), where min_bid is the bid needed to tie
        the other-agent bid for that slot in the last round.  If slot_id = 0,
        max_bid is min_bid * 2
        """
        i =  argmax_index(self.expected_utils(t, history, reserve))
        info = self.slot_info(t, history, reserve)
        return info[i]

    def bid(self, t, history, reserve):
        # The Balanced bidding strategy (BB) is the strategy for a player j that, given
        # bids b_{-j},
        # - targets the slot s*_j which maximizes his utility, that is,
        # s*_j = argmax_s {clicks_s (v_j - t_s(j))}.
        # - chooses his bid b' for the next round so as to
        # satisfy the following equation:
        # clicks_{s*_j} (v_j - t_{s*_j}(j)) = clicks_{s*_j-1}(v_j - b')
        # (p_x is the price/click in slot x)
        # If s*_j is the top slot, bid the value v_j


        
        # John 
        prev_round = history.round(t-1)
        amt_slots = len(prev_round.clicks)
        (slot, min_bid, max_bid) = self.target_slot(t, history, reserve)

       
        # How many clicks for this slot last round
        pos_j = prev_round.clicks[slot]
        pos_j_min_1 = prev_round.clicks[slot - 1]
       
        past_slot = self.slot_info(t, history, reserve)
        t_j = past_slot[slot][1]

        
        # Not expecting to win:
        if t_j >= self.value:
            
            bid =  self.value
        # If going to the top
        elif slot == 0:
   
            bid =  self.value
        # If not going for the top:
        else:
            bid = self.value - (pos_j * (self.value - t_j))/pos_j_min_1
    
        return bid

  

    def __repr__(self):
        return "%s(id=%d, value=%d)" % (
            self.__class__.__name__, self.id, self.value)


