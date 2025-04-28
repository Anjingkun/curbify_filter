left_right_visual_choice_question = [
'''Considering the relative positions of [A] (annotated by the red box) and [B] in the image provided, where is [A] (annotated by the red box) located with respect to the staircase? Select from the following choices."
(A) [option 1]
(B) [option 2]''',
'''From the image, what is the correct spatial relationship of [A] (annotated by the red box) in relation to [B]?
(A) [option 1]
(B) [option 2]''',
'''Observing the image, what is the correct spatial positioning of [A] (annotated by the red box) in reference to [B]?
(A) [option 1]
(B) [option 2]''',
'''In this image, where is [A] (annotated by the red box) located relative to [B]?
(A) [option 1]
(B) [option 2]''',
'''Where is [A] (annotated by the red box) located in relation to [B] in the image?
(A) [option 1]
(B) [option 2]''',
]

image_above_below_visual_choice_question = [
'''From the image's perspective, considering the relative positions of [A] (annotated by the red box) and [B] in the image provided, where is [A] (annotated by the red box) located with respect to the staircase? Select from the following choices."
(A) [option 1]
(B) [option 2]''',
'''From the image's perspective, what is the correct spatial relationship of [A] (annotated by the red box) in relation to [B]? Select from the following
(A) [option 1]
(B) [option 2]''',
'''From the image's perspective, what is the correct spatial positioning of [A] (annotated by the red box) in reference to [B]? Select from the following
(A) [option 1]
(B) [option 2]''',
'''From the image's perspective, where is [A] (annotated by the red box) located relative to [B]? Select from the following
(A) [option 1]
(B) [option 2]''',
'''From the image's perspective, where is [A] (annotated by the red box) located in relation to [B] in the image? Select from the following
(A) [option 1]
(B) [option 2]''',
]

# --------------------------------------

obj_close_visual_choice = [
'''Which object is closer to the camera taking this photo, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]''',
'''Which point is closer to the camera, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]''',
'''Which object appears closest to the camera in this image, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]''',
'''Which of the following is the closest to the observer, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]''',
'''Among these objects, which one is nearest to the camera, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]'''
]

obj_far_visual_choice = [
'''Which object is further to the camera taking this photo, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]''',
'''Which point is further to the camera, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]''',
'''Which object appears farthest to the camera in this image, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]''',
'''Which of the following is the farthest to the observer, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]''',
'''Among these objects, which one is farthest to the camera, [A] (highlighted by a red box) or [B] (highlighted by a blue box)?
(A) [A]
(B) [B]'''
]

# obj_far_visual_choice_A = [
#     "(A)"
# ]

# obj_far_visual_choice_B = [
#     "(B)"
# ]

obj_close_anchor_visual_choice_question = [
'''Estimate the real-world distances between objects in this image. Which object is closer to [C] (highlighted by a red box), [A] (highlighted by a blue box) or [B] (highlighted by a green box)?
(A) [A]
(B) [B]''',
'''Which object is the closest to the [C] (highlighted by a red box)? Choose among these: [A] (highlighted by a blue box) or [B] (highlighted by a green box).
(A) [A]
(B) [B]''',
'''Which is nearer to the [C] (highlighted by a red box)? [A] (highlighted by a blue box) or [B] (highlighted by a green box).
(A) [A]
(B) [B]''',
'''Considering the real-world distances, which object is closest to [C] (highlighted by a red box)? [A] (highlighted by a blue box) or [B] (highlighted by a green box).
(A) [A]
(B) [B]''',
'''Which object is positioned closest to [C] (highlighted by a red box)? Select from [A] (highlighted by a blue box) and [B] (highlighted by a green box).
(A) [A]
(B) [B]''',
'''Based on their relative distances, which object is nearer to [C] (highlighted by a red box)? Choose from [A] (highlighted by a blue box) and [B] (highlighted by a green box).
(A) [A]
(B) [B]'''
]

obj_far_anchor_visual_choice_question = [
'''Estimate the real-world distances between objects in this image. Which object is farther from [C] (highlighted by a red box), [A] (highlighted by a blue box) or [B] (highlighted by a green box)?
(A) [A]
(B) [B]''',

'''Which object is the farthest from [C] (highlighted by a red box)? Choose among these: [A] (highlighted by a blue box) or [B] (highlighted by a green box).
(A) [A]
(B) [B]''',

'''Which is farther away from [C] (highlighted by a red box)? [A] (highlighted by a blue box) or [B] (highlighted by a green box)?
(A) [A]
(B) [B]''',

'''Considering the real-world distances, which object is farthest from [C] (highlighted by a red box)? [A] (highlighted by a blue box) or [B] (highlighted by a green box)?
(A) [A]
(B) [B]''',

'''Which object is positioned farthest from [C] (highlighted by a red box)? Select from [A] (highlighted by a blue box) and [B] (highlighted by a green box).
(A) [A]
(B) [B]''',

'''Based on their relative distances, which object is farther from [C] (highlighted by a red box)? Choose from [A] (highlighted by a blue box) and [B] (highlighted by a green box).
(A) [A]
(B) [B]'''
]

point_close_visual_choice_question = [
'''Two points are circled on the image, labeled by A and B beside each circle. Which point is closer to the camera?
Select from the following choices.
(A) A is closer
(B) B is closer''',
'''Two points are circled on the image, labeled by A and B beside each circle. Which point is closer to the camera taking this photo?
(A) A is closer
(B) B is closer''',
'''Two points are circled on the image, labeled by A and B beside each circle. Which point is closer to the camera?
(A) A is closer
(B) B is closer''',
'''Two points are circled on the image, labeled by A and B beside each circle. Which point appears closest to the camera in this image?
(A) A is closer
(B) B is closer''',
'''Two points are circled on the image, labeled by A and B beside each circle. Which of the following is the closest to the observer?
(A) A is closer
(B) B is closer''',
'''Two points are circled on the image, labeled by A and B beside each circle. Among these points, which one is nearest to the camera?
(A) A is closer
(B) B is closer''',
]
point_far_visual_choice_question = [
'''Two points are circled on the image, labeled by A and B beside each circle. Which point is further to the camera?
Select from the following choices.
(A) A is further
(B) B is further''',
'''Two points are circled on the image, labeled by A and B beside each circle. Which point is farther from the camera taking this photo?
(A) A is further
(B) B is further''',
'''Two points are circled on the image, labeled by A and B beside each circle. Which point is farther to the camera?
(A) A is further
(B) B is further''',
'''Two points are circled on the image, labeled by A and B beside each circle. Which point appears farthest from the camera in this image?
(A) A is further
(B) B is further''',
'''Two points are circled on the image, labeled by A and B beside each circle. Which of the following is the farthest from the observer?
(A) A is further
(B) B is further''',
'''Two points are circled on the image, labeled by A and B beside each circle. Among these points, which one is farthest from the camera?
(A) A is further
(B) B is further''',
]