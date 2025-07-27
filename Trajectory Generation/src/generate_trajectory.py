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

    # user defined function to calculate X,Y coordinates in clothoid region
    def clothoid(self, alpha, a):        
        sum_x = 0
        sum_y = 0

        for count in range(41):
            sum_x += ((-1) ** count * alpha ** (2 * count)) / ((4 * count + 1) * factorial(2 * count))
            sum_y += ((-1) ** count * alpha ** (2 * count + 1)) / ((4 * count + 3) * factorial(2 * count + 1))

        x = a * sqrt(2 * alpha) * sum_x
        y = a * sqrt(2 * alpha) * sum_y

        result = [x, y]
        return result                     

    # user defined function used in for loop with float data type
    def range_float(self, start, stop, step):      
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

    # user defined function for X Y coordinate calculation in circular arc type track
    def circular_arc(self, l, R, X_start, Y_start, phi_s, direction):
        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'CircularArc'
        self.road_data[self.road_data_indexcount]['sbegin'] = self.indexcount

        # Direction: anticlockwise = +1 curvature, clockwise = -1 curvature
        sign = -1 if direction == 'clockwise' else 1
        curvature = sign / R
        self.road_data[self.road_data_indexcount]['curvaturebegin'] = curvature

        # Arc center
        Mx = X_start + R * cos(phi_s + sign * pi / 2)
        My = Y_start + R * sin(phi_s + sign * pi / 2)

        # Start and end angle for the arc
        theta_start = phi_s - sign * pi / 2 + sign * (1 / R)
        theta_end = phi_s - sign * pi / 2 + sign * (l / R)

        for i in self.range_float(theta_start, theta_end, sign * (1 / R)):
            self.S.append(self.indexcount)
            self.curvature.append(curvature)

            # Lane 0
            self.lanes[0]['X_center'].append(Mx + R * cos(i))
            self.lanes[0]['Y_center'].append(My + R * sin(i))
            self.lanes[0]['X_left'].append(Mx + (R - sign * self.lanewidth_half) * cos(i))
            self.lanes[0]['Y_left'].append(My + (R - sign * self.lanewidth_half) * sin(i))
            self.lanes[0]['X_right'].append(Mx + (R + sign * self.lanewidth_half) * cos(i))
            self.lanes[0]['Y_right'].append(My + (R + sign * self.lanewidth_half) * sin(i))

            for j in range(1, self.Number_of_lanes):
                self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']

                offset_center = R - sign * j * self.lanewidth
                offset_left = R - sign * (j * self.lanewidth + self.lanewidth_half)

                self.lanes[j]['X_center'].append(Mx + offset_center * cos(i))
                self.lanes[j]['Y_center'].append(My + offset_center * sin(i))
                self.lanes[j]['X_left'].append(Mx + offset_left * cos(i))
                self.lanes[j]['Y_left'].append(My + offset_left * sin(i))

            self.indexcount += 1

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['curvatureend'] = curvature
        self.road_data[self.road_data_indexcount]['R'] = sign * R
        self.road_data_indexcount += 1

        phi_e = phi_s + sign * l / R
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e

    
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

    # user defined function for X Y coordinate calculation in clothoid arc type track
    def clothoid_arc(self, l, R, X_start, Y_start, phi_s, direction, transition):
        """
        Generalized clothoid arc generator function.

        Parameters:
        - l: Clothoid length
        - R: Target curvature radius
        - X_start, Y_start: Starting coordinates
        - phi_s: Starting angle (radians)
        - direction: 'anticlockwise' or 'clockwise'
        - transition: 'lin_to_cir' or 'cir_to_lin'
        """

        self.road_data[self.road_data_indexcount] = {}
        self.road_data[self.road_data_indexcount]['typ'] = 'Clothoid'
        self.road_data[self.road_data_indexcount]['sbegin'] = self.indexcount

        A = sqrt(l * R)
        phi = (l ** 2) / (2 * (A ** 2))
        phi_sign = 1 if direction == 'anticlockwise' else -1
        curvature_sign = 1 if direction == 'anticlockwise' else -1

        if transition == 'line_to_circle':
            self.road_data[self.road_data_indexcount]['curvaturebegin'] = 0

            for i in range(1, l + 1):
                s = i
                curv = curvature_sign * i / (A ** 2)
                theta = phi_sign * (i ** 2) / (2 * A ** 2)

                self.S.append(self.indexcount)
                self.curvature.append(curv)
                xy = self.clothoid((i ** 2) / (2 * A ** 2), A)
                x = xy[0]
                y = xy[1]

                X_center = X_start + x * cos(phi_s) - y * sin(phi_s) if direction == 'anticlockwise' else X_start + x * cos(phi_s) + y * sin(phi_s)
                Y_center = Y_start + x * sin(phi_s) + y * cos(phi_s) if direction == 'anticlockwise' else Y_start + x * sin(phi_s) - y * cos(phi_s)

                self.lanes[0]['X_center'].append(X_center)
                self.lanes[0]['Y_center'].append(Y_center)

                angle = phi_s + theta if direction == 'anticlockwise' else phi_s - theta

                self.lanes[0]['X_left'].append(X_center + self.lanewidth_half * cos(angle + pi / 2))
                self.lanes[0]['Y_left'].append(Y_center + self.lanewidth_half * sin(angle + pi / 2))
                self.lanes[0]['X_right'].append(X_center + self.lanewidth_half * cos(angle - pi / 2))
                self.lanes[0]['Y_right'].append(Y_center + self.lanewidth_half * sin(angle - pi / 2))

                for j in range(1, self.Number_of_lanes):
                    self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                    self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']
                    offset = self.lanewidth_half + j * self.lanewidth
                    self.lanes[j]['X_center'].append(X_center + j * self.lanewidth * cos(angle + pi / 2))
                    self.lanes[j]['Y_center'].append(Y_center + j * self.lanewidth * sin(angle + pi / 2))
                    self.lanes[j]['X_left'].append(X_center + offset * cos(angle + pi / 2))
                    self.lanes[j]['Y_left'].append(Y_center + offset * sin(angle + pi / 2))

                self.indexcount += 1

            self.road_data[self.road_data_indexcount]['curvatureend'] = curvature_sign / R

        elif transition == 'circle_to_line':
            self.road_data[self.road_data_indexcount]['curvaturebegin'] = curvature_sign / R

            xy = self.clothoid((l ** 2) / (2 * A ** 2), A)
            x = xy[0]
            y = xy[1]

            angle_shift = phi_sign * phi
            X_start_clothoide = X_start + x * cos(phi_s + angle_shift) + y * sin(phi_s + angle_shift) if direction == 'anticlockwise' else X_start + x * cos(phi_s + angle_shift) - y * sin(phi_s + angle_shift)
            Y_start_clothoide = Y_start + x * sin(phi_s + angle_shift) - y * cos(phi_s + angle_shift) if direction == 'anticlockwise' else Y_start + x * sin(phi_s + angle_shift) + y * cos(phi_s + angle_shift)

            for i in range(l - 1, -1, -1):
                curv = curvature_sign * i / (A ** 2)
                theta = phi_sign * (i ** 2) / (2 * A ** 2)
                self.S.append(self.indexcount)
                self.curvature.append(curv)
                xy = self.clothoid((i ** 2) / (2 * A ** 2), A)
                x = xy[0]
                y = xy[1]

                phi_offset = phi_s + phi_sign * phi - pi

                X_center = X_start_clothoide + x * cos(phi_offset) + y * sin(phi_offset) if direction == 'anticlockwise' else X_start_clothoide + x * cos(phi_offset) - y * sin(phi_offset)
                Y_center = Y_start_clothoide + x * sin(phi_offset) - y * cos(phi_offset) if direction == 'anticlockwise' else Y_start_clothoide + x * sin(phi_offset) + y * cos(phi_offset)

                self.lanes[0]['X_center'].append(X_center)
                self.lanes[0]['Y_center'].append(Y_center)

                angle = phi_offset - theta if direction == 'anticlockwise' else phi_offset + theta

                self.lanes[0]['X_right'].append(X_center + self.lanewidth_half * cos(angle + pi / 2))
                self.lanes[0]['Y_right'].append(Y_center + self.lanewidth_half * sin(angle + pi / 2))
                self.lanes[0]['X_left'].append(X_center + self.lanewidth_half * cos(angle - pi / 2))
                self.lanes[0]['Y_left'].append(Y_center + self.lanewidth_half * sin(angle - pi / 2))

                for j in range(1, self.Number_of_lanes):
                    self.lanes[j]['X_right'] = self.lanes[j - 1]['X_left']
                    self.lanes[j]['Y_right'] = self.lanes[j - 1]['Y_left']
                    offset = self.lanewidth_half + j * self.lanewidth
                    self.lanes[j]['X_center'].append(X_center + j * self.lanewidth * cos(angle - pi / 2))
                    self.lanes[j]['Y_center'].append(Y_center + j * self.lanewidth * sin(angle - pi / 2))
                    self.lanes[j]['X_left'].append(X_center + offset * cos(angle - pi / 2))
                    self.lanes[j]['Y_left'].append(Y_center + offset * sin(angle - pi / 2))

                self.indexcount += 1

            self.road_data[self.road_data_indexcount]['curvatureend'] = 0

        self.road_data[self.road_data_indexcount]['send'] = self.indexcount - 1
        self.road_data[self.road_data_indexcount]['A'] = A
        self.road_data_indexcount += 1

        phi_e = phi_s + phi_sign * phi
        X_end = self.lanes[0]['X_center'][self.indexcount - 1]
        Y_end = self.lanes[0]['Y_center'][self.indexcount - 1]

        return X_end, Y_end, phi_e


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
                self.X_start, self.Y_start, self.phi_s = self.circular_arc(l, R, self.X_start, self.Y_start, self.phi_s, "anticlockwise")
                count += 1

            # 'Cir2' = circular arc with clock direction
            elif data == 'Cir2':
                self.X_start, self.Y_start, self.phi_s = self.circular_arc(l, R, self.X_start, self.Y_start, self.phi_s, "clockwise")
                count += 1

            # 'Clo1' = clothoid arc with anticlock direction connecting from line to circle
            elif data == 'Clo1':
                self.X_start, self.Y_start, self.phi_s = self.clothoid_arc(l, R, self.X_start, self.Y_start, self.phi_s, direction="anticlockwise", transition="line_to_circle")
                count += 1

            # 'Clo2' = clothoid arc with anticlock direction connecting from circle to line
            elif data == 'Clo2':
                self.X_start, self.Y_start, self.phi_s = self.clothoid_arc(l, R, self.X_start, self.Y_start, self.phi_s, direction="anticlockwise", transition="circle_to_line")
                count += 1

            # 'Clo3' = clothoid arc with clock direction connecting from line to circle
            elif data == 'Clo3':
                self.X_start, self.Y_start, self.phi_s = self.clothoid_arc(l, R, self.X_start, self.Y_start, self.phi_s, direction="clockwise", transition="line_to_circle")
                count += 1

            # 'Clo4' = clothoid arc with clock direction connecting from circle to line
            elif data == 'Clo4':
                self.X_start, self.Y_start, self.phi_s = self.clothoid_arc(l, R, self.X_start, self.Y_start, self.phi_s, direction="clockwise", transition="circle_to_line")
                count += 1

            else:
                print('Invalid inputs')
    

