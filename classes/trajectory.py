class Trajectory(object):
    def __init__(self, vehicle_id, time_list=None, epoch_list=None, local_x_list=None, local_y_list=None,
                 global_x_list=None, global_y_list=None, vehicle_length=None, vehicle_width=None,
                 vehicle_class=None, velocity_list=None, acc_list=None, origin_zone=None, destination_zone=None,
                 intersection_list=None, section_list=None, direction_list=None, movement_list=None,
                 preceding_list=None, following_list=None, space_headway_list=None, lane_list=None):
        self.vehicle_id = vehicle_id
        if time_list is None:
            self.time_list = []
        else:
            self.time_list = time_list
        if epoch_list is None:
            self.epoch_list = []
        else:
            self.epoch_list = epoch_list
        if local_x_list is None:
            self.local_x_list = []
        else:
            self.local_x_list = local_x_list
        if local_y_list is None:
            self.local_y_list = []
        else:
            self.local_y_list = local_y_list
        if global_x_list is None:
            self.global_x_list = []
        else:
            self.global_x_list = global_x_list
        if global_y_list is None:
            self.global_y_list = []
        else:
            self.global_y_list = global_y_list
        self.vehicle_length = vehicle_length
        self.vehicle_width = vehicle_width
        self.vehicle_class = vehicle_class
        if velocity_list is None:
            self.velocity_list = []
        else:
            self.velocity_list = velocity_list
        if acc_list is None:
            self.acc_list = []
        else:
            self.acc_list = acc_list
        self.origin_zone = origin_zone
        self.destination_zone = destination_zone
        if intersection_list is None:
            self.intersection_list = []
        else:
            self.intersection_list = intersection_list
        if section_list is None:
            self.section_list = []
        else:
            self.section_list = section_list
        if direction_list is None:
            self.direction_list = []
        else:
            self.direction_list = direction_list
        if movement_list is None:
            self.movement_list = []
        else:
            self.movement_list = movement_list
        if preceding_list is None:
            self.preceding_list = []
        else:
            self.preceding_list = preceding_list
        if following_list is None:
            self.following_list = []
        else:
            self.following_list = following_list
        if space_headway_list is None:
            self.space_headway_list = []
        else:
            self.space_headway_list = space_headway_list
        if lane_list is None:
            self.lane_list = []
        else:
            self.lane_list = lane_list

