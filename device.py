import pandas
import sqlalchemy
import pymysql


class Device():
    def __init__(self, start, end, device_type):
        self.start = start
        self.end = end
        self.device_type = device_type
        self.range = self.address_range()
        self.count = len(self.range)
        self.device_df = self.address_df()

    def address_range(self):
        addresses_list = []

        #Iterate through defined addresses for station 1
        for address in range(int(self.start, 16), int(self.end, 16) + 1):
            address_hex = hex(address) #convert to hex
            address_str = str(address_hex) #convert from hex to string
            x = address_str.replace('0x', self.device_type)
            addresses_list.append(x.upper())
            
        return(addresses_list)

    def address_df(self):
        '''Returns a dataframe with device id and device name'''
        device_dict = {
            'id': (x for x in range(1, (self.count+1))),
            'device_name':self.range
        }
        df = pandas.DataFrame(device_dict)

        return(df)

if __name__ == '__main__':
    B_device = Device(start='0x0', end='0x3FFF', device_type='B')
    M_device = Device(start='0x0', end='0x20479', device_type='M')
    X_device = Device(start='0x0', end='0x1FFF', device_type='X')
    Y_device = Device(start='0x0', end='0x1FFF', device_type='Y')


    df = M_device.device_df
    print(df)

