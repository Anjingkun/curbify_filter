# Distance
distance_questions = [
    "What is the distance between [A] and [B]?",
    "How far apart are [A] and [B]?",
    "How distant is [A] from [B]?",
    "How far is [A] from [B]?",
    "How close is [A] from [B]?",
    "Could you measure the distance between [A] and [B]?",
    "Can you tell me the distance of [A] from [B]?",
    "How far away is [A] from [B]?",
    "Can you provide the distance measurement between [A] and [B]?",
    "Can you give me an estimation of the distance between [A] and [B]?",
    "Could you provide the distance between [A] and [B]?",
    "How much distance is there between [A] and [B]?",
    "Tell me the distance between [A] and [B].",
    "Give me the distance from [A] to [B].",
    "Measure the distance from [A] to [B].",
    "Measure the distance between [A] and [B].",
]

distance_responses = [
    "[X].",
    "[A] and [B] are [X] apart.",
    "[A] is [X] away from [B].",
    "A distance of [X] exists between [A] and [B].",
    "[A] is [X] from [B].",
    "[A] and [B] are [X] apart from each other.",
    "They are [X] apart.",
    "The distance of [A] from [B] is [X].",
]

obj_depth_questions = [
    "What is the depth value of [A]?",
    "How far is [A] from camera?",
    "Give me the distance from [A] to camera.",
    "Measure the distance between [A] and camera.",
    "Tell me the distance between [A] and camera.",
    "How far away is [A] from camera?",
    "Can you give me an estimation of the distance between [A] and camera?",
    "Can you provide the distance between [A] and camera?",
    "How close is [A] from camera?",
    "Can you tell me the distance of [A] from camera?",
]

obj_depth_responses = [
    "[X].",
    "The depth of [A] is [X].",
    "[A] and camera are [X] apart.",
    "[A] is [X] away from camera.",
    "A distance of [X] exists between [A] and camera.",
    "[A] is [X] from camera.",
    "[A] and camera are [X] apart from each other.",
    "They are [X] apart.",
    "The distance of [A] from camera is [X].",
]

point_depth_questions = [
    "What is the depth value of point [A]?",
    "How far is point [A] from the camera?",
    "Give me the distance from point [A] to camera.",
    "Measure the distance between point [A] and camera.",
    "Tell me the distance between point [A] and camera.",
    "How far away is point [A] from camera?",
    "Can you give me an estimation of the distance between point [A] and camera?",
    "Can you provide the distance between point [A] and camera?",
    "How close is point [A] from camera?",
    "Can you tell me the distance of point [A] from camera?",
]

point_depth_responses = [
    "[X].",
    "The depth of point [A] is [X].",
    "Point [A] and camera are [X] apart.",
    "Point [A] is [X] away from camera.",
    "A distance of [X] exists between point [A] and camera.",
    "Point [A] is [X] from camera.",
    "Point [A] and camera are [X] apart from each other.",
    "They are [X] apart.",
    "The distance of point [A] from camera is [X].",
]

fine_grain_object_2_point_questions = [
    "Where is [A] located? Please provide its 2D coordinates.",
    "Can you find the [A]? Please provide its 2D coordinates.",
    "Can you point to [A]? Please provide its 2D coordinates."
    "Where can I find [A]? Please provide its 2D coordinates.",
    "What is the location of [A]? Please provide its 2D coordinates.",
    "Give me the position of [A]. Please provide its 2D coordinates.",
    "Chose the point of [A]. Please provide its 2D coordinates.",
    "What is the 2D location of [A]? Please provide its 2D coordinates.",

    "Point to [A].",
    "Point to the [A] in the image.",
    "Point to all occurrences of [A] in the image.",
    "Point to any [A] in the image.",
    "Locate all [A] in the image.",
    "Locate [A] in the image.",
    "Locate the [A] in the image.",

    "In the image, there is a [A]. Pinpoint a point to the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be between 0 and 1, indicating the normalized pixel location of the point.",
    "Identify a spot on the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be between 0 and 1, indicating the normalized pixel location of the point.",
    "Locate a point on the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be between 0 and 1, indicating the normalized pixel location of the point.",
    "Select a point on the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be between 0 and 1, indicating the normalized pixel location of the point.",
    "Select a location on the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be between 0 and 1, indicating the normalized pixel location of the point.",
    "Give me the position of [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be between 0 and 1, indicating the normalized pixel location of the point.",
    "Choose the point of [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be between 0 and 1, indicating the normalized pixel location of the point.",
    "What is the 2D location of [A]? Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be between 0 and 1, indicating the normalized pixel location of the point.",

    "In the image, there is a [A]. Pinpoint a point to the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be rounded to three decimal places, indicating the absolute pixel location of the point in the image.",
    "Identify a spot on the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be rounded to three decimal places, indicating the absolute pixel location of the point in the image.",
    "Locate a point on the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be rounded to three decimal places, indicating the absolute pixel location of the point in the image.",
    "Select a point on the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be rounded to three decimal places, indicating the absolute pixel location of the point in the image.",
    "Select a location on the [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be rounded to three decimal places, indicating the absolute pixel location of the point in the image.",
    "Give me the position of [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be rounded to three decimal places, indicating the absolute pixel location of the point in the image.",
    "Choose the point of [A]. Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be rounded to three decimal places, indicating the absolute pixel location of the point in the image.",
    "What is the 2D location of [A]? Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above. The coordinates should be rounded to three decimal places, indicating the absolute pixel location of the point in the image.",

    "Where is [A] located? Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above.",
    "Can you find the [A]? Your answer should be formatted as a tuple, i.e. [(x, y)], where the tuple contains the x and y coordinates of a point satisfying the conditions above.",
]


fine_grain_object_2_point_responses = [
    "[X]"
]

point_2_caption_questions = [
    "What is at point [X]?",
    "Which object is located at point [X]?",
    "Which object can be found at point [X]?",
    "Describe the object at point [X].",
    "What object lies at point [X]?",
    "What do you see at point [X]?",
    "What can be observed at point [X]?",
]

point_2_caption_responses = [
    "[A]."
]

# obj Predicates ------------------------------------------------------
left_predicate_questions = [
    "Is [A] at the left side of [B]?",
    "Is [A] to the left of [B] from the viewer's perspective?",
    "Does [A] appear on the left side of [B]?",
    "Can you confirm if [A] is positioned to the left of [B]?",
    "Considering the relative positions of [A] and [B] in the image provided, is [A] to the left of [B] from the viewer's perspective?"
]

left_true_responses = [
    "Yes.",
    "Yes, [A] is to the left of [B].",
    "Indeed, [A] is positioned on the left side of [B].",
    "Correct, you'll find [A] to the left of [B].",
]

left_false_responses = [
    "No.",
    "No, [A] is not to the left of [B].",
    "In fact, [A] is to the right of [B].",
    "Incorrect, [A] is not on the left side of [B].",
]

right_predicate_questions = [
    "Is [A] at the right side of [B]?",
    "Is [A] to the right of [B] from the viewer's perspective?",
    "Does [A] appear on the right side of [B]?",
    "Can you confirm if [A] is positioned to the right of [B]?",
    "Considering the relative positions of [A] and [B] in the image provided, is [A] to the right of [B] from the viewer's perspective?"
]

