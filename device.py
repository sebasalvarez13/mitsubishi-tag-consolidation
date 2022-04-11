

class Device():
    def __init__(self, start, end, device_type):
        self.start = start
        self.end = end
        self.device_type = device_type
        self.range = self.address_range()

    def address_range(self):
        addresses_list = []

        #Iterate through defined addresses for station 1
        for address in range(int(self.start, 16), int(self.end, 16) + 1):
            address_hex = hex(address) #convert to hex
            address_str = str(address_hex) #convert from hex to string
            x = address_str.replace('0x', self.device_type)
            addresses_list.append(x.upper())
            
        return(addresses_list)


if __name__ == '__main__':
    start = '0x0'
    end = '0x100'

    d1 = Device(start, end, 'M')
    print(d1.address_range())
    