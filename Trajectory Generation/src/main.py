from generate_trajectory import PathGenerate     # importing PathGenerate class
from generate_speedprofile import SpeedProfile   # importing SpeedProfile class
from savedata import SaveData                    # importing SaveData class
import matplotlib.pyplot as plt

###############################################################################################################################################################
# provide the data (L,R) for each section of track to be generated.
# 'Str' = Straight line,  'Cir1' = circular arc with anticlock direction, 'Cir2' = circular arc with clock direction,
# 'Clo1' = clothoid arc with anticlock direction connecting from line to circle,  'Clo2' = clothoid arc with anticlock direction connecting from circle to line
# 'Clo3' = clothoid arc with clock direction connecting from line to circle,  'Clo4' = clothoid arc with clock direction connecting from circle to line
# NOTE: order of defining the strings in road_1 is crucial.
# NOTE: arc of clothoid is kept same as arc of circle which is connected to it.
###############################################################################################################################################################
# path configurations
path_type = ['Str', 'Clo1', 'Cir1', 'Clo2', 'Str', 'Clo3', 'Cir2', 'Clo4', 'Str', 'Clo1', 'Cir1', 'Clo2', 'Str']
           #  L1      L2      L3      L4      L5     L6      L7      L8      L9     L10     L11     L12     L13
length   = [ 500,     20,     300,    20,     200,   20,     80,     20,    200,    100,    160,    100,    500]
           #  R1      R2      R3      R4      R5     R6      R7      R8      R9     R10     R11     R12     R13
arc      = [  0,     140,     140,   140,      0,    70,     70,     70,      0,    120,    120,    120,      0]

number_lanes = 3        # provide number of lanes data need to be generated
lanewidth = 30          # width of single lane

# initial conditions
X_start = 0             # start point in X axis
Y_start = 15            # start point in Y axis
phi_s = 0               # start of angle in radians

# path generation
path = PathGenerate(X_start,Y_start,phi_s,lanewidth,number_lanes)   # object initialisation
path.trajectory(path_type, length, arc)  # function call

# velocity profile generation
speed = SpeedProfile(path.road_data, path.S)  # object initialisation
speed.generate_speedprofile()     # function call

# saving path and velocity profile in .txt file
save = SaveData(path.S, path.lanes, speed.speed_profile, speed.reference_value)   # object initialisation
save.save(number_lanes)      # function call

for i in range(number_lanes):
    plt.plot(path.lanes[i]['X_center'], path.lanes[i]['Y_center'], linestyle='--', label=f"Lane{i+1}_center")
    plt.plot(path.lanes[i]['X_right'], path.lanes[i]['Y_right'], label=f"Lane{i+1}_right")
    plt.plot(path.lanes[i]['X_left'], path.lanes[i]['Y_left'], label=f"Lane{i+1}_left")

plt.title('Trajectory')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()