right_true_responses = [
    "Yes.",
    "Yes, [A] is to the right of [B].",
    "Indeed, [A] is positioned on the right side of [B].",
    "Correct, you'll find [A] to the right of [B].",
]

right_false_responses = [
    "No.",
    "No, [A] is not to the right of [B].",
    "In fact, [A] is to the left of [B].",
    "Incorrect, [A] is not on the right side of [B].",
]

horizontal_aligned_responses = [
    "[A] and [B] are horizontally aligned without one being to the left or right of the other.",
    "[A] and [B] exist on the same horizontal plane, with neither left nor right distinction.",
    "Both [A] and [B] occupy the same horizontal space, without a left or right relationship.",
    "At the same horizontal level, [A] and [B] are aligned without implying one is to the left or right.",
    "[A] and [B] stand at equal distances, with no indication of one being to the left or right.",
    "No horizontal hierarchy exists between [A] and [B]; they are at a shared horizontal position.",
    "Occupying the same level, [A] and [B] show no horizontal order of left or right.",
    "[A] and [B] are aligned in such a way that negates a left or right relationship.",
    "Without one to the left or right of the other, [A] and [B] are horizontally aligned.",
    "[A] and [B] are at a level where distinguishing between left and right does not apply.",
]

vertical_aligned_responses = [
    "[A] and [B] share the same elevation without one being over the other.",
    "[A] and [B] exist on the same vertical plane, with neither above nor below.",
    "Both [A] and [B] occupy the same vertical space, without a top or bottom distinction.",
    "At the same elevation, [A] and [B] are aligned without implying one is atop the other.",
    "[A] and [B] stand at equal heights, with no indication of one being higher or lower.",
    "No vertical hierarchy exists between [A] and [B]; they are at a shared elevation.",
    "Occupying the same level, [A] and [B] show no vertical order of above or below.",
    "[A] and [B] are aligned in such a way that negates a top or bottom relationship.",
    "Without one over the other, [A] and [B]'s elevation is equivalent.",
    "[A] and [B] are at a level where distinguishing between higher and lower does not apply.",
]

image_above_predicate_questions = [
    "From the image's perspective, is [A] above [B]?",
    "From the image's perspective, does [A] appear higher than [B]?",
    "From the image's perspective, is [A] located above [B]?",
    "From the image's perspective, would you say [A] is positioned over [B]?",
    "From the image's perspective, is [A] on top of [B]?",
    "From the image's perspective, is [A] over [B]?",
    "From the image's perspective, is [A] on [B]?",
]

image_above_true_responses = [
    "Yes.",
    "Yes, from the image's perspective, [A] is above [B].",
    "Correct, [A] appears higher than [B] in the image.",
    "Indeed, from the image's perspective, [A] is shown above [B].",
    "Yes, from the image's perspective, [A] is on top of [B].",
    "Yes, from the image's perspective, [A] is over [B].",
]

image_above_false_responses = [
    "No.",
    "No, from the image's perspective, [A] is not above [B].",
    "Actually, [A] appears below [B] in the image.",
    "Incorrect, from the image's perspective, [A] is lower than [B].",
    "No, from the image's perspective, [A] is not on top of [B].",
    "No, from the image's perspective, [A] is not over [B].",
]

image_below_predicate_questions = [
    "From the image's perspective, is [A] below [B]?",
    "From the image's perspective, does [A] appear lower than [B]?",
    "From the image's perspective, is [A] located beneath [B]?",
    "From the image's perspective, would you say [A] is shown under [B]?",
    "From the image's perspective, is [A] under [B]?",
    "From the image's perspective, is [A] beneath [B]?",
]

image_below_true_responses = [
    "Yes.",
    "Yes, from the image's perspective, [A] is below [B].",
    "Correct, [A] appears lower than [B] in the image.",
    "Indeed, from the image's perspective, [A] is shown beneath [B].",
    "Yes, from the image's perspective, [A] is beneath [B].",
]

image_below_false_responses = [
    "No.",
    "No, from the image's perspective, [A] is not below [B].",
    "Actually, [A] appears above [B] in the image.",
    "Incorrect, from the image's perspective, [A] is higher than [B].",
    "No, from the image's perspective, [A] is not beneath [B].",
]

world_above_predicate_questions = [
    "From a real-world perspective, is [A] physically above [B]?",
    "From a real-world perspective, is [A] located higher than [B]?",
    "From a real-world perspective, does [A] stand above [B]?",
    "From a real-world perspective, is [A] positioned over [B] based on gravity?",
    "From a real-world perspective, is [A] on top of [B]?",
    "From a real-world perspective, is [A] over [B]?",
    "From a real-world perspective, is [A] on [B]?",
]
world_above_true_responses = [
    "Yes.",
    "Yes, from a real-world perspective, [A] is above [B].",
    "Correct, in the physical world, [A] is higher than [B].",
    "Indeed, from a real-world perspective, [A] stands above [B].",
    "Yes, from a real-world perspective, [A] is on top of [B].",
    "Yes, from a real-world perspective, [A] is over [B].",
]
world_above_false_responses = [
    "No.",
    "No, from a real-world perspective, [A] is not above [B].",
    "Actually, [A] is physically below [B] in the real world.",
    "Incorrect, from a real-world perspective, [A] is lower than [B].",
    "No, from a real-world perspective, [A] is not on top of [B].",
    "No, from a real-world perspective, [A] is not over [B]",
]

world_below_predicate_questions = [
    "From a real-world perspective, is [A] below [B]?",
    "From a real-world perspective, is [A] physically below [B]?",
    "From a real-world perspective, is [A] located beneath [B]?",
    "From a real-world perspective, does [A] sit lower than [B]?",
    "From a real-world perspective, is [A] positioned under [B] based on gravity?",
    "From a real-world perspective, is [A] beneath [B]?",
    "From a real-world perspective, is [A] under [B]?",
]

world_below_true_responses = [
    "Yes.",
    "Yes, from a real-world perspective, [A] is below [B].",
    "Correct, in the physical world, [A] is lower than [B].",
    "Indeed, from a real-world perspective, [A] is positioned beneath [B].",
    "Yes, from a real-world perspective, [A] is beneath [B].",
    "Yes, from a real-world perspective, [A] is under [B].",
]

world_below_false_responses = [
    "No.",
    "No, from a real-world perspective, [A] is not below [B].",
    "Actually, [A] is physically above [B] in the real world.",
    "Incorrect, from a real-world perspective, [A] is higher than [B].",
    "No, from a real-world perspective, [A] is not beneath [B].",
    "No, from a real-world perspective, [A] is not under [B].",
]

behind_predicate_questions = [
    "Is the depth of [A] greater than that of [B]?",
    "Is [A] behind [B]?",
    "Is the position of [A] more distant than that of [B]?",
    "Does [A] lie behind [B]?",
    "Is [A] positioned behind [B]?",
    "Is [A] further to camera compared to [B]?",
    "Does [A] come behind [B]?",
    "Is [A] further to the viewer compared to [B]?",
    "Considering the relative positions of [A] and [B] in the image provided, is [A] behind [B]?"
]

behind_true_responses = [
    "Yes.",
    "Yes, it is.",
    "Yes, it is behind [B].",
    "That is True.",
    "Yes, [A] is further from the viewer.",
    "Yes, [A] is further from the camera.",
    "Yes, [A] is behind [B].",
    "Yes, the depth of [A] is greater than that of [B].",
]

