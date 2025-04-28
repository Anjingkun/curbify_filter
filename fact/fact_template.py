direction_responses = [
    "[B] is roughly at [X] o'clock from [A].",
    "[A] find [B] around the [X] o'clock direction.",
]

height_answers = [
    "The height of [A] is [X].",
    "[A] is [X] tall.",
    "[A] is [X] in height.",
]

width_answers = [
    "The width of [A] is [X].",
    "[A] is [X] wide.",
    "[A] is [X] in width.",
]

horizontal_distance_answers = [
    "[A] and [B] are [X] apart horizontally.",
    "[A] is [X] away from [B] horizontally.",
    "A horizontal distance of [X] exists between [A] and [B].",
    "[A] is [X] from [B] horizontally.",
    "Horizontally, [A] and [B] are [X] apart.",
    "[A] and [B] are [X] apart horizontally from each other.",
    "The horizontal distance of [A] from [B] is [X].",
]

vertical_distance_answers = [
    "[A] and [B] are [X] apart vertically.",
    "[A] is [X] away from [B] vertically.",
    "A vertical distance of [X] exists between [A] and [B].",
    "[A] is [X] from [B] vertically.",
    "[A] and [B] are [X] apart vertically from each other.",
    "Vertically, [A] and [B] are [X] apart.",
    "The vertical distance of [A] from [B] is [X].",
]

front_true = [
    "The depth of [A] is less than the depth of [B].",
    "[A] is closer to the viewer than [B].",
    "[A] is in front of [B].",
    "[A] is closer to the camera than [B].",
]

front_false = [
    "The depth of [A] is greater than the depth of [B].",
    "[A] is further to the viewer than [B].",
    "[A] is behind [B].",
    "[A] is further to the camera than [B].",
]

small_true_responses = [
    "[A] is smaller than [B].",
    "[A] has a smaller size compared to [B].",
    "[A] occupies less space than [B].",
]

small_false_responses = [
    "[A] is bigger than [B].",
    "[A] has a larger size compared to [B].",
    "[A] is larger in size than [B].",
]

thin_true_responses = [
    "[A] is thinner than [B].",
    "[A] has a lesser width compared to [B].",
    "The width of [A] is less than the width of [B].",
]

thin_false_responses = [
    "[A] might be wider than [B]",
    "The width of [A] surpass the width of [B].",
    "The width of [A] is larger than the width of [B].",
]

short_true_responses = [
    "[A] is shorter than [B].",
    "[A] has a lesser height compared to [B].",
    "[A] is not as tall as [B].",
]

short_false_responses = [
    "[A] is taller than [B].",
    "[A] has a greater height compared to [B].",
    "[A] is much taller as [B].",
]

image_below_true_responses = [
    "From the image's perspective, [A] is below [B].",
    "From the image's perspective, [A] is positioned under [B].",
    "From the image's perspective, [A] is located below [B].",
    "From the image's perspective, [A] is located beneath [B].",
]

image_below_false_responses = [
    "From the image's perspective, [A] is above [B].",
    "From the image's perspective, [A] is positioned over [B].",
    "From the image's perspective, [A] is located above [B].",
    "From the image's perspective, [A] is on the top of [B].",
]

world_below_true_responses = [
    "From a real-world perspective, [A] is physically below [B] based on gravity.",
    "From a real-world perspective, [A] is physically located beneath [B] based on gravity.",
    "From a real-world perspective, [A] is physically under [B] based on gravity.",
]

world_below_false_responses = [
    "From a real-world perspective, [A] is physically above [B] based on gravity.",
    "From a real-world perspective, [A] is physically located over [B] based on gravity.",
    "From a real-world perspective, [A] is physically over [B] based on gravity.",
    "From a real-world perspective, [A] is physically on top of [B] based on gravity.",
    "From a real-world perspective, [A] is situated on [B] based on gravity.",
    "From a real-world perspective, [A] is located higher than [B] based on gravity.",
]

touch_true_responses = [
    "[A] touches [B]. The distance between them is less than 10cm.",
    "[A] is touching [B]. The distance between them is less than 10cm.",
    "[A] is next to [B]. The distance between them is less than 10cm.",
    "[A] is in contect with [B]. The distance between them is less than 10cm.",
    "[A] is beside [B]. The distance between them is less than 10cm.",
    "[A] is adjacent to [B]. The distance between them is less than 10cm.",
]

touch_false_responses = [
    "[A] does not touch [B]. The distance between them is more than 10cm.",
    "[A] is not touching [B]. The distance between them is more than 10cm.",
    "[A] is not next to [B]. The distance between them is more than 10cm.",
    "[A] is not in contact with [B]. The distance between them is more than 10cm.",
    "[A] is not beside [B]. The distance between them is more than 10cm.",
    "[A] is not adjacent to [B]. The distance between them is more than 10cm.",
]

far_from_true_responses = [
    "[A] is far from [B]. The distance between them is more than 1m.",
    "[A] is far away from [B]. The distance between them is more than 1m.",
    "[A] and [B] are far apart. The distance between them is more than 1m.",
    "[A] is a long distance from [B]. The distance between them is more than 1m.",
]

far_from_false_responses = [
    "[A] is not far from [B]. The distance between them is less than 1m.",
    "[A] is a little close to [B]. The distance between them is less than 1m.",
    "[A] is a short distance from [B]. The distance between them is less than 1m.",
]

left_true_responses = [
    "[A] is to the left of [B].",
    "[A] is positioned on the left side of [B].",
    "You'll find [A] to the left of [B].",
]

