import math                   # importing math library for nan assignment
from math import sqrt
import numpy as np            # importing numpy library for array usage

class SpeedProfile:           # class for calculating speed profile and referance speed profile
    def __init__(self, road_data, S):    # class initialisation with two arguments
        self.g = 9.81  # Acceleration due to gravity
        self.mu_max = 1 / 4  # Maximum value for the adhesion coefficient
        self.a_decel = -(1 / 8) * self.g  # Acceleration for a deceleration process
        self.a_accel = (1 / 10) * self.g  # Acceleration value for an acceleration process
        self.v_desired = (100 / 3.6) ** 2  # Square of the desired speed (= 100 km/h) in (m/s)^2
        self.s_decel_offset = -5  # Offset for braking processes, offset for the Generation of the setpoint profile from the maximum value profile
        self.s_accel_offset = 0  # Offset for acceleration processes, offset for generating the setpoint profile from the maximum value profile
        self.profile_number  = 0
        self.curves_indices = []
        self.road_data = road_data
        self.road_data_number = len(self.road_data)  # Determine the number of data records
        self.S = S              # indices genrated from track generation
        self.speed_profile = self.v_desired * np.ones((1, len(self.S)))    # 1D array creation for speed profile
        self.reference_value = self.v_desired * np.ones((1, len(self.S)))  # 1D array creation for referance speed profile

    # function for speed profiles calculation. Depending on the number of curves,
    # an individual speed profile is first calculated in this section for each of the curves
    def speed(self, decel_offset, accel_offset):
        tmp_s = np.zeros((6, self.profile_number))  # temporary variable
        tmp_vv = np.zeros((6, self.profile_number)) # temporary variable

        for count in range(self.profile_number ):
            if count > 0:
                x = self.road_data[self.curves_indices[count - 1]]['adjust_speed'] >= self.road_data[self.curves_indices[count]]['adjust_speed']
                y = self.road_data[self.curves_indices[count - 1]]['adjust_speed'] < self.road_data[self.curves_indices[count]]['adjust_speed']
                z = (2 * self.a_accel * (self.road_data[self.curves_indices[count]]['sbegin_no_acc'] - self.road_data[self.curves_indices[count - 1]]['send_no_acc']) +
                     self.road_data[self.curves_indices[count - 1]]['adjust_speed']) > self.road_data[self.curves_indices[count]]['adjust_speed']
            else:             # setting false condition for first indice of list
                x = False
                y = False
                z = False

            if (count == 0) or (count > 0 and x) or (count > 0 and y and z):
                tmp_s[0, count] = (self.road_data[self.curves_indices[count]]['sbegin_no_br'] + (self.v_desired - self.road_data[self.curves_indices[count]]['adjust_speed']) /
                                   (2 * self.a_decel) + decel_offset - 200)
                tmp_vv[0, count] = self.v_desired
                tmp_s[1, count] = (self.road_data[self.curves_indices[count]]['sbegin_no_br'] + (self.v_desired - self.road_data[self.curves_indices[count]]['adjust_speed']) /
                                   (2 * self.a_decel) + decel_offset)
                tmp_vv[1, count] = self.v_desired
                tmp_s[2, count] = self.road_data[self.curves_indices[count]]['sbegin_no_br'] + decel_offset
                tmp_vv[2, count] = self.road_data[self.curves_indices[count]]['adjust_speed']
            else:
                tmp_s[0, count] = self.road_data[self.curves_indices[count]]['sbegin_no_acc'] + (self.v_desired - self.road_data[self.curves_indices[count]]['adjust_speed']) / (
                                              2 * self.a_decel) + decel_offset - 200
                tmp_vv[0, count] = self.v_desired
                tmp_s[1, count] = (self.road_data[self.curves_indices[count]]['sbegin_no_acc'] + (self.v_desired - self.road_data[self.curves_indices[count]]['adjust_speed']) /
                                (2 * self.a_decel) + decel_offset)
                tmp_vv[1, count] = self.v_desired
                tmp_s[2, count] = self.road_data[self.curves_indices[count]]['sbegin_no_acc'] + decel_offset
                tmp_vv[2, count] = self.road_data[self.curves_indices[count]]['adjust_speed']

            if count < self.profile_number  - 1:
                a = self.road_data[self.curves_indices[count + 1]]['adjust_speed'] >= self.road_data[self.curves_indices[count]]['adjust_speed']
                b = self.road_data[self.curves_indices[count + 1]]['adjust_speed'] < self.road_data[self.curves_indices[count]]['adjust_speed']
                c = (2 * self.a_accel * (self.road_data[self.curves_indices[count]]['send_no_br'] - self.road_data[self.curves_indices[count + 1]]['sbegin_no_br']) +
                     self.road_data[self.curves_indices[count + 1]]['adjust_speed']) > self.road_data[self.curves_indices[count]]['adjust_speed']
            else:           # setting false condition for last indice of list
                a = False
                b = False
                c = False

            if (count == self.profile_number  - 1) or (count < (self.profile_number  - 1) and a) or (count < (self.profile_number  - 1) and b and c):
                tmp_s[3, count] = self.road_data[self.curves_indices[count]]['send_no_acc'] + accel_offset
                tmp_vv[3, count] = self.road_data[self.curves_indices[count]]['adjust_speed']
                tmp_s[4, count] = (self.road_data[self.curves_indices[count]]['send_no_acc'] + (self.v_desired - self.road_data[self.curves_indices[count]]['adjust_speed']) /
                                   (2 * self.a_accel) + accel_offset)
                tmp_vv[4, count] = self.v_desired
                tmp_s[5, count] = (self.road_data[self.curves_indices[count]]['send_no_acc'] + (self.v_desired - self.road_data[self.curves_indices[count]]['adjust_speed']) /
                                   (2 * self.a_accel) + accel_offset + 200)
                tmp_vv[5, count] = self.v_desired
            else:
                tmp_s[3, count] = self.road_data[self.curves_indices[count]]['send_no_br'] + accel_offset
                tmp_vv[3, count] = self.road_data[self.curves_indices[count]]['adjust_speed']
                tmp_s[4, count] = (self.road_data[self.curves_indices[count]]['send_no_br'] + ( self.v_desired - self.road_data[self.curves_indices[count]]['adjust_speed']) /
                                   (2 * self.a_accel) + accel_offset)
                tmp_vv[4, count] = self.v_desired
                tmp_s[5, count] = (self.road_data[self.curves_indices[count]]['send_no_br'] + (self.v_desired - self.road_data[self.curves_indices[count]]['adjust_speed']) /
                                   (2 * self.a_accel) + accel_offset + 200)
                tmp_vv[5, count] = self.v_desired

        return tmp_s, tmp_vv   # return of temorary variables

    def generate_speedprofile(self):

        ##################################################################################################
        # Calculation of the end points of the braking distances,the starting points of the accelerations
        # No checking of mutual influence!
        ##################################################################################################
        for count in range(self.road_data_number):  # Find number of curves, determine transition sections
            if self.road_data[count]['typ'] == 'CircularArc':  # A speed profile is created for each curve
                self.curves_indices.append(count)
                self.profile_number  += 1
                self.road_data[count]['vv_max'] = self.mu_max * self.g * abs(self.road_data[count]['R'])  # Square of the maximum speed in the curve.No longitudinal acceleration
                self.road_data[count]['adjust_speed'] = self.road_data[count]['vv_max']  # At this point we do not yet know whether we need to reduce the speed in this curve,
                # so the reduced speed is set equal to the maximum speed.
                self.road_data[count]['previous_curve'] = 0
                self.road_data[count]['next_curve'] = 0  # Mark mutual influence as not checked

                if count > 0:  # Calculate the waypoint from which braking is no longer permitted
                    if self.road_data[count-1]['typ'] == 'Clothoid':  # Previous part of the curve is a clothoid
                        # Correct the end point of the braking distance if necessary
                        self.road_data[count]['sbegin_no_acc'] = (self.road_data[count - 1]['sbegin'] + (self.road_data[count - 1]['send'] - self.road_data[count - 1]['sbegin']) *
                                                             abs(self.road_data[count]['R']) * sqrt(self.mu_max ** 2 * self.g ** 2 - self.a_accel ** 2) / self.road_data[count]['vv_max'])

                        if self.road_data[count]['sbegin_no_acc'] > self.road_data[count]['sbegin']:
                            self.road_data[count]['sbegin_no_acc'] = self.road_data[count]['sbegin']

                        # Correct the end point of the braking distance if necessary
                        self.road_data[count]['sbegin_no_br'] = (self.road_data[count - 1]['sbegin'] + (self.road_data[count - 1]['send'] - self.road_data[count - 1]['sbegin']) *
                                                            abs(self.road_data[count]['R']) * sqrt(self.mu_max ** 2 * self.g ** 2 - self.a_decel ** 2) / self.road_data[count]['vv_max'])

                        if self.road_data[count]['sbegin_no_br'] > self.road_data[count]['sbegin']:
                            self.road_data[count]['sbegin_no_br'] = self.road_data[count]['sbegin']

                        # Calculate the location of the maximum acceleration
                        s_max = 0.5 * self.road_data[count - 1]['sbegin'] + 0.5 * self.road_data[count]['sbegin_no_br'] - self.road_data[count]['vv_max'] / (4 * self.a_decel)

                        if self.road_data[count - 1]['sbegin'] <= s_max <= self.road_data[count]['sbegin_no_br']:
                            # If the acceleration maximum is in the braking interval, calculate the acceleration maximum
                            mu_res_max = self.g * sqrt(self.a_decel ** 2 + ((2 * self.a_decel * s_max - 2 * self.a_decel * self.road_data[count]['sbegin_no_br'] + self.road_data[count]['vv_max']) ** 2 *
                                        (s_max - self.road_data[count - 1]['sbegin']) ** 2) / ((self.road_data[count - 1]['send'] - self.road_data[count - 1]['sbegin']) * abs(self.road_data[count]['R'])) ** 2)

                            if mu_res_max > self.mu_max:
                                self.road_data[count]['sbegin_no_br'] = self.road_data[count - 1]['sbegin'] + self.road_data[count]['vv_max'] / (2 * self.a_decel) + sqrt(-2 * sqrt(self.mu_max ** 2 * self.g ** 2 - self.a_decel ** 2) /
                                                                       self.a_decel * (self.road_data[count - 1]['send'] -self.road_data[count - 1]['sbegin']) * abs(self.road_data[count]['R']))

                            if (self.road_data[count]['sbegin_no_br'] < self.road_data[count - 1]['sbegin']) or (self.road_data[count]['sbegin_no_br'] > self.road_data[count - 1]['send']):
                                print('The calculation of the end point of the braking distance before the following curve has gone wrong:')
                                print(self.profile_number)

                    elif self.road_data[count - 1]['typ'] == 'Straight line' or self.road_data[count - 1]['typ'] == 'CircularArc':
                        self.road_data[count]['sbegin_no_br'] = self.road_data[count]['sbegin']
                        self.road_data[count]['sbegin_no_acc'] = self.road_data[count]['sbegin']

                    else:
                        print('Road geometry not taken into account before curve:')
                        print(self.profile_number)
                        self.road_data[count]['sbegin_no_br'] = math.nan
                        self.road_data[count]['sbegin_no_acc'] = math.nan

                else:
                    print('Error: sbegin_no_br cannot be determined for the following curve:')
                    print(self.profile_number)
                    self.road_data[count]['sbegin_no_br'] = math.nan
                    self.road_data[count]['sbegin_no_acc'] = math.nan

                if count < self.road_data_number - 1:  # Calculate waypoints from which acceleration/braking is permitted again.
                    if self.road_data[count + 1]['typ'] == 'Clothoid':
                        self.road_data[count]['send_no_br'] = (self.road_data[count + 1]['send'] + (self.road_data[count + 1]['sbegin'] - self.road_data[count + 1]['send']) *
                                                             abs(self.road_data[count]['R']) * sqrt(self.mu_max ** 2 * self.g ** 2 - self.a_decel ** 2) / self.road_data[count]['vv_max'])

                        # Correct the starting point of the braking distance if necessary
                        if self.road_data[count]['send_no_br'] < self.road_data[count]['send']:
                            self.road_data[count]['send_no_br'] = self.road_data[count]['send']

                        self.road_data[count]['send_no_acc'] = (self.road_data[count + 1]['send'] + (self.road_data[count + 1]['sbegin'] - self.road_data[count + 1]['send']) *
                                                              abs(self.road_data[count]['R']) * sqrt(self.mu_max ** 2 * self.g ** 2 - self.a_accel ** 2) / self.road_data[count]['vv_max'])

                        # Correct the end point of the braking distance if necessary
                        if self.road_data[count]['send_no_acc'] < self.road_data[count]['send']:
                            self.road_data[count]['send_no_acc'] = self.road_data[count]['send']

                        #  Calculate the location of maximum acceleration
                        s_max = 0.5 * self.road_data[count + 1]['send'] + 0.5 * self.road_data[count]['send_no_acc'] - self.road_data[count]['vv_max'] / (4 * self.a_accel)

                        if (s_max >= self.road_data[count]['send_no_acc']) and (s_max <= self.road_data[count + 1]['send']):
                            # If the acceleration maximum lies in the acceleration interval, calculate the acceleration maximum
                            mu_res_max = self.g * sqrt(self.a_accel ** 2 + ((2 * self.a_accel * s_max - 2 * self.a_accel * self.road_data[count]['send_no_acc'] + self.road_data[count]['vv_max']) ** 2 *
                                        (self.road_data[count + 1]['send'] - s_max) ** 2) / ((self.road_data[count + 1]['send'] - self.road_data[count + 1]['sbegin']) * abs(self.road_data[count]['R'])) ** 2)

                            if mu_res_max > self.mu_max:
                                # if the acceleration maximum is too high, recalculate the starting point of the acceleration process
                                self.road_data[count]['send_no_acc'] = self.road_data[count + 1]['send'] + self.road_data[count]['vv_max'] / (2 * self.a_accel) - sqrt(2 * sqrt(self.mu_max ** 2 * self.g ** 2 - self.a_accel ** 2) /
                                                                      self.a_accel * (self.road_data[count + 1]['send'] - self.road_data[count + 1]['sbegin']) * abs(self.road_data[count]['R']))

                                if (self.road_data[count]['send_no_acc'] < self.road_data[count + 1]['sbegin']) or (self.road_data[count]['send_no_acc'] > self.road_data[count + 1]['send']):
                                    print('The calculation of the starting point for the acceleration process after the following curve has gone wrong:')
                                    print(self.profile_number)

                    elif self.road_data[count + 1]['typ'] == 'Straight line' or self.road_data[count + 1]['typ'] == 'CircularArc':
                        self.road_data[count]['send_no_br'] = self.road_data[count]['send']
                        self.road_data[count]['send_no_acc'] = self.road_data[count]['send']

                    else:
                        print('Road geometry behind bend not taken into account:')
                        print(self.profile_number)
                        self.road_data[count]['sbegin_no_br'] = math.nan
                        self.road_data[count]['sbegin_no_acc'] = math.nan

                else:
                    print('Error: send_no_br/send_no_acc cannot be determined for the following curve:')
                    print(self.profile_number)
                    self.road_data[count]['sbegin_no_br'] = math.nan
                    self.road_data[count]['sbegin_no_acc'] = math.nan

        ##################################################################################################
        #  Sorting of the curve indices depending on the maximum speed and checking the mutual influence
        #  Procedure: 1. The curves are sorted according to the assigned speed.
        #             2. The curve that has not yet been considered and in which the lowest speed is driven,
        #                 is processed next.
        #             3. Checked whether the speed in the preceding or the following curve must be reduced
        ###################################################################################################
        if self.profile_number  >= 1:
            for count in range(self.profile_number):
                tmp_pre_sort = np.zeros((3, self.profile_number))
                # Sorting the curves based on the speeds assigned to them
                for tmp_count in range(self.profile_number):
                    tmp_pre_sort[0, tmp_count] = tmp_count  # Consecutive number
                    tmp_pre_sort[1, tmp_count] = self.curves_indices[tmp_count]
                    tmp_pre_sort[2, tmp_count] = self.road_data[self.curves_indices[tmp_count]]['adjust_speed']

                tmp_sort = np.zeros((3, self.profile_number))
                for tmp_count in range(self.profile_number):
                    tmp_index = np.argmin(tmp_pre_sort[2])
                    tmp_sort[0, tmp_count] = tmp_pre_sort[0, tmp_index]
                    tmp_sort[1, tmp_count] = tmp_pre_sort[1, tmp_index]
                    tmp_sort[2, tmp_count] = tmp_pre_sort[2, tmp_index]
                    tmp_pre_sort[2, tmp_index] = np.inf

                sort_curves_indices = np.zeros((2, self.profile_number), dtype=int)
                sort_curves_indices[0, :] = tmp_sort[0, :].astype(int)
                sort_curves_indices[1, :] = tmp_sort[1, :].astype(int)

                if self.road_data[sort_curves_indices[1, count]]['previous_curve'] == 0:
                    if sort_curves_indices[0, count] > 0:
                        if self.road_data[self.curves_indices[sort_curves_indices[0, count] - 1]]['adjust_speed'] > self.road_data[sort_curves_indices[1, count]]['adjust_speed']:
                            vv_before = 2 * self.a_decel * (self.road_data[self.curves_indices[sort_curves_indices[0, count] - 1]]['send_no_br'] -
                                        self.road_data[sort_curves_indices[1, count]]['sbegin_no_br']) + self.road_data[sort_curves_indices[1, count]]['adjust_speed']

                            if self.road_data[self.curves_indices[sort_curves_indices[0, count] - 1]]['adjust_speed'] > vv_before:
                                self.road_data[self.curves_indices[sort_curves_indices[0, count] - 1]]['adjust_speed'] = vv_before

                            self.road_data[sort_curves_indices[1, count]]['previous_curve'] = 1
                            self.road_data[self.curves_indices[sort_curves_indices[0, count] - 1]]['next_curve'] = 1

                        else:
                            print('The speed in the previous curve is lower than in the curve just considered.')
                            print('This case should not occur!')

                    else:
                        self.road_data[sort_curves_indices[1, count]]['previous_curve'] = 1

                if self.road_data[sort_curves_indices[1, count]]['next_curve'] == 0:
                    if sort_curves_indices[0, count] < self.profile_number  - 1:
                        if self.road_data[self.curves_indices[sort_curves_indices[0, count] + 1]]['adjust_speed'] > self.road_data[sort_curves_indices[1, count]]['adjust_speed']:
                            vv_following = (2 * self.a_accel * (self.road_data[self.curves_indices[sort_curves_indices[0, count] + 1]]['sbegin_no_acc'] - self.road_data[sort_curves_indices[1, count]]['send_no_acc']) +
                                            self.road_data[sort_curves_indices[1, count]]['adjust_speed'])

                            if self.road_data[self.curves_indices[sort_curves_indices[0, count] + 1]]['adjust_speed'] > vv_following:
                                self.road_data[self.curves_indices[sort_curves_indices[0, count] + 1]]['adjust_speed'] = vv_following

                            self.road_data[sort_curves_indices[1, count]]['next_curve'] = 1
                            self.road_data[self.curves_indices[sort_curves_indices[0, count] + 1]]['previous_curve'] = 1

                        else:
                            print('The speed in the following curve is lower than in the curve just considered.')
                            print('This case should not occur!')

                    else:
                        self.road_data[sort_curves_indices[1, count]]['next_curve'] = 1

        ########################################################################################################
        # Creating a valid velocity profile
        # From the individual profiles calculated, an overall profile is calculated in this program
        # section is used to calculate an overall profile.
        #########################################################################################################
        tmp_s, tmp_vv = self.speed(0, 0)

        for count in range(self.profile_number):
            for count_s in range(len(self.S)):
                vv = np.interp(count_s, tmp_s[:, count], tmp_vv[:, count])
                if self.speed_profile[0, count_s] > vv:
                    self.speed_profile[0, count_s] = vv

        self.speed_profile = np.sqrt(self.speed_profile)

        ########################################################################################################
        # Creating a valid referance velocity profile
        # From the individual profiles calculated, an overall profile is calculated in this program
        # section is used to calculate an overall profile.
        #########################################################################################################
        tmp_s_ref, tmp_v_ref = self.speed(self.s_decel_offset, self.s_accel_offset)

        for count in range(self.profile_number):
            for count_s in range(len(self.S)):
                vv_ref = np.interp(count_s, tmp_s_ref[:, count], tmp_v_ref[:, count])
                if self.reference_value[0, count_s] > vv_ref:
                    self.reference_value[0, count_s] = vv_ref

        self.reference_value = np.sqrt(self.reference_value)