behind_false_responses = [
    "No.",
    "No, it is not.",
    "No, it is in front of [B].",
    "That is False.",
    "No, [A] is closer to the viewer.",
    "No, [A] is closer to the camera.",
    "No, [A] is in front of [B].",
    "No, the depth of [A] is less than that of [B].",
]

front_predicate_questions = [
    "Is [A] in front of [B]?",
    "Is the position of [A] less distant than that of [B]?",
    "Does [A] lie in front of [B]?",
    "Is [A] positioned in front of [B]?",
    "Is [A] closer to camera compared to [B]?",
    "Does [A] come in front of [B]?",
    "Is [A] positioned before [B]?",
    "Is [A] closer to the viewer compared to [B]?",
    "Is the depth of [A] less than that of [B]?",
    "Considering the relative positions of [A] and [B] in the image provided, is [A] in front of [B]?"
]

front_true_responses = [
    "Yes.",
    "Yes, it is.",
    "Yes, it is in front of [B].",
    "That is True.",
    "Yes, [A] is closer to the viewer.",
    "Yes, [A] is closer to the camera.",
    "Yes, [A] is in front of [B].",
    "Yes, the depth of [A] is less than that of [B].",
]

front_false_responses = [
    "No.",
    "No, it is not.",
    "No, it is behind [B].",
    "That is False.",
    "No, [A] is further to the viewer.",
    "No, [A] is further to the viewer.",
    "No, [A] is behind [B].",
    "No, the depth of [A] is greater than that of [B].",
]

wide_predicate_questions = [
    "Is [A] wider than [B]?",
    "Does [A] have a greater width compared to [B]?",
    "Can you confirm if [A] is wider than [B]?",
    "Considering the relative sizes of [A] and [B] in the image provided, is [A] wider than [B]?"
]

wide_true_responses = [
    "Yes.",
    "Yes, [A] is wider than [B].",
    "Indeed, [A] has a greater width compared to [B].",
    "Correct, the width of [A] exceeds that of [B].",
]

wide_false_responses = [
    "No.",
    "No, [A] is not wider than [B].",
    "In fact, [A] might be narrower than [B].",
    "Incorrect, the width of [A] does not surpass that of [B].",
]

thin_predicate_questions = [
    "Is [A] thinner than [B]?",
    "Does [A] have a lesser width compared to [B]?",
    "Can you confirm if [A] is thinner than [B]?",
    "Considering the relative sizes of [A] and [B] in the image provided, is [A] thinner than [B]?"
]

thin_true_responses = [
    "Yes.",
    "Yes, [A] is thinner than [B].",
    "Indeed, [A] has a lesser width compared to [B].",
    "Correct, the width of [A] is less than that of [B].",
]

thin_false_responses = [
    "No.",
    "No, [A] is not thinner than [B].",
    "In fact, [A] might be wider than [B].",
    "Incorrect, the width of [A] is not less than that of [B].",
]

tall_predicate_questions = [
    "Is [A] taller than [B]?",
    "Does [A] have a greater height compared to [B]?",
    "Can you confirm if [A] is taller than [B]?",
    "Considering the relative sizes of [A] and [B] in the image provided, is [A] taller than [B]?"
]

tall_true_responses = [
    "Yes.",
    "Yes, [A] is taller than [B].",
    "Indeed, [A] has a greater height compared to [B].",
    "Correct, [A] is much taller as [B].",
]

tall_false_responses = [
    "No.",
    "No, [A] is not taller than [B].",
    "In fact, [A] may be shorter than [B].",
    "Incorrect, the height of [A] is not larger of that of [B].",
]

short_predicate_questions = [
    "Is [A] shorter than [B]?",
    "Does [A] have a lesser height compared to [B]?",
    "Can you confirm if [A] is shorter than [B]?",
    "Considering the relative sizes of [A] and [B] in the image provided, is [A] shorter than [B]?"
]

short_true_responses = [
    "Yes.",
    "Yes, [A] is shorter than [B].",
    "Indeed, [A] has a lesser height compared to [B].",
    "Correct, [A] is not as tall as [B].",
]

short_false_responses = [
    "No.",
    "No, [A] is not shorter than [B].",
    "In fact, [A] may be taller than [B].",
    "Incorrect, the height of [A] does not fall short of that of [B].",
]

big_predicate_questions = [
    "Is [A] bigger than [B]?",
    "Does [A] have a larger size compared to [B]?",
    "Can you confirm if [A] is bigger than [B]?",
    "Considering the relative sizes of [A] and [B] in the image provided, is [A] bigger than [B]?"
]

big_true_responses = [
    "Yes.",
    "Yes, [A] is bigger than [B].",
    "Indeed, [A] has a larger size compared to [B].",
    "Correct, [A] is larger in size than [B].",
]

big_false_responses = [
    "No.",
    "No, [A] is not bigger than [B].",
    "Actually, [A] might be smaller than [B].",
    "Incorrect, [A] is not larger than [B].",
]

small_predicate_questions = [
    "Is [A] smaller than [B]?",
    "Does [A] have a smaller size compared to [B]?",
    "Can you confirm if [A] is smaller than [B]?",
    "Considering the relative sizes of [A] and [B] in the image provided, is [A] smaller than [B]?"
]

small_true_responses = [
    "Yes.",
    "Yes, [A] is smaller than [B].",
    "Indeed, [A] has a smaller size compared to [B].",
    "Correct, [A] occupies less space than [B].",
]

small_false_responses = [
    "No.",
    "No, [A] is not smaller than [B].",
    "Actually, [A] might be larger than [B].",
    "Incorrect, [A] is not smaller in size than [B].",
]

touch_predicate_questions = [
    "Is [A] beside [B]?",
    "Is [A] touching [B]?",
    "Is [A] next to [B]?",
    "Is [A] in contact with [B]?",
    "Is [A] with [B]?",
    "Are [A] and [B] making contact?",
    "Is [A] placed right next to [B]?",
    "Are [A] and [B] beside each other?",
    "Does [A] touch [B]?",
    "Is [A] directly adjacent to [B]?",
    "Can you see [A] touching [B]?",
    "Is [A] next to [B] and touching it?",
    "Is the surface of [A] in direct contact with [B]?"
]
touch_true_responses = [
    "Yes.",
    "Yes, [A] is touching [B].",
    "Yes, [A] is next to [B].",
    "Yes, [A] is beside [B].",
    "Yes, [A] is in contact with [B].",
    "Yes, [A] is with [B].",
    "Indeed, [A] and [B] are beside each other and touching.",
    "Yes, [A] is right next to [B] and making contact.",
    "Yes, the surface of [A] is in contact with [B].",
    "Absolutely, [A] is next to and touching [B].",
    "Yes, [A] and [B] clearly make contact.",
]

touch_false_responses = [
    "No.",
    "No, [A] is not touching [B].",
    "No, [A] is not next to [B].",
    "No, [A] is not beside [B].",
    "No, [A] is not in contact with [B].",
    "No, [A] is not with [B].",
    "[A] and [B] are not in contact.",
    "There is a gap between [A] and [B].",
    "[A] is not next to [B], and they're not touching.",
    "They are not placed beside each other.",
    "No, [A] is not making contact with [B].",
    "[A] and [B] are clearly separated.",
]