contain_true_responses = [
    "[A] contains [B].",
    "[A] includes [B].",
    "[A] encloses [B].",
    "[A] surrounds [B].",
    "[B] is inside [A].",
    "[B] is within [A].",
    "[B] is a part of [A].",
]

contain_false_responses = [
    "[B] is outside [A].",
    "[B] is not included in [A].",
    "[B] is not contained by [A].",
    "[B] is not surrounded by [A].",
    "[B] is not a part of [A].",
    "[B] is not inside [A].",
    "[A] doesn't contain [B].",
    "[A] doesn't include [B].",
]

is_facing_true_responses = [
    "[A] faces towards [B].",
    "[A] is facing towards [B].",
    "[A] is looking toward [B].",
    "[A] is orienting towards [B].",
    "[A] aims at [B].",
    "[A] is turned towards [B]."
]

is_facing_false_responses = [
    "[A] isn't facing towards [B].",
    "[A] isn't facing towards [B].",
    "[A] isn't looking toward [B].",
    "[A] isn't orienting towards [B].",
    "[A] isn't aiming at [B].",
    "[A] isn't turned towards [B]."
]

is_facing_away_from_true_responses = [
    "[A] is facing away from [B].",
    "[A] is looking in the opposite direction of [B]?",
    "[A] is looking away from [B].",
    "[A] is orienting away from [B].",
    "[A] is aimed away from [B].",
    "[A] is turned away from [B].",
    "[B] is at the back of [A].",
]

is_facing_away_from_false_responses = [
    "[A] isn't facing away from [B].",
    "[A] isn't looking in the opposite direction of [B]?",
    "[A] isn't looking away from [B].",
    "[A] isn't orienting away from [B].",
    "[A] isn't aimed away from [B].",
    "[A] isn't turned away from [B].",
]

angle_of_object_answers = [
    "The angle between the front of [A] and the front of [B] is [X] degrees.",
    "They differ by [X] degrees in their facing directions.",
    "The angular difference between [A] and [B] is [X] degrees.",
    "The front directions of [A] and [B] are [X] degrees apart.",
    "[A] and [B] are facing [X] degrees away from each other.",
    "There is a [X]-degree angle between the fronts of [A] and [B].",
    "[X] degrees separate the front orientations of [A] and [B]."
]

left_false_responses = [
    "[A] is to the right of [B].",
    "[A] is positioned on the right side of [B].",
    "You'll find [A] to the right of [B].",
]

distance_template_answers = [
    "[A] and [B] are [X] apart.",
    "[A] is [X] away from [B].",
    "A distance of [X] exists between [A] and [B].",
    "[A] is [X] from [B].",
    "[A] and [B] are [X] apart from each other.",
    "The distance of [A] from [B] is [X].",
]

point_close_true_responses = [
    "The depth of point [A] is less than the depth of point [B].",
    "Point [A] is closer to the viewer than point [B].",
    "Point [A] is closer to the camera than point [B].",
    "Point [A] is in front of point [B].",
]

point_close_false_responses = [
    "The depth of point [A] is greater than the depth of point [B].",
    "Point [A] is further to the viewer than point [B].",
    "Point [A] is further to the camera than point [B].",
    "Point [A] is behind point [B].",
]

obj_depth_answers = [
    "[A] and camera are [X] apart.",
    "[A] and viewer are [X] apart.",
    "[A] is [X] away from camera.",
    "[A] is [X] away from viewer.",
    "A distance of [X] exists between [A] and camera.",
    "A distance of [X] exists between [A] and viewer.",
    "[A] is [X] from camera.",
    "[A] is [X] from viewer.",
    "[A] and camera are [X] apart from each other.",
    "[A] and viewer are [X] apart from each other.",
    "The distance of [A] from camera is [X].",
    "The distance of [A] from viewer is [X].",
]

point_depth_answers = [
    "The depth of point [A] is [X].",
    "Point [A] and camera are [X] apart.",
    "Point [A] and viewer are [X] apart.",
    "Point [A] is [X] away from camera.",
    "Point [A] is [X] away from viewer.",
    "A distance of [X] exists between point [A] and camera.",
    "A distance of [X] exists between point [A] and viewer.",
    "Point [A] is [X] from camera.",
    "Point [A] is [X] from viewer.",
    "Point [A] and camera are [X] apart from each other.",
    "Point [A] and viewer are [X] apart from each other.",
    "The distance of point [A] from camera is [X].",
    "The distance of point [A] from viewer is [X].",
]

fine_grain_object_2_point_answers = [
    "[A] is located at point [X]",
    "You can find [A] at point [X].",
    "The position of [A] is at point [X].",
    "The 2D location of [A] is at point [X]." ,
]

point_2_caption_template_answers = [
    "Point [X] is on [A].",
    "Point [X] indicates [A].",
    "Point [X] corresponds to [A].",
    "At point [X] lies [A].",
    "[A] is represented by point [X].",
    "Point [X] marks [A].",
    "[A] is located at point [X].",
]

close_anchor_answers = [
    "Between [A] and [B], [A] is closer to [C].",
    "[A] is closer to [C] than [B] is.",
    "Compared to [B], [A] is nearer to [C].",
    "[C] is closer to [A] than to [B].",
    "[A] lies closer to [C] than [B].",
    "[A] is the closer one to [C] between the two.",
    "If we compare distances to [C], [A] is nearer than [B].",
]