def do_rectangles_overlap(rect1, rect2):
    x1_r1, y1_r1, x2_r1, y2_r1 = rect1
    x1_r2, y1_r2, x2_r2, y2_r2 = rect2
    
    if x2_r1 <= x1_r2 or x2_r2 <= x1_r1:
        return False
    
    if y2_r1 <= y1_r2 or y2_r2 <= y1_r1:
        return False
    
    return True


def make_mergeable_set(boxes):
    overlap_tracker = dict()
    mergeable_boxes = []

    for root_bx_idx in range(len(boxes)):
        overlap_tracker[root_bx_idx] = {root_bx_idx}
        for sub_bx_idx in range(len(boxes)):
            if root_bx_idx != sub_bx_idx:
                if do_rectangles_overlap(boxes[root_bx_idx], boxes[sub_bx_idx]):
                    overlap_tracker[root_bx_idx].add(sub_bx_idx)


    for key in list(overlap_tracker.keys()):
        overlap_set = overlap_tracker.get(key, None)
        if overlap_set != None: #If the overlap_set for key doesn't exists, don't need to continue. Because, the box was already overlaps with some other box.
            merged_bx_set = set(overlap_set)
            
            for bx_idx in overlap_set:
                sub_bx_set = overlap_tracker.get(bx_idx, None)
                if sub_bx_set!= None: #If the box idx was deleted, i.e. already merged to other box, do not add this anymore.
                    merged_bx_set.update(sub_bx_set)
                    del overlap_tracker[bx_idx]

            mergeable_boxes.append(merged_bx_set)

    return mergeable_boxes

"""
    Merge the boxes now.
    TODO:
        1. For each merging_set, get coords of all the available boxes.
            
            x1 ⬇️       x2 ⬆️
            y1 ⬇️       y2 ⬆️
            
"""
def merge_from_set(mergeable_boxes_set, boxes):
    merged_boxes = []
    for m_set in mergeable_boxes_set:
        mrgd_x1, mrgd_y1, mrgd_x2, mrgd_y2 = -1, -1, -1, -1
        for bx_ix in m_set:
            x1, y1, x2, y2 = boxes[bx_ix]

            # if this is the first element we have picked from the set, make the merged boxes x1, y2, x2, y2 to the first element's x2,
            if mrgd_x1 == -1 or mrgd_y1 == -1 or mrgd_x2 == -1 or mrgd_y2 == -1:
                mrgd_x1, mrgd_y1, mrgd_x2, mrgd_y2 = x1, y1, x2, y2
                
            mrgd_x1 = x1 if x1 < mrgd_x1 else mrgd_x1 # make merged_x1 to x1 if x1 is less than mrgd_x1. Else leave it as it s
            mrgd_y1 = y1 if y1 < mrgd_y1 else mrgd_y1 # make merged_x1 to x1 if x1 is less than mrgd_x1. Else leave it as it s
            mrgd_x2 = x2 if x2 > mrgd_x2 else mrgd_x2 # make merged_x1 to x1 if x1 is less than mrgd_x1. Else leave it as it s
            mrgd_y2 = y2 if y2 > mrgd_y2 else mrgd_y2 # make merged_x1 to x1 if x1 is less than mrgd_x1. Else leave it as it s

        merged_box = (mrgd_x1, mrgd_y1, mrgd_x2, mrgd_y2)
        merged_boxes.append(merged_box)

    return merged_boxes