far_from_predicate_questions = [
    "Is [A] far from [B]?",
    "Is [A] far away from [B]?",
    "Are [A] and [B] far apart?",
    "Would you say [A] is a long distance from [B]?",
    "Is there a large distance between [A] and [B]?",
    "Are [A] and [B] located far from each other?",
    "Is [A] positioned far away from [B]?",
    "Is [A] not near [B]?",
    "Is [A] not close to [B]?",
    "Would you consider [A] to be distant from [B]?"
]

far_from_true_responses = [
    "Yes.",
    "Yes, [A] is far from [B].",
    "[A] is far away from [B].",
    "That’s right, there is a large distance between [A] and [B].",
    "Yes, [A] and [B] are quite far apart.",
    "[A] is positioned a significant distance from [B].",
    "Indeed, [A] is not near [B].",
    "Yes, [A] and [B] are located far from each other.",
    "Absolutely, [A] is distant from [B].",
]

far_from_false_responses = [
    "No.",
    "No, [A] is not far from [B].",
    "[A] is actually quite close to [B].",
    "No, there isn’t a large distance between [A] and [B].",
    "[A] is near [B], not far away.",
    "They are positioned close to each other.",
    "No, [A] is not far away from [B].",
    "Actually, [A] and [B] are a little close together.",
    "No, [A] is in close proximity to [B].",
    "That’s not correct — [A] is a little close to [B].",
]

contain_predicate_questions = [
    "Does [A] contain [B]?",
    "Is [A] surrounding [B]?",
    "Is [B] inside [A]?",
    "Is [B] a part of [A]?",
    "Would you say [A] contains [B]?",
    "Can [B] be found inside [A]?",
    "Is [B] located within [A]?",
    "Is [B] surrounded by [A]?",
    "Is [B] completely or partially inside [A]?",
    "Would you say [B] is part of [A]'s contents?",
    "Could [B] be considered to be inside [A]?"
]

contain_true_responses = [
    "Yes.",
    "Yes, [A] contains [B].",
    "Yes, [B] is inside [A].",
    "That's correct, [B] is inside [A].",
    "Yes, [B] is a part of [A].",
    "Indeed, [B] is located within [A].",
    "Absolutely, [B] is inside [A].",
    "Yes, [B] can be found within [A].",
    "Yes, [B] is surrounded by [A].",
    "Yes, [A] is surrounding [B].",
    "Yes, [B] is a part of [A].",
]

contain_false_responses = [
    "No.",
    "No, [A] does not contain [B].",
    "No, [B] is not inside [A].",
    "Actually, [B] is outside [A].",
    "No, [B] is not a part of [A].",
    "That’s incorrect, [B] is not inside [A].",
    "No, [B] is located outside of [A].",
    "Definitely not — [B] is not inside [A].",
    "No, [B] is not surrounded by [A].",
]

outside_predicate_questions = [
    "Is [A] outside of [B]?",
    "Is [A] located outside [B]?",
    "Would you say [A] is outside [B]?",
    "Is [A] positioned beyond the bounds of [B]?",
    "Is [A] completely or partially outside of [B]?",
    "Is [A] not inside [B]?",
    "Is [A] not within [B]?",
    "Can we say [A] lies outside [B]?",
    "Is [A] outside [B]?"
]

outside_true_responses = [
    "Yes.",
    "Yes, [A] is outside of [B].",
    "That's correct, [A] is outside of [B].",
    "Yes, [A] is located beyond the bounds of [B].",
    "Indeed, [A] is completely outside [B].",
    "Yes, [A] is not within [B].",
    "[A] lies outside [B]'s area.",
    "Absolutely, [A] is external to [B].",
    "[A] is positioned outside [B].",
]

outside_false_responses = [
    "No.",
    "No, [A] is not outside of [B].",
    "Actually, [A] is at least partially inside [B].",
    "Actually, [A] is within [B].",
    "That's incorrect, [A] is not completely outside [B].",
    "No, [A] is inside or overlapping with [B].",
    "No, [A] is inside [B]'s boundary.",
    "No, most part of [A] lies within [B].",
    "No, [A] is not entirely external to [B].",
]

# point predicate questions --------------------------------------------------------

# point_left_predicate_questions = [
# ]

# point_left_true_responses = [
# ]

# point_left_false_responses = [
# ]

# point_right_predicate_questions = [
# ]

# point_right_true_responses = [
# ]

# point_right_false_responses = [
# ]

# point_above_predicate_questions = [
# ]

# point_above_true_responses = [
# ]

# point_above_false_responses = [
# ]

# point_below_predicate_questions = [
# ]

# point_below_true_responses = [
# ]

# point_below_false_responses = [
# ]

point_close_predicate_questions = [
    "Is point [A] in front of point [B]?",
    "Is point [A] less distant than point [B]?",
    "Does point [A] lie in front of point [B]?",
    "Is point [A] positioned in front of point [B]?",
    "Is point [A] closer to camera compared to point [B]?",
    "Does point [A] come closer to viewer compared to point [B]?",
    "Does point [A] come in front of point [B]?",
    "Is point [A] positioned before point [B]?",
    "Is point [A] closer to viewer compared to point [B]?",
    "Considering the positions of points [A] and [B], is point [A] closer to camera compared to point [B]?"
]

point_close_true_responses = [
    "Yes.",
    "Yes, it is.",
    "Yes, it is in front of point [B].",
    "That is True.",
    "Yes, point [A] is closer to viewer.",
    "Yes, point [A] is in front of point [B].",
]

point_close_false_responses = [
    "No.",
    "No, it is not.",
    "No, it is behind [B].",
    "That is False.",
    "No, [A] is further to viewer.",
    "No, [A] is behind [B].",
]

point_far_predicate_questions = [
    "Is point [A] behind point [B]?",
    "Is point [A] more distant than point [B]?",
    "Does point [A] lie behind point [B]?",
    "Is point [A] positioned behind point [B]?",
    "Is point [A] farther from camera compared to point [B]?",
    "Does point [A] come farther from viewer compared to point [B]?",
    "Does point [A] come behind point [B]?",
    "Is point [A] positioned after point [B]?",
    "Is point [A] farther from viewer compared to point [B]?",
    "Considering the positions of points [A] and [B], is point [A] farther from camera compared to point [B]?"
]

point_far_true_responses = [
    "Yes.",
    "Yes, it is.",
    "Yes, it is behind point [B].",
    "That is True.",
    "Yes, point [A] is farther from viewer.",
    "Yes, point [A] is behind point [B].",
]

point_far_false_responses = [
    "No.",
    "No, it is not.",
    "No, it is in front of [B].",
    "That is False.",
    "No, [A] is closer to viewer.",
    "No, [A] is in front of [B].",
]

# obj Choice ------------------------------------------------------------------------
left_choice_questions = [
    "Which is more to the left, [A] or [B]?",
    "Between [A] and [B], which one appears on the left side from the viewer's perspective?",
    "Who is positioned more to the left, [A] or [B]?",
    "Considering the positions of objects [A] and [B] in the image provided, who is more to the left, [A] or [B]?"
]

left_choice_responses = [
    "[X].",
    "[X] is more to the left.",
    "From the viewer's perspective, [X] appears more on the left side.",
    "Positioned to the left is [X].",
]

