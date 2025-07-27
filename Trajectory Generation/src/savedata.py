class SaveData:   # class to save files
    # class initialisation with files as arguments
    def __init__(self, S, lanes, speedprofile, speedreferance):
        self.S = S
        self.lanes = lanes
        self.speedprofile = speedprofile
        self.speedreferance = speedreferance

    # function to save an array as txt file
    def savedata_array(self, filename, array):
        array = array.flatten()
        # Open a file in write mode
        with open(filename, 'w') as file:
            # Write each element of the list to the file
            for item in array:
                file.write(str(item) + '\n')

    # function to save a list as txt file
    def savedata_list(self, filename, list):
        # Open a file in write mode
        with open(filename, 'w') as file:
            # Write each element of the list to the file
            for item in list:
                file.write(str(item) + '\n')

    # function to save files with appropriate file names
    def save(self,number_lanes):
        for count in range(number_lanes):
            # condition check for lenth of all files, they should be equal
            if (len(self.S) == len(self.lanes[count]['X_center']) == len(self.lanes[count]['Y_center']) == len(self.lanes[count]['X_left']) == len(self.lanes[count]['Y_left']) ==
                    len(self.lanes[count]['X_right']) == len(self.lanes[count]['Y_right']) == self.speedprofile.shape[1] == self.speedreferance.shape[1]):
                if count == 0:
                    self.savedata_list("Indices_list.txt", self.S)
                    self.savedata_array("speed_max.txt", self.speedprofile)
                    self.savedata_array("speed_referance.txt", self.speedreferance)
                self.savedata_list(f"lane{count+1}_X_center.txt", self.lanes[count]['X_center'])
                self.savedata_list(f"lane{count+1}_Y_center.txt", self.lanes[count]['Y_center'])
                self.savedata_list(f"lane{count+1}_X_left.txt", self.lanes[count]['X_left'])
                self.savedata_list(f"lane{count+1}_Y_left.txt", self.lanes[count]['Y_left'])
                self.savedata_list(f"lane{count+1}_X_right.txt", self.lanes[count]['X_right'])
                self.savedata_list(f"lane{count+1}_Y_right.txt", self.lanes[count]['Y_right'])

            else:
                # this blocks executes it something is wrong in data files
                print(f'Dimension mismatch for lane {count+1}, recheck inputs provided and code file')
                print(f"length of X_center: {len(self.lanes[count]['X_center'])}")
                print(f"length of Y_center: {len(self.lanes[count]['Y_center'])}")
                print(f"length of X_left: {len(self.lanes[count]['X_left'])}")
                print(f"length of Y_left: {len(self.lanes[count]['Y_left'])}")
                print(f"length of X_right: {len(self.lanes[count]['X_right'])}")
                print(f"length of Y_right: {len(self.lanes[count]['Y_right'])}")
                print(f"length of speed_profile: {self.speedprofile.shape[1]}")
                print(f"length of speed_referance: {self.speedreferance.shape[1]}")
