import skfuzzy as fuzz
from skfuzzy import control as ctrl


users_types=['normal','hater']

def get_user_type_rules(likes_fuzzy, dislikes_fuzzy, shares_fuzzy, group_conform, relevance, friend_trust, friend_experience, friendship, like_score, user_type='normal'):
    rules = []
    if user_type == 'normal':
        # Existing rules for normal users
        rules.append(ctrl.Rule(likes_fuzzy['high_success'] & dislikes_fuzzy['low_success'], relevance['high_relevance']))
        rules.append(ctrl.Rule(shares_fuzzy['high_success'] & dislikes_fuzzy['low_success'], relevance['high_relevance']))
        rules.append(ctrl.Rule(likes_fuzzy['low_success'] | dislikes_fuzzy['high_success'], relevance['high_relevance']))
        rules.append(ctrl.Rule(likes_fuzzy['low_success'] | ~shares_fuzzy['high_success'], relevance['high_relevance']))
        rules.append(ctrl.Rule(relevance['high_relevance'] & group_conform['high_group_conform'], relevance['high_relevance']))
        rules.append(ctrl.Rule(friend_experience['negative'], friendship['no_friendship']))
        rules.append(ctrl.Rule(friend_experience['positive'] & friend_trust['good_friend'] | friend_trust['just_knowed'], friendship['mid_friendship']))
        rules.append(ctrl.Rule(friend_experience['positive'] & friend_trust['good_friend'] | friend_trust['just_knowed'], relevance['high_relevance']))
        rules.append(ctrl.Rule(friend_trust['hated'], relevance['no_relevance']))
        rules.append(ctrl.Rule(like_score['negative'], relevance['no_relevance']))
        rules.append(ctrl.Rule(relevance['high_relevance'] & group_conform['no_group_conform'], relevance['no_relevance']))
    elif user_type == 'hater':
        # Existing rules for hater users
        rules.append(ctrl.Rule(likes_fuzzy['high_success'] & dislikes_fuzzy['low_success'], relevance['high_relevance']))
        rules.append(ctrl.Rule(shares_fuzzy['high_success'] & dislikes_fuzzy['low_success'], relevance['no_relevance']))
        rules.append(ctrl.Rule(likes_fuzzy['low_success'] | dislikes_fuzzy['high_success'], relevance['no_relevance']))
        rules.append(ctrl.Rule(likes_fuzzy['low_success'] | ~shares_fuzzy['high_success'], relevance['no_relevance']))
        rules.append(ctrl.Rule(relevance['high_relevance'] & group_conform['high_group_conform'], relevance['no_relevance']))
        rules.append(ctrl.Rule(friend_experience['negative'], friendship['no_friendship']))
        rules.append(ctrl.Rule(friend_experience['positive'] & friend_trust['good_friend'] | friend_trust['just_knowed'], friendship['no_friendship']))
        rules.append(ctrl.Rule(friend_experience['positive'] & friend_trust['good_friend'] | friend_trust['just_knowed'], relevance['no_relevance']))
        rules.append(ctrl.Rule(friend_trust['hated'], relevance['no_relevance']))
        rules.append(ctrl.Rule(like_score['negative'], relevance['no_relevance']))
        rules.append(ctrl.Rule(relevance['high_relevance'] & group_conform['no_group_conform'], relevance['no_relevance']))
    elif user_type == 'power_user':
        # Rules for power users
        rules.append(ctrl.Rule(likes_fuzzy['high_success'] & shares_fuzzy['high_success'], relevance['high_relevance']))
        rules.append(ctrl.Rule(dislikes_fuzzy['high_success'] | shares_fuzzy['low_success'], relevance['high_relevance']))
        rules.append(ctrl.Rule(friend_trust['good_friend'] & friend_experience['positive'], friendship['high_friendship']))
        rules.append(ctrl.Rule(friend_trust['good_friend'] & friend_experience['positive'], relevance['high_relevance']))
        rules.append(ctrl.Rule(group_conform['high_group_conform'], relevance['high_relevance']))
        rules.append(ctrl.Rule(like_score['positive'], relevance['high_relevance']))
    elif user_type == 'casual_user':
        # Rules for casual users
        rules.append(ctrl.Rule(likes_fuzzy['low_success'] | shares_fuzzy['low_success'], relevance['low_relevance']))
        rules.append(ctrl.Rule(dislikes_fuzzy['high_success'] | shares_fuzzy['low_success'], relevance['low_relevance']))
        rules.append(ctrl.Rule(friend_trust['just_knowed'], friendship['low_friendship']))
        rules.append(ctrl.Rule(friend_trust['just_knowed'], relevance['low_relevance']))
        rules.append(ctrl.Rule(group_conform['low_group_conform'], relevance['low_relevance']))
        rules.append(ctrl.Rule(like_score['neutral'], relevance['low_relevance']))
    elif user_type == 'engagement_user':
        # Rules for engagement users
        rules.append(ctrl.Rule(likes_fuzzy['mid_success'] | shares_fuzzy['high_success'], relevance['mid_relevance']))
        rules.append(ctrl.Rule(dislikes_fuzzy['low_success'] | shares_fuzzy['mid_success'], relevance['mid_relevance']))
        rules.append(ctrl.Rule(friend_trust['good_friend'] & friend_experience['positive'], friendship['high_friendship']))
        rules.append(ctrl.Rule(friend_trust['good_friend'] & friend_experience['positive'], relevance['high_relevance']))
        rules.append(ctrl.Rule(group_conform['mid_group_conform'], relevance['mid_relevance']))
        rules.append(ctrl.Rule(like_score['positive'], relevance['mid_relevance']))
    
    return rules