right_choice_questions = [
    "Which is more to the right, [A] or [B]?",
    "Between [A] and [B], which one appears on the right side from the viewer's perspective?",
    "Who is positioned more to the right, [A] or [B]?",
    "Considering the positions of objects [A] and [B] in the image provided, who is more to the right, [A] or [B]?"
]

right_choice_responses = [
    "[X].",
    "[X] is more to the right.",
    "From the viewer's perspective, [X] appears more on the right side.",
    "Positioned to the right is [X].",
]

# -----------------------
# 📷 Image Coordinate System
# -----------------------

image_above_choice_questions = [
    "From the image's perspective, which is above, [A] or [B]?",
    "From the image's perspective, who appears higher, [A] or [B]?",
    "From the image's perspective, which one is positioned higher, [A] or [B]?",
    "From the image's perspective, between [A] and [B], who is located above?",
]

image_above_choice_responses = [
    "[X].",
    "[X], from the image's perspective.",
    "[X] appears higher in the image.",
    "From the image's view, [X] is above.",
    "[X] is shown above in the image.",
]

image_below_choice_questions = [
    "From the image's perspective, which is below, [A] or [B]?",
    "From the image's perspective, who appears lower, [A] or [B]?",
    "From the image's perspective, which one is positioned lower, [A] or [B]?",
    "From the image's perspective, between [A] and [B], who is located below?",
]

image_below_choice_responses = [
    "[X].",
    "[X], from the image's perspective.",
    "[X] appears lower in the image.",
    "From the image's view, [X] is below.",
    "[X] is shown below in the image.",
]

# -----------------------
# 🌍 World Coordinate System
# -----------------------

world_above_choice_questions = [
    "From a real-world perspective, which is physically above, [A] or [B]?",
    "From a real-world perspective, who is located higher, [A] or [B]?",
    "From a real-world perspective, which object stands above the other?",
    "From a real-world perspective, between [A] and [B], who is vertically higher?",
]

world_above_choice_responses = [
    "[X].",
    "[X], from a real-world perspective.",
    "[X] is physically higher.",
    "From a 3D spatial view, [X] is above.",
    "In real-world coordinates, [X] is higher.",
]

world_below_choice_questions = [
    "From a real-world perspective, which is physically below, [A] or [B]?",
    "From a real-world perspective, who is located lower, [A] or [B]?",
    "From a real-world perspective, which object rests below the other?",
    "From a real-world perspective, between [A] and [B], who is vertically lower?",
]

world_below_choice_responses = [
    "[X].",
    "[X], from a real-world perspective.",
    "[X] is physically lower.",
    "From a 3D spatial view, [X] is below.",
    "In real-world coordinates, [X] is lower.",
]

front_choice_questions = [
    "Which is in front, [A] or [B]?",
    "Between [A] and [B], which one is positioned in front?",
    "Who is more forward, [A] or [B]?",
    "Which object is closer to the camera, [A] or [B]?",
    "Which object is closer to the camera taking this photo, [A] or [B]?"
    "Considering the positions of objects [A] and [B] in the image provided, who is in front, [A] or [B]?"
]

front_choice_responses = [
    "[X].",
    "[X] is in front.",
    "Positioned in front is [X].",
    "[X] is more forward.",
    "[X] is closer to the camera."
]

behind_choice_questions = [
    "Which is behind, [A] or [B]?",
    "Between [A] and [B], which one is positioned behind?",
    "Who is more distant, [A] or [B]?",
    "Which object is further away from the camera, [A] or [B]?",
    "Which object is further away from the camera taking this photo, [A] or [B]?"
    "Considering the positions of objects [A] and [B] in the image provided, who is behind, [A] or [B]?"
]

behind_choice_responses = [
    "[X].",
    "[X] is behind.",
    "Positioned behind is [X].",
    "[X] is more distant.",
    "[X] is further away from the camera."
]

tall_choice_questions = [
    "Who is taller, [A] or [B]?",
    "Between [A] and [B], which one has more height?",
    "Which of these two, [A] or [B], stands taller?",
    "Considering the sizes of objects [A] and [B] in the image provided, who is taller, [A] or [B]?"
]

tall_choice_responses = [
    "[X].",
    "[X] is taller.",
    "With more height is [X].",
    "Standing taller between the two is [X].",
]

short_choice_questions = [
    "Who is shorter, [A] or [B]?",
    "Between [A] and [B], which one has less height?",
    "Which of these two, [A] or [B], stands shorter?",
    "Considering the sizes of objects [A] and [B] in the image provided, who is shorter, [A] or [B]?"
]

short_choice_responses = [
    "[X].",
    "[X] is shorter.",
    "With less height is [X].",
    "Standing shorter between the two is [X].",
]

big_choice_questions = [
    "Who is bigger, [A] or [B]?",
    "Between [A] and [B], which one has larger size?",
    "Which of these two, [A] or [B], is bigger?",
    "Considering the sizes of objects [A] and [B] in the image provided, who is bigger, [A] or [B]?"
]

big_choice_responses = [
    "[X].",
    "[X] is bigger.",
    "With larger size is [X].",
    "Bigger between the two is [X].",
]

small_choice_questions = [
    "Who is smaller, [A] or [B]?",
    "Between [A] and [B], which one has smaller size?",
    "Which of these two, [A] or [B], is smaller?",
    "Considering the sizes of objects [A] and [B] in the image provided, who is smaller, [A] or [B]?"
]

small_choice_responses = [
    "[X].",
    "[X] is smaller.",
    "With smaller size is [X].",
    "Smaller between the two is [X].",
]

wide_choice_questions = [
    "Which object is wider, [A] or [B]?",
    "Between [A] and [B], which one has larger width?",
    "Which of these two, [A] or [B], is wider?",
    "Considering the sizes of objects [A] and [B] in the image provided, who is wider, [A] or [B]?"
]

wide_choice_responses = [
    "[X].",
    "[X] is wider.",
    "With larger width is [X].",
    "Wider between the two is [X].",
]

thin_choice_questions = [
    "Which object is thinner, [A] or [B]?",
    "Between [A] and [B], which one has smaller width?",
    "Which of these two, [A] or [B], is thinner?",
    "Considering the sizes of objects [A] and [B] in the image provided, who is thinner, [A] or [B]?"
]

thin_choice_responses = [
    "[X].",
    "[X] is thinner.",
    "With smaller width is [X].",
    "Thinner between the two is [X].",
]

# point choice -----------------------------------------------
# point_left_choice_questions = [

# ]

# point_left_choice_responses = [
# ]

# point_right_choice_questions = [
# ]

# point_right_choice_responses = [
# ]

# point_above_choice_questions = [
# ]

# point_above_choice_responses = [
# ]

# point_below_choice_questions = [
# ]

# point_below_choice_responses = [
# ]

point_close_choice_questions = [
    "Which is in front, point [A] or point [B]?",
    "Between point [A] and point [B], which one is positioned in front?",
    "Who is more forward, [A] or [B]?",  	
    "Which point is closer to the camera, point [A] or point [B]?",
    "Considering the points [A] and [B], who is in front, point [A] or point [B]?"
]

point_close_choice_responses = [
    "Point [X]",
    "The point [X] is in front.",
    "Positioned in front is point [X].",
    "The point [X] is more forward.",
    "The point [X] is closer.",
    "The point [X] is closer to the camera."
]

