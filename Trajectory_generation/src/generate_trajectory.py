from math import pi, cos, sin, sqrt, factorial          # importing math functions for operations in functions

class PathGenerate:                    # defining class to generate trajectory

    def __init__(self,X_start,Y_start,phi_s,lanewidth,lanes):          # Initialisation of class variables
        self.Number_of_lanes = lanes
        self.S = []                    # list if indices
        self.curvature = []            # list of curvature at circular and clothloid path
        self.road_data = {}            # dictionary to store data of track
        self.lanewidth = lanewidth
        self.lanewidth_half = self.lanewidth/2    # width of single track
        self.X_start = X_start
        self.Y_start = Y_start
        self.phi_s = phi_s
        self.indexcount = 0
        self.road_data_indexcount = 0
        self.lanenumber = 0
        self.lanes = {}
        for i in range(self.Number_of_lanes):
            self.lanes[i] = {'X_center': [], 'Y_center': [], 'X_left': [], 'Y_left': [], 'X_right': [], 'Y_right': []}

    def clothoid(self, alpha, a):        # user defined function to calculate X,Y coordinates in clothoid type track
        sum_x = 0
        sum_y = 0

        for count in range(41):
            sum_x += ((-1) ** count * alpha ** (2 * count)) / ((4 * count + 1) * factorial(2 * count))
            sum_y += ((-1) ** count * alpha ** (2 * count + 1)) / ((4 * count + 3) * factorial(2 * count + 1))

        x = a * sqrt(2 * alpha) * sum_x
        y = a * sqrt(2 * alpha) * sum_y

        result = [x, y]
        return result                     # returning X Y coordinates


    def range_float(self, start, stop, step):      # user defined function used in for loop with float data type
        z = start
        if step > 0:
            while z <= stop:
                yield z
                z += step
        elif step < 0:
            while z >= stop:
                yield z
                z += step

    # user defined function for X Y coordinate calculation in staright line type track
    def straight_line(self, l, X_start, Y_start, phi_s):
        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'Straight line'
        self.road_data[self.road_data_indexcount]['curvaturebegin'] = 0
        self.road_data[self.road_data_indexcount]['sbegin'] = 0

        for i in range(l + 1):                      # loop to calculate X,Y iteratively till length(l)
            self.S.append(self.indexcount)
            self.curvature.append(0)
            self.lanes[0]['X_center'].append(X_start + i * cos(phi_s))
            self.lanes[0]['Y_center'].append(Y_start + i * sin(phi_s))
            self.lanes[0]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s + pi / 2))
            self.lanes[0]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s + pi / 2))
            self.lanes[0]['X_right'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s - pi / 2))
            self.lanes[0]['Y_right'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s - pi / 2))
            for j in range(1, self.Number_of_lanes):
                self.lanes[j]['X_right'] = self.lanes[j-1]['X_left']
                self.lanes[j]['Y_right'] = self.lanes[j-1]['Y_left']
                self.lanes[j]['X_center'].append(self.lanes[0]['X_center'][self.indexcount] + (j * self.lanewidth) * cos(phi_s + pi / 2))
                self.lanes[j]['Y_center'].append(self.lanes[0]['Y_center'][self.indexcount] + (j * self.lanewidth) * sin(phi_s + pi / 2))
                self.lanes[j]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + (j * self.lanewidth + self.lanewidth_half) * cos(phi_s + pi / 2))
                self.lanes[j]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + (j * self.lanewidth + self.lanewidth_half) * sin(phi_s + pi / 2))
            self.indexcount += 1

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['curvatureend'] = 0
        self.road_data_indexcount += 1

        phi_e = phi_s
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e

    # user defined function for X,Y coordinate calculation in anticlock direction circular arc type track
    def circular_arc_anticlock(self, l, R, X_start, Y_start, phi_s):
        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'CircularArc'
        self.road_data[self.road_data_indexcount]['sbegin'] = self.indexcount
        self.road_data[self.road_data_indexcount]['curvaturebegin'] = 1 / R

        # Center of the arc calculation
        Mx = X_start + R * cos(phi_s + pi / 2)
        My = Y_start + R * sin(phi_s + pi / 2)

        for i in self.range_float(phi_s - pi / 2 + 1 / R, ((phi_s - pi / 2) + l / R), 1 / R):
            self.S.append(self.indexcount)
            self.curvature.append(1 / R)
            self.lanes[0]['X_center'].append(Mx + R * cos(i))
            self.lanes[0]['Y_center'].append(My + R * sin(i))
            self.lanes[0]['X_left'].append(Mx + (R - self.lanewidth_half) * cos(i))
            self.lanes[0]['Y_left'].append(My + (R - self.lanewidth_half) * sin(i))
            self.lanes[0]['X_right'].append(Mx + (R + self.lanewidth_half) * cos(i))
            self.lanes[0]['Y_right'].append(My + (R + self.lanewidth_half) * sin(i))
            for j in range(1, self.Number_of_lanes):
                self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']
                self.lanes[j]['X_center'].append(Mx + (R - (j * self.lanewidth)) * cos(i))
                self.lanes[j]['Y_center'].append(My + (R - (j * self.lanewidth)) * sin(i))
                self.lanes[j]['X_left'].append(Mx + (R - (j*self.lanewidth + self.lanewidth_half)) * cos(i))
                self.lanes[j]['Y_left'].append(My + (R - (j*self.lanewidth + self.lanewidth_half)) * sin(i))
            self.indexcount += 1

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['curvatureend'] = 1 / R
        self.road_data[self.road_data_indexcount]['R'] = R
        self.road_data_indexcount += 1

        phi_e = phi_s + l / R
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e

    # user defined function for X,Y coordinate calculation in clock direction circular arc type track
    def circular_arc_clock(self, l, R, X_start, Y_start, phi_s):
        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'CircularArc'
        self.road_data[self.road_data_indexcount]['sbegin'] = self.indexcount
        self.road_data[self.road_data_indexcount]['curvaturebegin'] = -1 / R

        Mx = X_start + R * cos(phi_s - pi / 2)
        My = Y_start + R * sin(phi_s - pi / 2)

        for i in self.range_float(phi_s + pi / 2 - 1 / R, phi_s + pi / 2 - 1 / R - (l - 1) / R, -1 / R):
            self.S.append(self.indexcount)
            self.curvature.append(-1 / R)
            self.lanes[0]['X_center'].append(Mx + R * cos(i))
            self.lanes[0]['Y_center'].append(My + R * sin(i))
            self.lanes[0]['X_left'].append(Mx + (R + self.lanewidth_half) * cos(i))
            self.lanes[0]['Y_left'].append(My + (R + self.lanewidth_half) * sin(i))
            self.lanes[0]['X_right'].append(Mx + (R - self.lanewidth_half) * cos(i))
            self.lanes[0]['Y_right'].append(My + (R - self.lanewidth_half) * sin(i))
            for j in range(1, self.Number_of_lanes):
                self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']
                self.lanes[j]['X_center'].append(Mx + (R + (j * self.lanewidth)) * cos(i))
                self.lanes[j]['Y_center'].append(My + (R + (j * self.lanewidth)) * sin(i))
                self.lanes[j]['X_left'].append(Mx + (R + (j*self.lanewidth + self.lanewidth_half)) * cos(i))
                self.lanes[j]['Y_left'].append(My + (R + (j*self.lanewidth + self.lanewidth_half)) * sin(i))
            self.indexcount += 1

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['curvatureend'] = -1 / R
        self.road_data[self.road_data_indexcount]['R'] = -R
        self.road_data_indexcount += 1

        phi_e = phi_s - l / R
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e

    # user defined function for X,Y coordinate calculation in anticlock direction clothoid arc connecting from line to circle type track
    def clothoid_arc_lin_cir_anticlock(self, l, R, X_start, Y_start, phi_s):
        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'Clothoid'
        self.road_data[self.road_data_indexcount]['curvaturebegin'] = 0
        self.road_data[self.road_data_indexcount]['sbegin'] = self.indexcount

        A = sqrt(l * R)
        phi = (l ** 2) / (2 * (A ** 2))

        X_start_clothoide = X_start
        Y_start_clothoide = Y_start

        for i in range(1, l + 1):
            self.S.append(self.indexcount)
            self.curvature.append(i / (A ** 2))
            xy = self.clothoid((i ** 2) / (2 * (A ** 2)), A)
            self.lanes[0]['X_center'].append(X_start_clothoide + xy[0] * cos(phi_s) - xy[1] * sin(phi_s))
            self.lanes[0]['Y_center'].append(Y_start_clothoide + xy[0] * sin(phi_s) + xy[1] * cos(phi_s))
            self.lanes[0]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s + i ** 2 / (2 * A ** 2) + pi / 2))
            self.lanes[0]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s + i ** 2 / (2 * A ** 2) + pi / 2))
            self.lanes[0]['X_right'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s + i ** 2 / (2 * A ** 2) - pi / 2))
            self.lanes[0]['Y_right'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s + i ** 2 / (2 * A ** 2) - pi / 2))
            for j in range(1, self.Number_of_lanes):
                self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']
                self.lanes[j]['X_center'].append(self.lanes[0]['X_center'][self.indexcount] + (j * self.lanewidth) * cos(phi_s + i ** 2 / (2 * A ** 2) + pi / 2))
                self.lanes[j]['Y_center'].append(self.lanes[0]['Y_center'][self.indexcount] + (j * self.lanewidth) * sin(phi_s + i ** 2 / (2 * A ** 2) + pi / 2))
                self.lanes[j]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + (self.lanewidth_half + j*self.lanewidth) * cos(phi_s + i ** 2 / (2 * A ** 2) + pi / 2))
                self.lanes[j]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + (self.lanewidth_half + j*self.lanewidth) * sin(phi_s + i ** 2 / (2 * A ** 2) + pi / 2))
            self.indexcount += 1

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['curvatureend'] = 1 / R
        self.road_data[self.road_data_indexcount]['A'] = A
        self.road_data_indexcount += 1

        phi_e = phi_s + phi
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e

    # user defined function for X,Y coordinate calculation in anticlock direction clothoid arc connecting from circle to line type track
    def clothoid_arc_cir_lin_anticlock(self, l, R, X_start, Y_start, phi_s):
        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'Clothoid'
        self.road_data[self.road_data_indexcount]['sbegin'] = self.indexcount
        self.road_data[self.road_data_indexcount]['curvaturebegin'] = 1 / R

        A = sqrt(l * R)
        phi = (l ** 2) / (2 * (A ** 2))

        xy = self.clothoid((l ** 2) / (2 * (A ** 2)), A)
        clothoide_size_X = xy[0]
        clothoide_size_Y = xy[1]

        X_start_clothoide = X_start + clothoide_size_X * cos(phi_s + phi) + clothoide_size_Y * sin(phi_s + phi)
        Y_start_clothoide = Y_start + clothoide_size_X * sin(phi_s + phi) - clothoide_size_Y * cos(phi_s + phi)

        for i in range(l - 1, -1, -1):
            self.S.append(self.indexcount)
            self.curvature.append(i / (A ** 2))
            xy = self.clothoid((i ** 2) / (2 * (A ** 2)), A)
            self.lanes[0]['X_center'].append(X_start_clothoide + xy[0] * cos(phi_s + phi - pi) + xy[1] * sin(phi_s + phi - pi))
            self.lanes[0]['Y_center'].append(Y_start_clothoide + xy[0] * sin(phi_s + phi - pi) - xy[1] * cos(phi_s + phi - pi))
            self.lanes[0]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s + phi - pi - i ** 2 / (2 * A ** 2) - pi / 2))
            self.lanes[0]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s + phi - pi - i ** 2 / (2 * A ** 2) - pi / 2))
            self.lanes[0]['X_right'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s + phi - pi - i ** 2 / (2 * A ** 2) + pi / 2))
            self.lanes[0]['Y_right'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s + phi - pi - i ** 2 / (2 * A ** 2) + pi / 2))
            for j in range(1, self.Number_of_lanes):
                self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']
                self.lanes[j]['X_center'].append(self.lanes[0]['X_center'][self.indexcount] + (j * self.lanewidth) * cos(phi_s + phi - pi - i ** 2 / (2 * A ** 2) - pi / 2))
                self.lanes[j]['Y_center'].append(self.lanes[0]['Y_center'][self.indexcount] + (j * self.lanewidth) * sin(phi_s + phi - pi - i ** 2 / (2 * A ** 2) - pi / 2))
                self.lanes[j]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + (self.lanewidth_half + j*self.lanewidth) * cos(phi_s + phi - pi - i ** 2 / (2 * A ** 2) - pi / 2))
                self.lanes[j]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + (self.lanewidth_half + j*self.lanewidth) * sin(phi_s + phi - pi - i ** 2 / (2 * A ** 2) - pi / 2))
            self.indexcount += 1

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['curvatureend'] = 0
        self.road_data[self.road_data_indexcount]['A'] = A
        self.road_data_indexcount += 1

        phi_e = phi_s + phi
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e

    # user defined function for X,Y coordinate calculation in clock direction clothoid arc connecting from line to circle type track
    def clothoid_arc_lin_cir_clock(self, l, R, X_start, Y_start, phi_s):
        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'Clothoid'
        self.road_data[self.road_data_indexcount]['sbegin'] = self.indexcount
        self.road_data[self.road_data_indexcount]['curvaturebegin'] = 0

        A = sqrt(l * R)
        phi = l ** 2 / (2 * (A ** 2))

        X_start_clothoide = X_start
        Y_start_clothoide = Y_start

        for i in range(1, l + 1):
            self.S.append(self.indexcount)
            self.curvature.append(-i / (A ** 2))
            xy = self.clothoid((i ** 2) / (2 * (A ** 2)), A)
            self.lanes[0]['X_center'].append(X_start_clothoide + xy[0] * cos(phi_s) + xy[1] * sin(phi_s))
            self.lanes[0]['Y_center'].append(Y_start_clothoide + xy[0] * sin(phi_s) - xy[1] * cos(phi_s))
            self.lanes[0]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s - i ** 2 / (2 * A ** 2) + pi / 2))
            self.lanes[0]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s - i ** 2 / (2 * A ** 2) + pi / 2))
            self.lanes[0]['X_right'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s - i ** 2 / (2 * A ** 2) - pi / 2))
            self.lanes[0]['Y_right'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s - i ** 2 / (2 * A ** 2) - pi / 2))
            for j in range(1, self.Number_of_lanes):
                self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']
                self.lanes[j]['X_center'].append(self.lanes[0]['X_center'][self.indexcount] + (j * self.lanewidth) * cos(phi_s - i ** 2 / (2 * A ** 2) + pi / 2))
                self.lanes[j]['Y_center'].append(self.lanes[0]['Y_center'][self.indexcount] + (j * self.lanewidth) * sin(phi_s - i ** 2 / (2 * A ** 2) + pi / 2))
                self.lanes[j]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + (self.lanewidth_half + j * self.lanewidth) * cos(phi_s - i ** 2 / (2 * A ** 2) + pi / 2))
                self.lanes[j]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + (self.lanewidth_half + j * self.lanewidth) * sin(phi_s - i ** 2 / (2 * A ** 2) + pi / 2))
            self.indexcount += 1

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['curvatureend'] = -1 / R
        self.road_data[self.road_data_indexcount]['A'] = A
        self.road_data_indexcount += 1

        phi_e = phi_s - phi
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e

    # user defined function for X,Y coordinate calculation in clock direction clothoid arc connecting from circle to line type track
    def clothoid_arc_cir_lin_clock(self, l, R, X_start, Y_start, phi_s):
        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'Clothoid'
        self.road_data[self.road_data_indexcount]['sbegin'] = self.indexcount
        self.road_data[self.road_data_indexcount]['curvaturebegin'] = -1 / R

        A = sqrt(l * R)
        phi = l ** 2 / (2 * (A ** 2))

        xy = self.clothoid(l ** 2 / (2 * (A ** 2)), A)
        clothoide_size_X = xy[0]
        clothoide_size_Y = xy[1]

        X_start_clothoide = X_start + clothoide_size_X * cos(phi_s - phi) - clothoide_size_Y * sin(phi_s - phi)
        Y_start_clothoide = Y_start + clothoide_size_X * sin(phi_s - phi) + clothoide_size_Y * cos(phi_s - phi)

        for i in range(l - 1, -1, -1):
            self.S.append(self.indexcount)
            self.curvature.append(-i / (A ** 2))
            xy = self.clothoid((i ** 2) / (2 * (A ** 2)), A)
            self.lanes[0]['X_center'].append(X_start_clothoide + xy[0] * cos(phi_s - phi - pi) - xy[1] * sin(phi_s - phi - pi))
            self.lanes[0]['Y_center'].append(Y_start_clothoide + xy[0] * sin(phi_s - phi - pi) + xy[1] * cos(phi_s - phi - pi))
            self.lanes[0]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s - phi - pi + i ** 2 / (2 * A ** 2) - pi / 2))
            self.lanes[0]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s - phi - pi + i ** 2 / (2 * A ** 2) - pi / 2))
            self.lanes[0]['X_right'].append(self.lanes[0]['X_center'][self.indexcount] + self.lanewidth_half * cos(phi_s - phi - pi + i ** 2 / (2 * A ** 2) + pi / 2))
            self.lanes[0]['Y_right'].append(self.lanes[0]['Y_center'][self.indexcount] + self.lanewidth_half * sin(phi_s - phi - pi + i ** 2 / (2 * A ** 2) + pi / 2))
            for j in range(1, self.Number_of_lanes):
                self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']
                self.lanes[j]['X_center'].append(self.lanes[0]['X_center'][self.indexcount] + (j * self.lanewidth) * cos(phi_s - phi - pi + i ** 2 / (2 * A ** 2) - pi / 2))
                self.lanes[j]['Y_center'].append(self.lanes[0]['Y_center'][self.indexcount] + (j * self.lanewidth) * sin(phi_s - phi - pi + i ** 2 / (2 * A ** 2) - pi / 2))
                self.lanes[j]['X_left'].append(self.lanes[0]['X_center'][self.indexcount] + (self.lanewidth_half + j*self.lanewidth) * cos(phi_s - phi - pi + i ** 2 / (2 * A ** 2) - pi / 2))
                self.lanes[j]['Y_left'].append(self.lanes[0]['Y_center'][self.indexcount] + (self.lanewidth_half + j*self.lanewidth) * sin(phi_s - phi - pi + i ** 2 / (2 * A ** 2) - pi / 2))
            self.indexcount += 1

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['curvatureend'] = 0
        self.road_data[self.road_data_indexcount]['A'] = A
        self.road_data_indexcount += 1

        phi_e = phi_s - phi
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e

    # function to calculate track coordinates X,Y including straight line, clothoid and circular arc
    def trajectory(self, road, length, arc):

        count = 0

        for data in road:
            l = length[count]
            R = arc[count]

            # 'Str' = Straight line
            if data == 'Str':
                self.X_start, self.Y_start, self.phi_s = self.straight_line(l, self.X_start, self.Y_start, self.phi_s)
                count += 1

            # 'Cir1' = circular arc with anticlock direction
            elif data == 'Cir1':
                self.X_start, self.Y_start, self.phi_s = self.circular_arc_anticlock(l, R, self.X_start, self.Y_start, self.phi_s)
                count += 1

            # 'Cir2' = circular arc with clock direction
            elif data == 'Cir2':
                self.X_start, self.Y_start, self.phi_s = self.circular_arc_clock(l, R, self.X_start, self.Y_start, self.phi_s)
                count += 1

            # 'Clo1' = clothoid arc with anticlock direction connecting from line to circle
            elif data == 'Clo1':
                self.X_start, self.Y_start, self.phi_s = self.clothoid_arc_lin_cir_anticlock(l, R, self.X_start, self.Y_start, self.phi_s)
                count += 1

            # 'Clo2' = clothoid arc with anticlock direction connecting from circle to line
            elif data == 'Clo2':
                self.X_start, self.Y_start, self.phi_s = self.clothoid_arc_cir_lin_anticlock(l, R, self.X_start, self.Y_start, self.phi_s)
                count += 1

            # 'Clo3' = clothoid arc with clock direction connecting from line to circle
            elif data == 'Clo3':
                self.X_start, self.Y_start, self.phi_s = self.clothoid_arc_lin_cir_clock(l, R, self.X_start, self.Y_start, self.phi_s)
                count += 1

            # 'Clo4' = clothoid arc with clock direction connecting from circle to line
            elif data == 'Clo4':
                self.X_start, self.Y_start, self.phi_s = self.clothoid_arc_cir_lin_clock(l, R, self.X_start, self.Y_start, self.phi_s)
                count += 1

            else:
                print('Invalid inputs')



    

