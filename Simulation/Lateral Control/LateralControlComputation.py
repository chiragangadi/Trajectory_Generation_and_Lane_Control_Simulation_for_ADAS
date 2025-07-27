# In der folgenden Zeile wird die Anzahl der Ausg‰nge festgelegt (hier 2):
# nOut = 2
# In den folgenden drei Zeilen werden die Namen der Ausg‰nge 
# festgelegt (kann entfallen, dann werden Standardnamen gew‰hlt)
# Out_1 = "Lateral distance" 
# Out_2 = "exit simulation"

# Nachfolgend wird die eigentliche Funktion deklariert
# Sie MUSS "main" heiﬂen!
# Die Anzahl der Blockeing‰nge (hier 3) wird automatisch
# aus der Parameterliste erkannt, ebenso die Namen der 
# Blockeing‰nge (hier psi, pos_x, pos_y)

import math

# Global variables
X_route = []
Y_route = []
data_read = 0
i_smaller_old = 0

def main(Init, Terminate, psi, pos_x, pos_y):
    global X_route, Y_route, data_read, i_smaller_old

    # Variables for data file operations
    org_line_X = ""
    org_line_Y = ""
    dataPath_X = "route_right_X_en.txt"   # Give file if file is present in same directory
    dataPath_Y = "route_right_Y_en.txt"   # Give full path if file is in different directory
    x_read = 0
    y_read = 0
    
    # Variables for computations
    p_x, p_y = 0, 0
    q_x, q_y = 0, 0
    i, i_smaller = 0, 0
    condition_point = 0
    dx1, dy1, dx2, dy2, l1, l2 = 0, 0, 0, 0, 0, 0
    nx1, ny1, nx2, ny2 = 0, 0, 0, 0
    rho1, rho2 = 0, 0
    det_1, det_2, det_3, det_4 = 0, 0, 0, 0
    e_x, e_y = 0, 0
    lateral_distance = 0
    
    # The constant pi needs to be defined
    pi = 3.1415926535

    # During the initialization of the simulation Init = 1
    if Init == 1:
        ForReading = 1
        
        # Reading the file containing the complete trajectory in X coordinates and storing in new array
        try:
            with open(dataPath_X, 'r') as file_x:
                for org_line_X in file_x:
                    X_route.append(float(org_line_X))
            x_read = 1
        except FileNotFoundError:
            pass
            
        # Reading the file containing the complete trajectory in Y coordinates and storing in new array
        try:
            with open(dataPath_Y, 'r') as file_y:
                for org_line_Y in file_y:
                    Y_route.append(float(org_line_Y))
            y_read = 1
        except FileNotFoundError:
            pass
        # IF else statements for checking route data of x and y coordinates have been read correctly or not
        if x_read == 1 and y_read == 1:
            # Below code is executed if both the files are read
            if len(X_route) == len(Y_route):
                # Condition for identical number of coordinates in both X and Y
                data_read = 1
            else:
                # If one of the file has incorrect number of coordinates
                print("One of the data files is incorrect")
                print("The simulation is terminated!")
                data_read = 0
        else:
            # If one or both the files are not read
            print("One of the data files could not be read!")
            print("The simulation is terminated!")
            data_read = 0
        
        lateral_distance = 1.5     # Initialize output variable
       
        
    # After the simulation, Terminate = 1 is set for a call
    elif Terminate == 1:
        print("Termination takes place!")
        Terminate()
        
    if data_read == 1:
        # The following lines of code are executed in every simulation step after the data files are completely read
            
        # Computation to determine the point P
        p_x = pos_x + 10 * math.cos(psi)
        p_y = pos_y + 10 * math.sin(psi)
            
        # Computation to determine the auxiliary point Q
        q_x = p_x + 10 * math.cos(psi - (pi/2))
        q_y = p_y + 10 * math.sin(psi - (pi/2))
            
        # Find the maximum value of the index i for which the condition is less than or equal to zero ...
        i = i_smaller_old
        condition_point = (q_x - p_x) * (Y_route[i] - p_y) - (X_route[i] - p_x) * (q_y - p_y)
            
        while condition_point <= 0 and i <= len(X_route) - 2:
            if condition_point <= 0:
                i_smaller = i
                
            i += 1
                
            if i >= len(X_route):
                i = len(X_route) - 1
                
            condition_point = (q_x - p_x) * (Y_route[i] - p_y) - (X_route[i] - p_x) * (q_y - p_y)
            
        i_smaller_old = i_smaller  # Save the current "i_smaller" for the next run
         
        # Components of the line by connecting the two vertices of the "edge of the road"   
        dx1 = X_route[i_smaller + 1] - X_route[i_smaller]
        dy1 = Y_route[i_smaller + 1] - Y_route[i_smaller]
        
        # Components of the line by connecting points P and Q    
        dx2 = q_x - p_x
        dy2 = q_y - p_y
        
        # Calculating the length of the connecting lines    
        l1 = math.sqrt(dx1*dx1 + dy1*dy1)
        l2 = math.sqrt(dx2*dx2 + dy2*dy2)
        
        # Components of the normal vector, perpendicular to the polygon chain    
        nx1 = dy1 / l1
        ny1 = -1 * (dx1 / l1)
        
        # Components of the normal vector, perpendicular to the line PQ    
        nx2 = dy2 / l2
        ny2 = -1 * (dx2 / l2)
        
        # Calculate the distance parameter Rho for the Hessian normal form of the two straight lines    
        rho1 = nx1 * X_route[i_smaller] + ny1 * Y_route[i_smaller]
        rho2 = nx2 * p_x + ny2 * p_y
        
        # Calculate the intersection of the straight lines using Cramerís rule
        # For Cramerís rule and lienar equations refer to:
        # Hoehere Mathematik fuer Ingenieure
        # Burg / Haf / Wille; Band II; Seite 42    
        det_1 = rho1 * ny2 - rho2 * ny1
        det_2 = nx1 * ny2 - ny1 * nx2
        det_3 = nx1 * rho2 - nx2 * rho1
        det_4 = nx1 * ny2 - nx2 * ny1
            
        e_x = det_1 / det_2
        e_y = det_3 / det_4
        
        # Calculate the value oft he lateral distance    
        lateral_distance = math.sqrt((e_x - p_x)**2 + (e_y - p_y)**2)
        
        # Check if the point P is to the right or left edge of the road with respect to the centre of gravity of the vehicle    
        condition_point = (e_x - pos_x) * (p_y - pos_y) - (p_x - pos_x) * (e_y - pos_y)
        
        # If the point P is to the right of the edge of line, the sign of the lateral distance must be corrected    
        if condition_point < 0:
            lateral_distance *= -1
            
    else:
        # If the data files have not been completely read, a constant value is assigned to the outputs
        lateral_distance = 1.5
    
    Out_1.value = lateral_distance
    
    # If the data file have not been read completely, the output 2 "exit_simulation" is assigned with the value of 5 == logic 1 and the simulation in the higher level module is ended. 
    # However, if the data files have been read completely, the output 2 "exit_simulation" is assigned with the value of 0 and the simulation runs normally.

    if data_read == 0:
        Out_2.value = 5
    else:
        Out_2.value = 0