point_far_choice_questions = [
    "Which is behind, point [A] or point [B]?",
    "Between point [A] and point [B], which one is positioned behind?",
    "Who is more distant from viewer, [A] or [B]?",
    "Which point is closer to the camera, point [A] or point [B]?",
    "Considering the points [A] and [B], who is behind, point [A] or point [B]?"
]

point_far_choice_responses = [
    "Point [X]",
    "The point [X] is behind.",
    "Positioned behind is point [X].",
    "The point [X] is more distant.",
    "The point [X] is farther.",
    "The point [X] is farther from the camera."
]

# Direction
direction_questions = ["If you are at [A], where will you find [B]?"]

direction_responses = ["[B] is roughly at [X] o'clock from [A].", "[A] will find [B] around the [X] o'clock direction."]


# Vertical and horizonal distance
vertical_distance_questions = [
    "What is the vertical distance between [A] and [B]?",
    "How far apart are [A] and [B] vertically?",
    "How distant is [A] from [B] vertically?",
    "How far is [A] from [B] vertically?",
    "Could you measure the vertical distance between [A] and [B]?",
    "Can you tell me the vertical distance between [A] and [B]?",
    "How far away is [A] from [B] vertically?",
    "Estimate the vertical distance between [A] and [B].",
    "Could you provide the vertical distance between [A] and [B]?",
    "How much distance is there between [A] and [B] vertically?",
    "Tell me the distance between [A] and [B] vertically.",
    "Give me the vertical distance from [A] to [B].",
    "Measure the vertical distance from [A] to [B].",
    "Measure the distance between [A] and [B] vertically.",
]

vertical_distance_answers = [
    "[X]",
    "[A] and [B] are [X] apart vertically.",
    "[A] is [X] away from [B] vertically.",
    "A vertical distance of [X] exists between [A] and [B].",
    "[A] is [X] from [B] vertically.",
    "[A] and [B] are [X] apart vertically from each other.",
    "Vertically, They are [X] apart.",
    "The vertical distance of [A] from [B] is [X].",
    "They are [X] apart.",
    "It is approximately [X].",
]

vertical_distance_supporting_answers = [
    "[bottom] directly supports [top], with no vertical distance between them.",
    "There is no vertical gap, as [bottom] is directly beneath and supporting [top].",
    "[top] is directly supported by [bottom], indicating zero vertical separation.",
    "With [bottom] supporting [top], they are in immediate vertical contact.",
    "[bottom] and [top] are connected vertically with [bottom] providing support directly below [top].",
    "The vertical support between [bottom] and [top] is direct, leaving no space.",
    "[bottom] directly below [top] serves as a supporting structure with no vertical distance.",
    "[top] receives direct support from [bottom] without any vertical gap.",
    "In their vertical arrangement, [bottom] supports [top] immediately, with no distance apart.",
    "Vertically, [bottom] is the immediate supporter of [top], with no discernible distance between them.",
]

vertical_distance_overlapping_answers = [
    "[A] and [B] overlap, so it's hard to tell how far apart they are vertically.",
    "Because [A] and [B] overlap vertically, figuring out the distance is hard.",
    "The overlap between [A] and [B] makes the vertical distance unclear.",
    "[A] and [B] are overlapping, which makes knowing the vertical distance difficult.",
    "It's hard to say the vertical distance since [A] and [B] overlap.",
    "Since [A] and [B] overlap, the vertical distance between them is hard to tell.",
    "[A] and [B]'s vertical overlap leaves the distance between them uncertain.",
    "Overlapping [A] and [B] makes it challenging to determine their vertical distance.",
]

horizontal_distance_questions = [
    "What is the horizontal distance between [A] and [B]?",
    "How far apart are [A] and [B] horizontally?",
    "How distant is [A] from [B] horizontally?",
    "How far is [A] from [B] horizontally?",
    "Could you measure the horizontal distance between [A] and [B]?",
    "Can you tell me the horizontal distance of [A] from [B]?",
    "Can you give me an estimation of the horizontal distance between [A] and [B]?",
    "Could you provide the horizontal distance between [A] and [B]?",
    "How much distance is there between [A] and [B] horizontally?",
    "Tell me the distance between [A] and [B] horizontally.",
    "Give me the horizontal distance from [A] to [B].",
    "Horizontal gap between [A] and [B].",
    "Measure the horizontal distance from [A] to [B].",
    "Measure the distance between [A] and [B] horizontally.",
]

horizontal_distance_answers = [
    "[X]",
    "[A] and [B] are [X] apart horizontally.",
    "[A] is [X] away from [B] horizontally.",
    "A horizontal distance of [X] exists between [A] and [B].",
    "[A] is [X] from [B] horizontally.",
    "[A] and [B] are [X] apart horizontally from each other.",
    "Horizontally, They are [X] apart.",
    "The horizontal distance of [A] from [B] is [X].",
    "They are [X] apart.",
    "It is approximately [X].",
]

# Width/Height
width_questions = [
    "Measure the width of [A].",
    "Determine the horizontal dimensions of [A].",
    "Find out how wide [A] is.",
    "What is the width of [A]?",
    "How wide is [A]?",
    "What are the dimensions of [A] in terms of width?",
    "Could you tell me the horizontal size of [A]?",
    "What is the approximate width of [A]?",
    "How wide is [A]?",
    "How much space does [A] occupy horizontally?",
    "How big is [A] in terms of width?",
]
width_responses = [
    "[X].",
    "The width of [A] is [X].",
    "[A] is [X] wide.",
    "[A] is [X] in width.",
    "It is [X].",
]

height_questions = [
    "Measure the height of [A].",
    "Determine the vertical dimensions of [A].",
    "Find out how tall [A] is.",
    "What is the height of [A]?",
    "How tall is [A]?",
    "What are the dimensions of [A] in terms of height?",
    "Could you tell me the vericall size of [A]?",
    "What is the approximate height of [A]?",
    "How tall is [A]?",
    "How much space does [A] occupy vertically?",
    "How tall is [A]?",
    "How tall is [A] in terms of height?",
]
height_responses = [
    "[X].",
    "The height of [A] is [X].",
    "[A] is [X] tall.",
    "[A] is [X] in height.",
    "It is [X].",
]
how_horizontal_face_object_questions = [
    "I need to go to [A]. Which direction should I rotate to face it? [option]",
    "To face [A], which direction should I rotate? [option]",
    "Which direction should I rotate to look at [A]? [option]",
    "If I want to face [A], should I rotate left or right? [option]",
    "To turn toward [A], should I rotate left or right? [option]",
    "In which direction should I rotate to look at [A]? [option]",
    "To align my view with [A], should I rotate left or right? [option]",
    "Should I rotate left or right to face [A]? [option]",
    "To see [A] from here, which way should I rotate? [option]",
    "Should I rotate my view to the left or to the right to look at [A]? [option]"
]

how_vertical_face_object_questions = [
    "I want to look at [A]. Should I rotate my view up or down? [option]",
    "To face [A], do I need to rotate up or down? [option]",
    "Should I rotate up or down to look at [A]? [option]",
    "From here, should I rotate up or down to see [A]? [option]",
    "Which direction should I rotate to face [A] — up or down? [option]",
    "If I want to face [A], should I rotate upward or downward? [option]",
    "To align my view with [A], should I rotate up or down? [option]",
    "Should I look upward or downward to see [A]? [option]",
    "To see [A], do I need to rotate up or down? [option]",
    "Which direction should I rotate to look at [A] — up or down? [option]"
]

facing_object_questions = [
    "Is [A] facing towards [B]?",
    "Is [A] oriented towards [B]?",
    "Is [A] aimed at [B]?",
    "Does [A] turn towards [B]?",
    "Could you tell me if [A] is facing [B]?",
    "Could you tell me if [A] is turned towards [B]?",
]

facing_object_true_responses = [
    "Yes.",
    "Yes, [A] faces towards [B]",
    "Yes, [A] is oriented towards [B].",
    "Yes, [A] is aimed at [B].",
    "Yes, [A] is facing [B].",
    "Yes, [A] is turned towards [B]."
]

facing_object_false_responses = [
    "No.",
    "No, [A] is not facing towards [B].",
    "No, [A] is not oriented towards [B].",
    "No, [A] is not aimed at [B].",
    "No, [A] does not turn towards [B].",
    "No, [A] is not turned towards [B]."
]
facing_away_object_questions = [
    "Is [A] facing away from [B]?",
    "Is [A] turned away from [B]?",
    "Is [A] looking in the opposite direction of [B]?",
    "Is [A] positioned with its back to [B]?",
    "Is [A] oriented away from [B]?",
    "Is [B] at the back of [A]?"
]
facing_away_object_true_responses = [
    "Yes.",
    "Yes, [A] is facing away from [B].",
    "Correct, [A] is looking away from [B].",
    "Yes, [A] is positioned with its back facing [B].",
    "That’s right, [A] is facing away from [B].",
    "Absolutely, [A] is directed away from [B].",
    "Yes, [A]'s orientation is away from [B].",
    "Yes, [B] is at the back of [A]."
]

facing_away_object_false_responses = [
    "No.",
    "No, [A] is not facing away from [B].",
    "[A] is not turned away from [B].",
    "[A] does not have its back to [B].",
    "That’s not correct — [A] is not looking away from [B].",
    "No, [A] is not facing the opposite direction of [B].",
    "No, [A]'s orientation is not away from [B].",
    "No, [B] is not at the back of [A]."
]

angle_of_objects_questions = [
    "What is the angle between the front of [A] and the front of [B]?",
    "How many degrees apart are the front directions of [A] and [B]?",
    "Could you tell me the angle between the facing directions of [A] and [B]?",
    "How different are the orientations of [A] and [B] in degrees?",
    "What's the angular difference between [A] and [B]'s front directions?",
    "What is the degree difference between the fronts of [A] and [B]?",
    "Can you tell me how much [A] and [B] differ in facing direction?"
]

angle_of_objects_responses = [
    "[X] degrees.",
    "The angle between the front of [A] and the front of [B] is [X] degrees.",
    "They differ by [X] degrees in their facing directions.",
    "The angular difference between [A] and [B] is [X] degrees.",
    "The front directions of [A] and [B] are [X] degrees apart.",
    "[A] and [B] are facing [X] degrees away from each other.",
    "There is a [X]-degree angle between the fronts of [A] and [B].",
    "[X] degrees separate the front orientations of [A] and [B]."
]

# choice relation

choice_left_right_questions = [
    "Considering the relative positions of [A] and [B] in the image provided, is [A] to the left or to the right of [B]?",
    "Is [A] to the left or to the right of [B] in the image?",
    "Based on their positions, is [A] located to the left or right of [B]?",
    "In the image, is [A] on the left side or the right side of [B]?",
    "Would you say [A] is to the left or to the right of [B] in the picture?",
    "Visually, is [A] positioned to the left or to the right of [B]?",
]

choice_left_responses = [
    "[A] is to the left of [B].",
    "In the image, [A] appears on the left side of [B].",
    "Based on their positions, [A] is located to the left of [B].",
    "[A] is positioned on [B]'s left side.",
    "Clearly, [A] is on the left of [B] in the image.",
    "From the image, it's evident that [A] is to the left of [B]."
]

choice_right_responses = [
    "[A] is to the right of [B].",
    "In the image, [A] appears on the right side of [B].",
    "Based on their positions, [A] is located to the right of [B].",
    "[A] is positioned on [B]'s right side.",
    "Clearly, [A] is on the right of [B] in the image.",
    "From the image, it's evident that [A] is to the right of [B]."
]

# -----------------------
# 📷 Image Coordinate System
# -----------------------

image_choice_above_below_questions = [
    "From the image's perspective, is [A] above or below [B]?",
    "From the image's perspective, is [A] located above or below [B]?",
    "From the image's perspective, is [A] positioned above or below [B]?",
    "From the image's perspective, relative to [B], is [A] above or below?",
]

image_choice_above_responses = [
    "[A] is above [B].",
    "From the image's perspective, [A] appears above [B].",
    "Based on their image positions, [A] is located above [B].",
    "[A] is situated higher than [B] in the image.",
    "Clearly, from the image's perspective, [A] is above [B]."
]

image_choice_below_responses = [
    "[A] is below [B].",
    "From the image's perspective, [A] appears below [B].",
    "Based on their image positions, [A] is located beneath [B].",
    "[A] is situated lower than [B] in the image.",
    "Clearly, from the image's perspective, [A] is below [B]."
]

# -----------------------
# 🌍 World Coordinate System
# -----------------------

world_choice_above_below_questions = [
    "From a real-world perspective, is [A] above or below [B]?",
    "From a real-world perspective, is [A] physically located above or below [B]?",
    "From a real-world perspective, is [A] positioned above or below [B]?",
    "From a real-world perspective, relative to [B], is [A] vertically above or below?",
]

world_choice_above_responses = [
    "[A] is above [B].",
    "From a real-world perspective, [A] is physically above [B].",
    "In terms of real-world spatial position, [A] is above [B].",
    "[A] is situated higher than [B] in the real world.",
    "Clearly, from a real-world perspective, [A] is above [B]."
]

world_choice_below_responses = [
    "[A] is below [B].",
    "From a real-world perspective, [A] is physically below [B].",
    "In terms of real-world spatial position, [A] is below [B].",
    "[A] is situated lower than [B] in the real world.",
    "Clearly, from a real-world perspective, [A] is below [B]."
]

choice_front_behind_questions = [
    "Is [A] in front of or behind [B] in the image?",
    "Considering their positions, is [A] located in front of or behind [B]?",
    "In the image, is [A] positioned in front of or behind [B]?",
    "Relative to [B], is [A] in front or behind?",
]

choice_front_responses = [
    "[A] is in front of [B].",
    "In the image, [A] appears in front of [B].",
    "[A] is positioned closer to the viewer than [B].",
    "Clearly, [A] is in front of [B].",
    "Visually, [A] is located in front of [B]."
]

choice_behind_responses = [
    "[A] is behind [B].",
    "In the image, [A] appears behind [B].",
    "[A] is positioned farther from the viewer than [B].",
    "Clearly, [A] is behind [B].",
    "Visually, [A] is located behind [B]."
]

choice_wide_thin_questions = [
    "Considering the positions of [A] and [B] in the image, is [A] wider or thinner than [B]?",
    "Is [A] wider or thinner than [B]?",
    "In terms of width, does [A] look wider or thinner when compared to [B]?",
    "Looking at their shapes, would you say [A] is wider or thinner than [B]?",
]

choice_wide_responses = [
    "[A] is wider than [B].",
    "In the image, [A] appears to be wider than [B].",
    "Considering their positions, [A] looks broader than [B].",
    "Clearly, [A] has more width compared to [B]."
]

choice_thin_responses = [
    "[A] is thinner than [B].",
    "In the image, [A] appears to be more narrow than [B].",
    "Considering their positions, [A] looks slimmer than [B].",
    "Clearly, [A] has less width compared to [B]."
]

choice_tall_short_questions = [
    "Considering the positions of [A] and [B] in the image, is [A] taller or shorter than [B]?",
    "Is [A] taller or shorter than [B]?",
    "In terms of height, does [A] look taller or shorter compared to [B]?",
    "From their relative heights in the image, would you say [A] is taller or shorter than [B]?",
]

choice_tall_responses = [
    "[A] is taller than [B].",
    "In the image, [A] appears to be taller than [B].",
    "Considering their positions, [A] has more height than [B].",
    "Clearly, [A] is higher in height compared to [B]."
]

choice_short_responses = [
    "[A] is shorter than [B].",
    "In the image, [A] appears to be shorter than [B].",
    "Considering their positions, [A] has less height than [B].",
    "Clearly, [A] is lower in height compared to [B]."
]

choice_big_small_questions = [
    "Considering the positions of [A] and [B] in the image, is [A] bigger or smaller than [B]?",
    "Is [A] bigger or smaller than [B]?",
    "In terms of size, does [A] appear bigger or smaller than [B]?",
    "Looking at the image, does [A] seem bigger or smaller compared to [B]?",
    "Based on their sizes in the image, would you say [A] is bigger or smaller than [B]?"
]

choice_big_responses = [
    "[A] is bigger than [B].",
    "In the image, [A] appears to be larger than [B].",
    "Considering their positions, [A] takes up more space than [B].",
    "Clearly, [A] is larger in size than [B]."
]

choice_small_responses = [
    "[A] is smaller than [B].",
    "In the image, [A] appears to be smaller than [B].",
    "Considering their positions, [A] takes up less space than [B].",
    "Clearly, [A] is smaller in size than [B]."
]

choice_point_close_far_questions = [
    "Considering the positions of point [A] and point [B], is point [A] closer or farther from the camera than point [B]?",
    "Is point [A] closer or farther from the camera than point [B]?",
    "Is point [A] positioned closer to the camera than point [B]?",
    "Does point [A] appear closer or farther from the camera than point [B]?"
]

choice_point_close_responses = [
    "Point [A].",
    "Point [A] is closer to the camera than point [B].",
    "Point [A] appears to be closer to the viewer than point [B].",
    "Point [A] is positioned closer to the camera compared to point [B].",
    "Clearly, point [A] is closer to the camera than point [B]."
]

choice_point_far_responses = [
    "Point [A].",
    "Point [A] is farther from the camera than point [B].",
    "Point [A] appears to be farther away from the viewer than point [B].",
    "Point [A] is positioned farther from the camera compared to point [B].",
    "Clearly, point [A] is more distant from the camera than point [B]."
]

choice_inside_outside_questions = [
    "Is [A] inside or outside of [B]?",
    "Would you say [A] is inside or outside [B]?",
    "Choose the correct answer: Is [A] inside [B] or outside it?",
    "Is [A] spatially inside [B], or outside of it?",
    "Is [A] situated inside [B] or outside?",
    "Do you think [A] is within [B], or outside of it?",
    "Is [A] inside the boundaries of [B], or outside?",
    "Which is correct: [A] is inside [B], or outside of it?"
]

choice_inside_responses = [
    "[A] is inside [B].",
    "The correct answer is: inside.",
    "Yes, [A] is enclosed within [B].",
    "[A] is located inside [B].",
    "[A] lies within the bounds of [B].",
    "[A] is spatially positioned inside [B].",
    "[A] exists entirely within [B].",
    "[A] fits inside [B].",
    "[A] is contained in [B].",
    "[A] can be found inside [B]."
]

choice_outside_responses = [
    "[A] is outside [B].",
    "The correct answer is: outside.",
    "No, [A] is not inside [B], it's outside.",
    "[A] is located beyond the bounds of [B].",
    "[A] lies outside [B].",
    "[A] is not enclosed by [B].",
    "[A] is spatially situated outside [B].",
    "[A] exists outside the volume of [B].",
    "[A] cannot be found inside [B].",
]

# which obj close to anchor 
close_anchor_questions = [
    "Estimate the real-world distances between objects in this image. Which object is closer to [C], [A] or [B]?",
    "Based on their spatial positions, is [A] or [B] closer to [C]?",
    "From the image, which object appears to be nearer to [C], [A] or [B]?",
    "When comparing their distances from [C], does [A] or [B] seem closer?",
    "Looking at the image, which one is located closer to [C], [A] or [B]?",
    "Which object lies nearer to the anchor point [C], [A] or [B]?",
    "Considering their positions, is [A] positioned closer to [C] than [B]?",
]

close_anchor_responses = [
    "[X].",
    "[X] is closer to [C].",
    "The object closer to [C] is [X].",
    "Based on the image, [X] appears to be nearer to [C].",
    "[X] lies closer to [C] than the other object.",
    "[X] is positioned closer to the anchor point [C].",
    "Among the two, [X] is located nearer to [C].",
]


## Multi Choice

anchor_distance_nearest_multi_choice_questions = [
    "Estimate the real-world distances between objects in this image. Which object is closer to the [anchor] among [options]?",
    "Estimate the real-world distances between objects in this image. Which object is closer to the [anchor]? [options]",
    "Which object is the closest to the [anchor]? Choose among these: [options]",
    "Which is nearer to the [anchor]? [options]",
    "Considering the real-world distances, which object is closest to the [anchor] from the following options: [options]?",
    "Which of these objects: [options], is positioned closest to the [anchor]?",
    "Which object is positioned closest to the [anchor]? Select from: [options]",
    "Based on their relative distances, which object is nearer to the [anchor]? Choose from: [options]",
]

anchor_distance_farthest_multi_choice_questions = [
    "Estimate the real-world distances between objects in this image. Which object is farther from the [anchor] among [options]?",
    "Estimate the real-world distances between objects in this image. Which object is farther from the [anchor]? [options]",
    "Which object is the farthest from the [anchor]? Choose among these: [options]",
    "Which is farther from the [anchor]? [options]",
    "Considering the real-world distances, which object is farthest from the [anchor] from the following options: [options]?",
    "Which of these objects: [options], is positioned farthest from the [anchor]?",
    "Which object is positioned farthest from the [anchor]? Select from: [options]",
    "Based on their relative distances, which object is farther from the [anchor]? Choose from: [options]",
]

depth_nearest_multi_choice_questions = [
    "Which object is closer to the camera taking this photo? [options]",
    "Which point is closer to the camera? [options]",
    "Which object appears closest to the camera in this image? [options]",
    "Which of the following is the closest to the observer? [options]",
    "Among these objects, which one is nearest to the camera? [options]",
]

depth_farthest_multi_choice_questions = [
    "Which object is farther from the camera taking this photo? [options]",
    "Which point is farther to the camera? [options]",
    "Which object appears farthest from the camera in this image? [options]",
    "Which of the following is the farthest from the observer? [options]",
    "Among these objects, which one is farthest from the camera? [options]",
]